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
  });
  