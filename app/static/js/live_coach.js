(function () {
  'use strict';

  var conversationId = null;

  function appendMessage(role, text) {
    var box = document.getElementById('coachChatMessages');
    if (!box) return;
    var div = document.createElement('div');
    div.className = 'coach-chat-panel__msg coach-chat-panel__msg--' + role;
    div.textContent = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
  }

  function setNotice(text, show) {
    var el = document.getElementById('coachChatNotice');
    if (!el) return;
    if (show) {
      el.textContent = text;
      el.classList.remove('d-none');
    } else {
      el.classList.add('d-none');
    }
  }

  var form = document.getElementById('coachChatForm');
  var input = document.getElementById('coachChatInput');
  if (form && input) {
    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      var msg = input.value.trim();
      if (!msg) return;
      input.value = '';
      input.disabled = true;
      appendMessage('user', msg);
      setNotice('Pensando…', true);

      try {
        var res = await fetch('/api/coach/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: msg,
            conversation_id: conversationId,
            screen_context: document.body.dataset.screen || 'dashboard',
          }),
        });
        var j = await res.json();
        if (j.ok) {
          conversationId = j.conversation_id;
          appendMessage('assistant', j.reply);
          if (j.used_fallback) {
            setNotice('Modo reglas (IA externa no disponible)', true);
          } else {
            setNotice('', false);
          }
        } else {
          appendMessage('assistant', j.error || 'Error al procesar');
          setNotice('', false);
        }
      } catch (err) {
        appendMessage('assistant', 'Error de conexión. Intenta de nuevo.');
        setNotice('', false);
      }
      input.disabled = false;
      input.focus();
    });
  }

  document.querySelectorAll('[data-coach-action]').forEach(function (el) {
    el.addEventListener('click', async function (e) {
      var action = el.dataset.coachAction;
      var activityId = el.dataset.activityId;
      if (action === 'start' && activityId) {
        e.preventDefault();
        await fetch('/coach/activity/' + activityId + '/start', {
          method: 'POST',
          headers: { 'X-Requested-With': 'XMLHttpRequest' },
        });
        window.location.href = '/coach/activity/' + activityId;
      }
      if (action === 'pause' && activityId) {
        e.preventDefault();
        await fetch('/coach/activity/' + activityId + '/pause', {
          method: 'POST',
          headers: { 'X-Requested-With': 'XMLHttpRequest' },
        });
        window.location.reload();
      }
      if (action === 'water') {
        e.preventDefault();
        await fetch('/coach/water', { method: 'POST' });
        el.textContent = '¡Registrado!';
        el.disabled = true;
      }
    });
  });
})();
