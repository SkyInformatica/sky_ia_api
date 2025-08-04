// --- dicas sob os radios ---------------------------------------------------
function toggleHints() {
    const isQualificacao = document.getElementById('qualificacao').checked;
    document.getElementById('hint-qualificacao').classList.toggle('d-none', !isQualificacao);
    document.getElementById('hint-escritura').classList.toggle('d-none', isQualificacao);
}
// executa ao carregar a página
document.addEventListener('DOMContentLoaded', toggleHints);
// executa quando o usuário muda o radio
document.querySelectorAll('input[name="modelo"]').forEach(r =>
    r.addEventListener('change', toggleHints)
);

class SkAIApp {
    constructor() {
        this.form = document.getElementById('uploadForm');
        this.submitBtn = document.getElementById('submitBtn');
        this.submitText = document.getElementById('submitText');
        this.loadingSpinner = document.getElementById('loadingSpinner');
        this.results = document.getElementById('results');
        this.markdownContent = document.getElementById('markdownContent');
        this.jsonContent = document.getElementById('jsonContent');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.alertContainer = document.getElementById('alertContainer');
        this.processingTime = document.getElementById('processingTime');
        this.processingSeconds = document.getElementById('processingSeconds');
        this.processingMessage = document.getElementById('processingMessage');
        this.copyMarkdownBtn = document.getElementById('copyMarkdownBtn');
        this.currentMarkdown = ''; // Para armazenar o markdown original

        this.processingInterval = null;
        this.startTime = null;

        this.currentJsonData = null;
        this.currentModel = 'qualificacao';

        // Mensagens de processamento
        this.messages = [
            { time: 0, text: "Iniciando processamento..." },
            { time: 10, text: "Estamos identificando os documentos..." },
            { time: 20, text: "Ainda processando, muito conteúdo para analisar..." },
            { time: 30, text: "Parece demorado mas o resultado vai ser muito bom..." },
            { time: 40, text: "Finalizando a análise dos documentos..." },
            { time: 50, text: "Quase lá! Organizando as informações..." },
            { time: 60, text: "Um minuto se passou, continuamos trabalhando..." },
            { time: 70, text: "Processamento extenso, mas garantindo qualidade..." },
            { time: 80, text: "Extraindo informações importantes..." },
            { time: 90, text: "Análise em andamento, falta pouco..." },
            { time: 100, text: "Validando todos os dados extraídos..." },
            { time: 110, text: "Processamento minucioso em andamento..." },
            { time: 120, text: "Dois minutos se passaram, estamos quase lá..." },
            { time: 130, text: "Conferindo a precisão das informações..." },
            { time: 140, text: "Sua paciência resultará em dados mais precisos..." },
            { time: 150, text: "Finalizando os últimos detalhes..." },
            { time: 160, text: "Processamento em fase final..." },
            { time: 170, text: "Últimos ajustes sendo realizados..." },
            { time: 180, text: "Agradecemos sua paciência, estamos finalizando..." }
        ];

        this.initEventListeners();
    }

    initEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.downloadBtn.addEventListener('click', () => this.downloadJson());
        this.copyMarkdownBtn.addEventListener('click', () => this.copyMarkdown());

        // Atualizar modelo selecionado
        document.querySelectorAll('input[name="modelo"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.currentModel = e.target.value;
            });
        });
    }

    async copyMarkdown() {
        try {
            await navigator.clipboard.writeText(this.currentMarkdown);

            // Feedback visual temporário no botão
            const originalText = this.copyMarkdownBtn.innerHTML;
            this.copyMarkdownBtn.innerHTML = '✅ Copiado!';
            this.copyMarkdownBtn.disabled = true;

            setTimeout(() => {
                this.copyMarkdownBtn.innerHTML = originalText;
                this.copyMarkdownBtn.disabled = false;
            }, 2000);

        } catch (err) {
            console.error('Erro ao copiar:', err);
            this.showAlert('Erro ao copiar para área de transferência', 'danger');
        }
    }

    updateProcessingMessage(elapsedSeconds) {
        // Encontra a mensagem apropriada para o tempo atual
        let currentMessage = this.messages[0].text; // mensagem padrão

        for (let i = this.messages.length - 1; i >= 0; i--) {
            if (elapsedSeconds >= this.messages[i].time) {
                currentMessage = this.messages[i].text;
                break;
            }
        }

        // Atualiza o elemento com a mensagem
        if (this.processingMessage.textContent !== currentMessage) {
            this.processingMessage.style.opacity = '0';
            setTimeout(() => {
                this.processingMessage.textContent = currentMessage;
                this.processingMessage.style.opacity = '1';
            }, 200);
        }
    }

    startTimer() {
        this.startTime = Date.now();
        this.processingTime.classList.remove('d-none');
        this.processingSeconds.textContent = '0';
        this.processingMessage.style.transition = 'opacity 0.3s ease-in-out';

        this.processingInterval = setInterval(() => {
            const elapsedSeconds = Math.floor((Date.now() - this.startTime) / 1000);
            this.processingSeconds.textContent = elapsedSeconds;
            this.updateProcessingMessage(elapsedSeconds);
        }, 1000);
    }

    stopTimer() {
        if (this.processingInterval) {
            clearInterval(this.processingInterval);
            this.processingInterval = null;
        }

        if (this.startTime) {
            const finalTime = Math.floor((Date.now() - this.startTime) / 1000);
            this.processingSeconds.textContent = finalTime;
            this.processingMessage.textContent = "Processamento concluído!";
            this.startTime = null;
        }
    }

    async handleSubmit(e) {
        e.preventDefault();

        const apiKey = document.getElementById('apiKey').value;
        const files = document.getElementById('files').files;

        if (!apiKey || files.length === 0) {
            this.showAlert('Por favor, preencha todos os campos', 'warning');
            return;
        }

        this.setLoading(true);
        this.hideResults();
        this.startTimer();

        try {
            const formData = new FormData();
            formData.append('openai_api_key', apiKey);

            Array.from(files).forEach(file => {
                formData.append('files', file);
            });

            const endpoint = `/${this.currentModel}`;
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Erro na requisição');
            }

            let data;
            try {
                data = await response.json();
            } catch (err) {
                this.showAlert('Não foi possível interpretar a resposta da API', 'danger');
                return;
            }

            if (!data || typeof data !== 'object') {
                this.showAlert('Resposta vazia da API', 'warning');
                return;
            }

            this.processResponse(data);

        } catch (error) {
            console.error('Erro:', error);
            this.showAlert(`Erro: ${error.message}`, 'danger');
        } finally {
            this.setLoading(false);
            this.stopTimer();
        }
    }

    processResponse(resposta) {
        if (!resposta) {
            this.showAlert('Sem dados para exibir', 'warning');
            return;
        }

        let markdown = '';

        if (this.currentModel === 'escritura_publica') {
            markdown = resposta.resposta_processamento_markdown || '';
        } else if (resposta.resposta) {
            markdown = resposta.resposta.resposta_processamento_markdown || '';
        }

        this.currentMarkdown = markdown;

        // --- renderizações ---
        this.markdownContent.innerHTML = markdown
            ? marked.parse(markdown)
            : '<em>Nenhum resumo disponível</em>';

        this.currentJsonData = resposta;
        this.jsonContent.textContent = JSON.stringify(resposta, null, 2);
        Prism.highlightElement(this.jsonContent);

        this.showResults();
        this.showAlert('Processamento concluído com sucesso!', 'success');
    }


    hideResults() {
        this.results.classList.add('d-none');
        this.currentMarkdown = ''; // Limpa o markdown armazenado
    }

    downloadJson() {
        if (!this.currentJsonData) return;

        const blob = new Blob([JSON.stringify(this.currentJsonData, null, 2)], {
            type: 'application/json'
        });

        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.currentModel}_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    setLoading(loading) {
        this.submitBtn.disabled = loading;
        if (loading) {
            this.submitText.textContent = 'Processando...';
            this.loadingSpinner.classList.remove('d-none');
        } else {
            this.submitText.textContent = 'Processar Documentos';
            this.loadingSpinner.classList.add('d-none');
        }
    }

    showResults() {
        this.results.classList.remove('d-none');
        this.results.scrollIntoView({ behavior: 'smooth' });
    }

    hideResults() {
        this.results.classList.add('d-none');
    }

    showAlert(message, type) {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show mt-3" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        this.alertContainer.innerHTML = alertHtml;

        // Auto-remover após 5 segundos
        setTimeout(() => {
            const alert = this.alertContainer.querySelector('.alert');
            if (alert) alert.remove();
        }, 5000);
    }
}

// Inicializar a aplicação
document.addEventListener('DOMContentLoaded', () => {
    new SkAIApp();
});