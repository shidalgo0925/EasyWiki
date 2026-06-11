(function () {
  'use strict';

  /* --- Floating Coach IA panel --- */
  function initFloatingCoach() {
    var btn = document.getElementById('coachFloatingBtn');
    var panel = document.getElementById('coachChatPanel');
    if (!btn || !panel) return;

    btn.addEventListener('click', function () {
      panel.classList.toggle('is-open');
    });

    document.addEventListener('click', function (e) {
      if (!panel.classList.contains('is-open')) return;
      if (panel.contains(e.target) || btn.contains(e.target)) return;
      panel.classList.remove('is-open');
    });
  }

  /* --- Wizard option cards ↔ checkboxes --- */
  function initOptionCards() {
    document.querySelectorAll('.coach-option-card').forEach(function (card) {
      var input = card.querySelector('input[type="checkbox"]');
      if (!input) return;

      function sync() {
        card.classList.toggle('is-selected', input.checked);
      }

      card.addEventListener('click', function () {
        input.checked = !input.checked;
        sync();
      });

      sync();
    });
  }

  /* --- Wizard step navigation (only on /wizard/ai-plan) --- */
  function initWizard() {
    var btnBack = document.getElementById('btnBack');
    var btnNext = document.getElementById('btnNext');
    var btnCommit = document.getElementById('btnCommit');
    var wizProgress = document.getElementById('wizProgress');
    if (!btnNext || !wizProgress || !document.getElementById('wizardAiPlan')) return;

    var step = 1;
    var total = 7;

    function el(id) { return document.getElementById(id); }

    function showStep(n) {
      for (var i = 1; i <= total; i++) {
        var s = el('step' + i);
        if (s) s.classList.toggle('d-none', i !== n);
      }
      btnBack.disabled = (n === 1);
      btnNext.textContent = (n === total) ? 'Finalizar' : 'Siguiente';
      wizProgress.style.width = Math.round((n / total) * 100) + '%';
      wizProgress.textContent = 'Paso ' + n + '/' + total;
    }

    btnBack.addEventListener('click', function () {
      if (step > 1) { step--; showStep(step); }
    });

    btnNext.addEventListener('click', async function () {
      if (step === 3) {
        var metas_crudas = el('metasCrudas').value;
        var restricciones = {};
        try { restricciones = JSON.parse(el('restricciones').value || '{}'); } catch (e) { restricciones = {}; }
        var horizonte = el('horizonte').value;
        var res = await fetch('/api/ai/plan/suggest', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ metas_crudas: metas_crudas, restricciones: restricciones, horizonte: horizonte })
        });
        var j = await res.json();
        window.__draft = j.draft || {};
        el('smartPreview').textContent = JSON.stringify(window.__draft.metas_smart || [], null, 2);
      }
      if (step === 4) {
        el('breakdownPreview').textContent = JSON.stringify({
          rocas: window.__draft.rocas_semanales || [],
          microacciones: window.__draft.microacciones || {}
        }, null, 2);
      }
      if (step === 5) {
        el('calendarPreview').textContent = JSON.stringify(window.__draft.microacciones || {}, null, 2);
        el('finalPreview').textContent = JSON.stringify(window.__draft || {}, null, 2);
      }
      if (step < total) { step++; showStep(step); }
    });

    if (btnCommit) {
      btnCommit.addEventListener('click', async function () {
        var res = await fetch('/api/ai/plan/commit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ draft: window.__draft, user_id: 1 })
        });
        var j = await res.json();
        el('commitMsg').textContent = j.ok ? 'Guardado ✅' : 'Error al guardar';
      });
    }

    showStep(step);
  }

  document.addEventListener('DOMContentLoaded', function () {
    initFloatingCoach();
    initOptionCards();
    initWizard();
  });
})();
