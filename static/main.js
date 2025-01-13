// Seleção de elementos DOM
const fileInput = document.getElementById('file-input');
const userInput = document.getElementById('user-input');
const chatDiv = document.getElementById('chat');
let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let recordingStartTime;
let recordingInterval;

// Função para exibir o status da transcrição
function updateTranscriptionStatus(message) {
    const transcriptionStatusElement = document.getElementById('transcription-status');
    transcriptionStatusElement.textContent = message;
}

// Função para enviar mensagens
let isWaitingForResponse = false; // Variável para controle de resposta pendente

async function sendMessage() {
    if (isWaitingForResponse) return; // Bloqueia se estiver aguardando resposta

    isWaitingForResponse = true; // Define que está aguardando resposta

    const message = userInput.value;
    const userId = 'user123';
    const loadingMessage = document.getElementById('loading'); // A div de carregamento
    const chatDiv = document.getElementById('chat'); // O chat onde as mensagens são mostradas
    const fileInput = document.getElementById('file-input'); // O campo de entrada de arquivo

    // Exibe a mensagem de "Processando a transcrição..." enquanto a requisição está em andamento
    loadingMessage.style.display = 'block';

    // Adiciona a mensagem do usuário ao chat
    if (message !== "") {
        chatDiv.innerHTML += `
            <div class="you bubble">
                <b>Você:</b> <br/>
                <p>${message}</p>
            </div>`;
    }

    userInput.value = ''; // Limpa a caixa de texto

    const formData = new FormData();
    formData.append('message', message);
    formData.append('user_id', userId);
    
    // Adiciona o arquivo, se houver
    if (fileInput.files.length > 0) {
        formData.append('file', fileInput.files[0]);
    }

    // Envio da mensagem para o servidor
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            body: formData,
        });
        
        if (!response.ok) throw new Error('Network response was not ok ' + response.statusText);
        
        const data = await response.json();
        processBotResponse(data);
        fileInput.value = '';  // Limpa o input de arquivo após o envio
        openFileInput(data);

    } catch (error) {
        console.error(error.message);
    } finally {
        isWaitingForResponse = false; // Libera para novo envio após resposta

        // Esconde a mensagem de carregamento
        loadingMessage.style.display = 'none';
    }
}


// Função para processar a resposta do bot
function processBotResponse(data) {
    if (data.message) {
        data.message.forEach(msg => {
            chatDiv.innerHTML += `
                <div class="bot bubble">
                    <b>NutriBot:</b> <br/>
                    <p>${msg}</p>
                </div>`;
        });
    }

    if (data.card) {
        const buttonsHtml = data.card.buttons.map(button => 
            `<button class="btn_card" onclick="handleButtonClick('${button.value}')">${button.text}</button>`
        ).join('');

        chatDiv.innerHTML += `
            <div class="bot bubble">
                <b>NutriBot:</b> <br/>
                <p><strong>${data.card.title}</strong></p>
                <p>${data.card.subtitle ? data.card.subtitle : ""}</p>
                ${data.card.imageUrl ? `<img src="${data.card.imageUrl}" alt="Response Card Image" style="width: 50%;"/>` : ''}
                <div class="card_buttons">${buttonsHtml}</div>
            </div>`;
    }

    chatDiv.scrollTop = chatDiv.scrollHeight; // Rola para o final do chat
}

// Função para lidar com cliques em botões da resposta do bot
function handleButtonClick(value) {
    if (isWaitingForResponse) return; // Bloqueia se estiver aguardando resposta
    userInput.value = value;  // Define o valor do campo de entrada com o texto do botão clicado
    sendMessage();  // Envia a mensagem
}

// Função para transcrição de áudio para texto
function transcribeAudioToText(audioBlob) {
    // Exibe a mensagem "Transcrevendo..." enquanto a transcrição está ocorrendo
    updateTranscriptionStatus('Transcrevendo...');
    
    // Suponha que esta função transcreva o áudio em texto
    // Aqui você faria a transcrição real
    setTimeout(() => {
        const transcribedText = "Texto transcrito do áudio"; // Texto transcrito do áudio (exemplo)
        userInput.value = transcribedText; // Atualiza o campo de entrada com o texto transcrito

        // Exibe a mensagem de conclusão da transcrição
        updateTranscriptionStatus('Transcrição concluída!');
    }, 2000); // Simulação de tempo de transcrição (a transcrição real seria assíncrona)
}

// Funções para gravação de áudio
function updateRecordingTime() {
    const elapsedTime = Math.floor((Date.now() - recordingStartTime) / 1000);
    const minutes = Math.floor(elapsedTime / 60);
    const seconds = elapsedTime % 60;
    document.getElementById('recordingTime').innerText = `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
}

function toggleRecording() {
    isRecording ? stopRecording() : startRecording();
}

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    
    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        document.getElementById('audioPlayback').src = audioUrl;

        // Cria um arquivo para o input de arquivo com nome fixo
        const file = new File([audioBlob], `recording.wav`, { type: 'audio/wav' });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        document.getElementById('uploadForm').style.display = 'block';
        document.getElementById('recordingIndicator').style.display = 'none';
        clearInterval(recordingInterval);
        document.getElementById('recordingTime').innerText = '0:00';
        audioChunks = [];
        isRecording = false;
        document.getElementById('recordButton').style.display = 'block';

        // Transcrição do áudio para texto
        transcribeAudioToText(audioBlob); // Chama a função para transcrição
    };

    mediaRecorder.start();
    isRecording = true;
    recordingStartTime = Date.now();
    recordingInterval = setInterval(updateRecordingTime, 1000);
    
    document.getElementById('recordingIndicator').style.display = 'block';
    document.getElementById('recordButton').style.display = 'none'; // Esconde botão de gravação ao gravar
}

async function stopRecording() {
    if (isRecording) {
        mediaRecorder.stop();
        document.getElementById('recordingIndicator').style.display = 'none';
        document.getElementById('recordButton').style.display = 'block'; 
        chatDiv.innerHTML += `
            <div class="bot bubble">
                <b>NutriBot:</b> <br/>
                <p>Recebendo mídia. Aguarde!</p>
            </div>`;
    }
    setTimeout(() => {
        // Simula o clique no botão "send-button"
        document.getElementById("send-button").click();
    }, 800);
}

function uploadAudioAndSendText(inputElementId) {
    const audioInput = document.getElementById("audio-input").files[0];
    const formData = new FormData();
    formData.append("audio", audioInput);

    fetch("/upload-audio", { method: "POST", body: formData })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Transcription started") {
                // Poll for transcription result
                pollTranscription(data.job_name, inputElementId);
            }
        });
}

function pollTranscription(jobName, inputElementId) {
    fetch(`/get-transcription?job_name=${jobName}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === "in_progress") {
                setTimeout(() => pollTranscription(jobName, inputElementId), 2000);
            } else {
                document.getElementById(inputElementId).value = data.text;
            }
        });
}

// Evento para enviar mensagem ao clicar no botão
document.getElementById('send-button').addEventListener('click', sendMessage);

// Envia a mensagem ao pressionar Enter
userInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Abre o input de arquivo, se necessário
function openFileInput(data) {
    const ending = "imagem";
    // Verifica se a mensagem ou o estado do diálogo termina com "imagem"
    if (data.message && (data.message.slice(-ending.length) === ending || data.dialogState.slice(-ending.length) === ending)) {
        document.getElementById('recordingIndicator').style.display = 'block'; // Exibe o ícone de gravação
    } else {
        document.getElementById('recordingIndicator').style.display = 'none'; // Oculta se não necessário
    }
}

// Evento para enviar mensagem ao alterar o input de arquivo
fileInput.addEventListener('change', sendMessage);