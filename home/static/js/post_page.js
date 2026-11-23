document.addEventListener('DOMContentLoaded', function () {
  const commentForm = document.getElementById('yt-comment-form');
  const commentTextarea = document.getElementById('id_comment');
  const commentSubmitBtn = document.getElementById('comment-submit-btn');

  commentTextarea.addEventListener('input', function () {
    if (commentTextarea.value.trim().length > 0) {
      commentSubmitBtn.style.display = 'block';
    }else{
      commentSubmitBtn.style.display = 'none';
    }
  });

  commentTextarea.addEventListener('blur', function () {
    if (commentTextarea.value.trim().length === 0) {
      commentSubmitBtn.style.display = 'none';
    }
  });

  commentForm.addEventListener('submit', function (event) {
    event.preventDefault();

    // Собираем все данные из нашей формы
    const formData = new FormData(commentForm);
    formData.set('next', window.location.pathname);
    formData.set('post', 'send');
    const apiUrl = '/comments/api/comment/';

    // Отправляем AJAX запрос на бэкенд Django-comments
    fetch('/comments/api/comment/', {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
      .then(response => {
        if (response.status === 201 || response.ok) {
          commentTextarea.value = ''; // Очищаем поле
          commentTextarea.style.height = 'auto'; // Сбрасываем высоту
          commentSubmitBtn.style.visibility = 'hidden';
          window.location.reload();
        } else {
          return response.json().then(err => {
            console.error('Детали ошибки бэкенда:', err);
            alert('Ошибка сервера: ' + JSON.stringify(err));
          });
        }
      })
      .catch(error => {
        alert('Ошибка:', error);
      });
  });

  const counterSpan = document.getElementById('total-participants');
  if (counterSpan) {
    const pageId = counterSpan.dataset.pageId;
    async function updateParticipantsCount() {
      try {
        const response = await fetch(`/home/get_participants_count/${pageId}/`);
        if (response.ok) {
          const data = await response.json();
          if (counterSpan.textContent !== String(data.count)) {
            counterSpan.textContent = data.count;
          }
        }
      } catch (error) {
        console.error('Ошибка при обновлении счетчика:', error);
      }
    }
    setInterval(updateParticipantsCount, 60000);
  }

  const additionalInfoBtn = document.getElementById('additional-info-btn');
  if (additionalInfoBtn) {
    additionalInfoBtn.addEventListener('click', function () {
      const additionalInfoSection = document.getElementById('additional-info-section');
      additionalInfoSection.classList.toggle('hidden');
      if (additionalInfoSection.classList.contains('hidden')) {
        additionalInfoBtn.textContent = 'Дополнительная информация';
      } else {
        additionalInfoBtn.textContent = 'Скрыть доп. информацию';
        additionalInfoBtn.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

});

function autoResize(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
}