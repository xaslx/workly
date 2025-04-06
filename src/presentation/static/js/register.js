document.addEventListener('DOMContentLoaded', function() {
    const actionButton = document.getElementById('action_button');
    const telegramIdGroup = document.getElementById('telegram_id_group');
    const telegramIdInput = document.getElementById('telegram_id');
    const codeGroup = document.getElementById('code_group');
    const confirmationCodeInput = document.getElementById('confirmation_code');
    const registerDataGroup = document.getElementById('register_data_group');
    const usernameInput = document.getElementById('username');
    const nameInput = document.getElementById('name');
    const initialInstructions = document.getElementById('initial_instructions');
    const codeInstruction = document.getElementById('code_instruction');
    const registerInstruction = document.getElementById('register_instruction');
    
    const telegramIdError = document.getElementById('telegram_id_error');
    const codeError = document.getElementById('code_error');
    const usernameError = document.getElementById('username_error');
    const nameError = document.getElementById('name_error');
    
    let currentStep = 1;
    let isProcessing = false;
    let registrationCompleted = false;

    function setErrorTimeout(errorElement) {
        if (errorElement.textContent) {
            setTimeout(() => {
                errorElement.textContent = '';
            }, 3000);
        }
    }

    const beforeUnloadHandler = function(e) {
        if (currentStep > 1 && !registrationCompleted) {
            e.preventDefault();
            return 'Вы уверены? Все введенные данные могут быть потеряны.';
        }
    };

    window.addEventListener('beforeunload', beforeUnloadHandler);

    function updateUIForStep(step) {
        telegramIdGroup.style.display = 'none';
        codeGroup.style.display = 'none';
        registerDataGroup.style.display = 'none';
        initialInstructions.style.display = 'none';
        codeInstruction.style.display = 'none';
        registerInstruction.style.display = 'none';

        if (step === 1) {
            initialInstructions.style.display = 'block';
            telegramIdGroup.style.display = 'block';
            actionButton.textContent = 'Отправить код';
        } else if (step === 2) {
            codeInstruction.style.display = 'block';
            codeGroup.style.display = 'block';
            actionButton.textContent = 'Подтвердить код';
        } else if (step === 3) {
            registerInstruction.style.display = 'block';
            registerDataGroup.style.display = 'block';
            actionButton.textContent = 'Зарегистрироваться';
        }
    }
    
    const notyf = new Notyf();

    actionButton.addEventListener('click', async function() {
        if (isProcessing) return;
        isProcessing = true;
        
        try {
            if (currentStep === 1) {
                const telegramId = telegramIdInput.value.trim();
                
                if (!telegramId) {
                    telegramIdError.textContent = 'Пожалуйста, введите ваш Telegram ID';
                    setErrorTimeout(telegramIdError);
                    isProcessing = false;
                    return;
                }
                
                if (!/^\d+$/.test(telegramId)) {
                    telegramIdError.textContent = 'Telegram ID должен содержать только цифры';
                    setErrorTimeout(telegramIdError);
                    isProcessing = false;
                    return;
                }
                
                const response = await fetch('/auth/send-code', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({telegram_id: telegramId})
                });
                
                if (response.ok) {
                    currentStep = 2;
                    updateUIForStep(2);
                    telegramIdError.textContent = '';
                } else if (response.status === 409) {
                    const errorData = await response.json();
                    telegramIdError.textContent = errorData.detail || 'Этот Telegram ID уже зарегистрирован';
                    setErrorTimeout(telegramIdError);
                } else {
                    const errorData = await response.json();
                    telegramIdError.textContent = errorData.detail || 'Ошибка при отправке кода';
                    setErrorTimeout(telegramIdError);
                }
            } else if (currentStep === 2) {
                const code = confirmationCodeInput.value.trim();
                const telegramId = telegramIdInput.value.trim();
                
                if (!code) {
                    codeError.textContent = 'Пожалуйста, введите код подтверждения';
                    setErrorTimeout(codeError);
                    isProcessing = false;
                    return;
                }
                
                const response = await fetch('/auth/verify-code', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        telegram_id: telegramId,
                        confirmation_code: code
                    })
                });
                
                if (response.ok) {
                    const result = await response.json();
                    if (result !== null && result !== undefined) {
                        currentStep = 3;
                        updateUIForStep(3);
                        codeError.textContent = '';
                    } else {
                        codeError.textContent = 'Неверный код подтверждения';
                        setErrorTimeout(codeError);
                    }
                } else {
                    const errorData = await response.json();
                    codeError.textContent = errorData.detail || 'Ошибка при проверке кода';
                    setErrorTimeout(codeError);
                }
            } else if (currentStep === 3) {
                const username = usernameInput.value.trim();
                const name = nameInput.value.trim();
                const telegramId = telegramIdInput.value.trim();
                
                if (!username) {
                    usernameError.textContent = 'Пожалуйста, придумайте логин';
                    setErrorTimeout(usernameError);
                    isProcessing = false;
                    return;
                }
                
                if (!name) {
                    nameError.textContent = 'Пожалуйста, введите ваше имя';
                    setErrorTimeout(nameError);
                    isProcessing = false;
                    return;
                }
                
                const response = await fetch('/auth/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        telegram_id: telegramId,
                        username: username,
                        name: name
                    })
                });
                
                if (response.ok) {
                    registrationCompleted = true;
                    window.removeEventListener('beforeunload', beforeUnloadHandler);
                    
                    notyf.success('Регистрация успешна! Теперь можно войти.');
                    
                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 3000);
                } else {
                    const errorData = await response.json();
                    if (errorData.detail.includes('username')) {
                        usernameError.textContent = errorData.detail;
                        setErrorTimeout(usernameError);
                    } else {
                        nameError.textContent = errorData.detail || 'Ошибка при регистрации';
                        setErrorTimeout(nameError);
                    }
                }
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            isProcessing = false;
        }
    });

    updateUIForStep(1);
});
