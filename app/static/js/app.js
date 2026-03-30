/**
 * ConectaTalentos - Utilitários de UI
 */

// Auto-inicializa toasts do Bootstrap
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.toast').forEach(el => {
        new bootstrap.Toast(el).show();
    });
});

/**
 * Exibe um toast programaticamente.
 * @param {string} message - Mensagem a exibir
 * @param {'success'|'danger'|'warning'|'info'} level - Nível de severidade
 * @param {number} delay - Tempo em ms antes de fechar (padrão: 5000)
 */
function showToast(message, level = 'info', delay = 5000) {
    const icons = {
        success: 'bi-check-circle',
        danger: 'bi-x-circle',
        warning: 'bi-exclamation-triangle',
        info: 'bi-info-circle',
    };

    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-bg-${level} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="bi ${icons[level] || icons.info} me-2"></i>${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto"
                data-bs-dismiss="toast" aria-label="Fechar"></button>
        </div>`;

    document.getElementById('toast-container').appendChild(toast);
    new bootstrap.Toast(toast, { delay }).show();
    toast.addEventListener('hidden.bs.toast', () => toast.remove());
}

/**
 * Ativa spinner e desabilita botão de submit em um formulário.
 * @param {HTMLFormElement} form
 * @param {string} spinnerId - ID do elemento spinner
 * @param {string} btnId - ID do botão de submit
 */
function activateFormLoading(form, spinnerId, btnId) {
    form.addEventListener('submit', function (e) {
        if (!this.checkValidity()) {
            e.preventDefault();
            this.classList.add('was-validated');
            return;
        }
        const spinner = document.getElementById(spinnerId);
        const btn = document.getElementById(btnId);
        if (spinner) spinner.classList.remove('d-none');
        if (btn) btn.disabled = true;
    });
}
