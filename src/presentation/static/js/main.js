document.addEventListener('DOMContentLoaded', function() {
  const avatar = document.querySelector('.user-avatar');
  const dropdown = document.getElementById('userDropdown');
  const logoutButton = document.getElementById('logoutButton');

  if (avatar && dropdown) {
      avatar.addEventListener('click', function(e) {
          e.stopPropagation();
          dropdown.classList.toggle('show');
      });
  
      document.addEventListener('click', function(e) {
          if (!dropdown.contains(e.target)) {
              dropdown.classList.remove('show');
          }
      });
  }

  if (logoutButton) {
      logoutButton.addEventListener('click', function() {
          fetch('/auth/logout', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              credentials: 'include'
          })
          .then(response => {
              if (response.ok) {
                  window.location.href = '/';
              } else {
                  console.error('Ошибка при выходе');
              }
          })
          .catch(error => {
              console.error('Ошибка:', error);
          });
      });
  }


  const chatInput = document.querySelector('.chat-input');
  const sendButton = document.querySelector('.send-button');
  const chatMessages = document.querySelector('.chat-messages');
  const currentUsername = document.querySelector('.username')?.textContent || 'Anonymous';


  const socketProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
  const socketUrl = socketProtocol + window.location.host + '/ws/chat';
  const socket = new WebSocket(socketUrl);

  socket.onopen = function() {
      console.log("WebSocket подключен.");
      addSystemMessage("Вы подключены к чату");
      loadInitialMessages();
  };

  socket.onmessage = function(event) {
      try {
          const message = JSON.parse(event.data);
          renderMessage(message);
      } catch (error) {
          console.error('Ошибка парсинга сообщения:', error);
      }
  };

  socket.onclose = function(event) {
      console.log('WebSocket закрыт:', event);
      addSystemMessage("Соединение с чатом потеряно. Попробуйте перезагрузить страницу.");
  };

  socket.onerror = function(error) {
      console.log('Ошибка WebSocket:', error);
      addSystemMessage("Ошибка соединения с чатом");
  };


  async function sendMessage() {
      const messageText = chatInput.value.trim();
      if (!messageText) return;

      try {
 
          const response = await fetch('/chat/messages', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                text: messageText,
                username: currentUsername,
                created_at: new Date().toISOString()
            }),
          });

          if (!response.ok) {
              throw new Error('Ошибка сохранения сообщения');
          }

          chatInput.value = '';
      } catch (error) {
          console.error('Ошибка:', error);
          addSystemMessage('Не удалось отправить сообщение');
      }
  }


  function renderMessage(message) {
      const messageElement = document.createElement('div');
      const isCurrentUser = message.username === currentUsername;
      const messageClass = isCurrentUser ? 'message my-message' : 'message';
      
      const time = new Date(message.created_at || new Date());
      const timeString = time.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
      
      messageElement.className = messageClass;
      messageElement.innerHTML = `
          <div class="message-meta">
              <span class="message-username">${message.username || 'Anonymous'}</span>
              <span class="message-time">${timeString}</span>
          </div>
          <div class="message-content">${message.text}</div>
      `;
      
      chatMessages.appendChild(messageElement);
      chatMessages.scrollTop = chatMessages.scrollHeight;
  }


  function addSystemMessage(text) {
      const messageElement = document.createElement('div');
      messageElement.className = 'system-message';
      messageElement.textContent = text;
      chatMessages.appendChild(messageElement);
      chatMessages.scrollTop = chatMessages.scrollHeight;
  }


  async function loadInitialMessages() {
      try {
          const response = await fetch('/chat/messages', {
              credentials: 'include'
          });
          const messages = await response.json();
          messages.forEach(renderMessage);
      } catch (error) {
          console.error('Ошибка загрузки сообщений:', error);
      }
  }


  sendButton.addEventListener('click', sendMessage);

  chatInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
          sendMessage();
      }
  });


  if (chatInput) {
      chatInput.focus();
  }
});