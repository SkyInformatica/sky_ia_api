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

        this.currentJsonData = null;
        this.currentModel = 'qualificacao';

        this.initEventListeners();
    }

    initEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.downloadBtn.addEventListener('click', () => this.downloadJson());

        // Atualizar modelo selecionado
        document.querySelectorAll('input[name="modelo"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.currentModel = e.target.value;
            });
        });
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

        try {
            const formData = new FormData();
            formData.append('openai_api_key', apiKey);

            Array.from(files).forEach(file => {
                formData.append('files', file);
            });

            const endpoint = `/${this.currentModel}/upload`;
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Erro na requisição');
            }

            const data = await response.json();
            this.processResponse(data);

        } catch (error) {
            console.error('Erro:', error);
            this.showAlert(`Erro: ${error.message}`, 'danger');
        } finally {
            this.setLoading(false);
        }
    }

    processResponse(data) {
        const resposta = data.resposta;

        // Extrair e remover o markdown
        const markdown = resposta.resposta_processamento_markdown || '';
        delete resposta.resposta_processamento_markdown;

        // Renderizar markdown
        if (markdown) {
            this.markdownContent.innerHTML = marked.parse(markdown);
        } else {
            this.markdownContent.innerHTML = '<em>Nenhum resumo disponível</em>';
        }

        // Renderizar JSON
        this.currentJsonData = resposta;
        this.jsonContent.textContent = JSON.stringify(resposta, null, 2);
        Prism.highlightElement(this.jsonContent);

        this.showResults();
        this.showAlert('Processamento concluído com sucesso!', 'success');
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
