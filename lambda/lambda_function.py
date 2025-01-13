from bedrock import generate_recipe
from transcribe import transcribe_audio
from filtro import excluir_labels
from tradutor import traduzir_nome
from itents.saudacao import saudacoes_intent
from itents.kcal import kcal_intent
from itents.opcoes import opcoes_intent
from itents.texto import texto_intent
from itents.enviarfoto import enviar_fotos_intent
from itents.confirmacoes import confirmacoes_intent
from itents.confirmacoesquantidade import confimarcoesquantidade_intent
from itents.novosnomes import novosnomes_intent
from itents.confirmacaofinal import confirmacaofinal_intent
from itents.audio import audio_intent


import boto3 
rekognition_client = boto3.client('rekognition')

import re

itens_confirmados = []
iten_aconfirmar = []

resposta_positiva = ["sim", "s", "positivo", "yes", "ok", "certo","y"]
resposta_negativa = ["não", "nao", "n", "negativo", "no", "Ñ", "ñ"]


  # Inicialização do cliente Rekognition

def lambda_handler(event, context):
    session_attributes = event["sessionState"].get("sessionAttributes", {})
    current_intent = event["sessionState"]["intent"]["name"]
    slots = event['sessionState']['intent']['slots']

    

    if current_intent == "Saudacoes":
        return saudacoes_intent(session_attributes, slots)
    elif current_intent == "Kcal":
        return kcal_intent(session_attributes, slots)
    elif current_intent == "Opcoes":
        return opcoes_intent(session_attributes, slots)
    elif current_intent == "Texto":
        return texto_intent(session_attributes, slots,iten_aconfirmar)
    elif current_intent == "EnviarFotos":
        return enviar_fotos_intent(session_attributes, slots,iten_aconfirmar)
    elif current_intent == "Confirmacoes":
        return confirmacoes_intent(session_attributes, slots,iten_aconfirmar,itens_confirmados,resposta_positiva,resposta_negativa)
    elif current_intent == "ConfimacoesQuantidade":
        return confimarcoesquantidade_intent(session_attributes, slots,iten_aconfirmar,itens_confirmados,resposta_positiva,resposta_negativa)
    elif current_intent == "NovosNomes":
        return novosnomes_intent(session_attributes, slots,iten_aconfirmar,itens_confirmados)
    elif current_intent == "ConfirmacaoFinal":
        return confirmacaofinal_intent(session_attributes, slots,iten_aconfirmar,resposta_positiva,resposta_negativa)
    elif current_intent == "EnviarAudio":
        return audio_intent(session_attributes, slots,iten_aconfirmar)
    else:
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": "UnknownIntent", "state": "Failed"},
                "sessionAttributes": session_attributes,
            },
            "messages": [{"contentType": "PlainText", "content": "Desculpe, não entendi sua solicitação."}]
        }



