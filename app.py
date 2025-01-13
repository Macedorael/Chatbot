from flask import Flask, request, jsonify, render_template, session
import boto3
import uuid
import threading
import logging
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import json
import time
import requests

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Permite requisições de outros domínios

app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")

# Configuração do logging
logging.basicConfig(level=logging.INFO)

# Inicializa o cliente do Lex
lex_client = boto3.client("lexv2-runtime", region_name="us-east-1")
transcribe_client = boto3.client("transcribe", region_name="us-east-1")
# Inicializa o cliente do S3
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

LEX_BOT_ID = os.getenv("LEX_BOT_ID")
LEX_BOT_ALIAS_ID = os.getenv("LEX_BOT_ALIAS_ID")
LEX_LOCALE_ID = os.getenv("LEX_LOCALE_ID")

# Dicionário para controle de requisições
session_locks = {}

@app.route("/")
def home():
    user_id = str(uuid.uuid4())  # Gera um novo ID único para o usuário
    session["user_id"] = user_id  # Armazena o user_id na sessão
    session["session_id"] = str(uuid.uuid4())  # Gera um session_id único para o bot
    return render_template("index.html")  # Serve a página HTML

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("message")
    user_id = session.get("user_id")
    session_id = session.get("session_id")
    file = request.files.get("file")

    if not user_id or not session_id:
        return jsonify({"error": "Sessão do usuário não encontrada."}), 400

    # Inicializa o lock para a sessão
    if user_id not in session_locks:
        session_locks[user_id] = threading.Lock()

    lock = session_locks[user_id]

    with lock:
        try:
            file_url = None
            status_message = None
            if file:
                # Valida se o arquivo foi enviado corretamente
                if not file.filename:
                    return jsonify({"error": "Nenhum arquivo enviado."}), 400

                # Verifica se o arquivo tem uma extensão válida para transcrição
                valid_extensions = ['.mp3', '.wav', '.flac', '.m4a', '.jpg', '.jpeg', '.png']
                if not any(file.filename.lower().endswith(ext) for ext in valid_extensions):
                    return jsonify({"error": "Arquivo com formato inválido. Apenas arquivos de áudio e imagem são aceitos."}), 400

                # Upload do arquivo de imagem ou áudio para o S3
                file_key = f"{uuid.uuid4()}_{file.filename}"
                try:
                    s3_client.upload_fileobj(file, BUCKET_NAME, file_key)
                    file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_key}"
                    logging.info(f"Arquivo enviado para o S3 com sucesso: {file_key}")
                    user_input = file_key  # Usar a URL do arquivo no Lex
                except Exception as e:
                    logging.error(f"Erro ao enviar o arquivo para o S3: {str(e)}")
                    return jsonify({"error": "Erro ao enviar o arquivo para o S3."}), 500

                # Inicia a transcrição de áudio (se aplicável)
                if file.filename.lower().endswith(tuple(['.mp3', '.wav', '.flac', '.m4a'])):
                    transcribe_job_name = f"transcribe-{uuid.uuid4()}"
                    media_format = file.filename.split('.')[-1]
                    try:
                        logging.info(f"Iniciando transcrição para o arquivo {file_url}")
                        transcribe_client.start_transcription_job(
                            TranscriptionJobName=transcribe_job_name,
                            Media={'MediaFileUri': file_url},
                            MediaFormat=media_format,
                            LanguageCode="pt-BR"
                        )
                        status_message = "Transcrição em andamento..."
                        # Espera pela transcrição ser concluída
                        while True:
                            status = transcribe_client.get_transcription_job(TranscriptionJobName=transcribe_job_name)
                            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                                break
                            time.sleep(1)

                        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
                            transcription_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                            transcription_response = requests.get(transcription_url)
                            transcription_text = transcription_response.json()['results']['transcripts'][0]['transcript']
                            logging.info(f"Texto da transcrição: {transcription_text}")
                            user_input = transcription_text  
                        else:
                            logging.error("Erro na transcrição do áudio.")
                            return jsonify({"error": "Erro na transcrição do áudio."}), 500

                    except Exception as e:
                        logging.error(f"Erro ao iniciar ou obter a transcrição: {str(e)}")
                        return jsonify({"error": "Erro ao processar o áudio."}), 500
            
            # Verifica se o user_input está vazio após a transcrição
            if not user_input:
                logging.error("Input do usuário está vazio após a transcrição.")
                return jsonify({"error": "Texto vazio após a transcrição."}), 400

            # Envia o input para o Lex
            response = lex_client.recognize_text(
                botId=LEX_BOT_ID,
                botAliasId=LEX_BOT_ALIAS_ID,
                localeId=LEX_LOCALE_ID,
                sessionId=session_id,
                text=user_input,
            )

            logging.info("Resposta do Lex: %s", response)
            messages = []
            card = None
            buttons = []

            if "messages" in response:
                for msg in response["messages"]:
                    if msg["contentType"] == "PlainText":
                        messages.append(msg["content"])
                    elif msg["contentType"] == "ImageResponseCard":
                        card = msg["imageResponseCard"]
                        buttons = card.get("buttons", [])

                dialog_action = response["sessionState"].get("dialogAction", {})
                dialog_state = dialog_action.get("type")

                return jsonify(
                    {
                        "message": messages,
                        "card": {
                            "title": card.get("title"),
                            "subtitle": card.get("subtitle"),
                            "imageUrl": card.get("imageUrl"),
                            "buttons": buttons
                        } if card else None,
                        "dialogState": dialog_state,
                        "file_url": file_url,
                        "status_message": status_message
                    }
                )

        except Exception as e:
            logging.error("Erro ao chamar o Lex: %s", str(e))
            return jsonify({"error": str(e)}), 500


@app.route('/get-transcription', methods=['GET'])
def get_transcription():
    job_name = request.args.get('job_name')
    
    if not job_name:
        return jsonify({'error': 'Job name is required'}), 400

    try:
        result = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)

        if result['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            transcription_url = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
            transcription_response = requests.get(transcription_url)

            # Faz o parsing do conteúdo da transcrição
            transcription_text = transcription_response.json()['results']['transcripts'][0]['transcript']

            return jsonify({'text': transcription_text})

        return jsonify({'status': 'in_progress'}), 202

    except Exception as e:
        logging.error(f"Erro ao obter transcrição: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
