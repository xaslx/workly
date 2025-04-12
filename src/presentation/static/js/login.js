document.addEventListener('DOMContentLoaded', function() {
    const telegramIdGroup = document.getElementById('telegram_id_group');
    const codeGroup = document.getElementById('code_group');
    const initialInstructions = document.getElementById('initial_instructions');
    const codeInstruction = document.getElementById('code_instruction');
    const actionButton = document.getElementById('action_button');
    const telegramIdInput = document.getElementById('telegram_id');
    const codeInput = document.getElementById('confirmation_code');
    const loginForm = document.getElementById('loginForm');
    
    const telegramIdError = document.getElementById('telegram_id_error');
    const codeError = document.getElementById('code_error');
    const telegramIdHint = document.getElementById('telegram_id_hint');
    const lastTelegramIdSpan = document.getElementById('last_telegram_id');
    
    let currentTelegramId = null;
    let isProcessing = false;
    let loginCompleted = false;

    const lastTelegramId = localStorage.getItem('telegram_id');

    if (lastTelegramId) {
        lastTelegramIdSpan.textContent = lastTelegramId;
        telegramIdHint.style.display = 'block';
    }

    telegramIdHint.addEventListener('click', function() {
        telegramIdInput.value = lastTelegramId;
        telegramIdInput.focus();
    });

    function setErrorTimeout(errorElement) {
        if (errorElement.textContent) {
            setTimeout(() => {
                errorElement.textContent = '';
                errorElement.style.display = 'none';
            }, 3000);
        }
    }

    const beforeUnloadHandler = function(e) {
        if (currentTelegramId && !loginCompleted) {
            e.preventDefault();
            return 'Вы уверены? Введенный код подтверждения будет потерян.';
        }
    };

    window.addEventListener('beforeunload', beforeUnloadHandler);

    actionButton.addEventListener('click', async function() {
        if (isProcessing) return;
        isProcessing = true;
        
        try {
            if (!currentTelegramId) {
                const telegramId = telegramIdInput.value.trim();

                if (!telegramId) {
                    showError(telegramIdError, 'Пожалуйста, введите ваш Telegram ID');
                    isProcessing = false;
                    return;
                }
                
                if (!/^\d+$/.test(telegramId)) {
                    showError(telegramIdError, 'Telegram ID должен содержать только цифры');
                    isProcessing = false;
                    return;
                }
                
                localStorage.setItem('telegram_id', telegramId);
                const response = await fetch('/auth/send-code', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        telegram_id: telegramId,
                        auth_type: 'LOGIN'
                    })
                });
                
                if (response.ok) {
                    currentTelegramId = telegramId;
                    switchToCodeStage();
                } else {
                    const errorData = await response.json();
                    showError(telegramIdError, errorData.detail || 'Ошибка при отправке кода');
                }
            } else {
                const code = codeInput.value.trim();
                
                if (!code) {
                    showError(codeError, 'Пожалуйста, введите код подтверждения');
                    isProcessing = false;
                    return;
                }

                if (!/^\d+$/.test(code)) {
                    showError(codeError, 'Код подтверждения должен содержать только цифры');
                    isProcessing = false;
                    return;
                }
                
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        telegram_id: currentTelegramId,
                        confirmation_code: code
                    })
                });
                
                if (response.ok) {
                    loginCompleted = true;
                    window.removeEventListener('beforeunload', beforeUnloadHandler);
                    
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 500);
                } else {
                    const errorData = await response.json();
                    showError(codeError, errorData.detail || 'Неверный код подтверждения');
                }
            }
        } catch (error) {
            console.error('Error:', error);
            showError(telegramIdError, 'Произошла ошибка при обработке запроса');
        } finally {
            isProcessing = false;
        }
    });

    function switchToCodeStage() {
        telegramIdGroup.style.display = 'none';
        initialInstructions.style.display = 'none';
        codeGroup.style.display = 'block';
        codeInstruction.style.display = 'block';
        actionButton.textContent = 'Войти';
        codeInput.focus();
    }

    function showError(errorElement, message) {
        errorElement.textContent = message;
        errorElement.style.color = 'red';
        errorElement.style.display = 'block';
    }

    telegramIdInput.addEventListener('input', function() {
        clearError(telegramIdError);
    });
    
    codeInput.addEventListener('input', function() {
        clearError(codeError);
    });

    function clearError(errorElement) {
        if (errorElement) {
            errorElement.textContent = '';
            errorElement.style.display = 'none';
        }
    }

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        actionButton.click();
    });
});