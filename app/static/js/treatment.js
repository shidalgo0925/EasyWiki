(function () {
  'use strict';

  var root = document.getElementById('wizardTreatment');
  if (!root) return;

  var step = 1;
  var total = 7;
  var profileId = root.dataset.profileId ? parseInt(root.dataset.profileId, 10) : null;

  var initial = {};
  var prefill = {};
  try { initial = JSON.parse(root.dataset.initial || '{}'); } catch (e) { initial = {}; }
  try { prefill = JSON.parse(root.dataset.prefill || '{}'); } catch (e) { prefill = {}; }

  var btnBack = document.getElementById('treatmentBtnBack');
  var btnNext = document.getElementById('treatmentBtnNext');
  var progress = document.getElementById('treatmentProgress');
  var btnActivate = document.getElementById('btnActivate');
  var btnSaveDraft = document.getElementById('btnSaveDraft');
  var msgEl = document.getElementById('treatmentMsg');

  function el(id) { return document.getElementById(id); }

  function showStep(n) {
    for (var i = 1; i <= total; i++) {
      var s = el('tStep' + i);
      if (s) s.classList.toggle('d-none', i !== n);
    }
    btnBack.disabled = (n === 1);
    btnNext.classList.toggle('d-none', n === total);
    progress.style.width = Math.round((n / total) * 100) + '%';
    progress.textContent = 'Paso ' + n + '/' + total;
    if (n === total) renderSummary();
  }

  function getObstacles() {
    var list = [];
    document.querySelectorAll('.obstacle-check:checked').forEach(function (cb) {
      list.push(cb.value);
    });
    var other = el('obstaclesOther').value.trim();
    if (other) list.push('otro: ' + other);
    return list;
  }

  function getRoutine() {
    return {
      start_time: el('routineStart').value,
      hours_available: parseInt(el('routineHours').value, 10) || 6,
      work_blocks: el('routineBlocks').value.trim(),
      best_days: el('routineBestDays').value.trim(),
      habits: el('routineHabits').value.trim(),
    };
  }

  function getPreferences() {
    var prefs = {};
    document.querySelectorAll('.pref-check').forEach(function (cb) {
      prefs[cb.value] = cb.checked;
    });
    return prefs;
  }

  function getCommitment() {
    var sel = document.querySelector('.commitment-radio:checked');
    return sel ? sel.value : '';
  }

  function collectData() {
    return {
      profile_id: profileId,
      wizard_step: step,
      current_situation: el('currentSituation').value.trim(),
      main_problem: el('mainProblem').value.trim(),
      primary_area: el('primaryArea').value,
      goal_30_days: el('goal30').value.trim(),
      goal_90_days: el('goal90').value.trim(),
      success_definition: el('successDefinition').value.trim(),
      obstacles: getObstacles(),
      current_routine: getRoutine(),
      commitment_level: getCommitment(),
      coaching_preferences: getPreferences(),
    };
  }

  function renderSummary() {
    var d = collectData();
    var lines = [
      'Situación: ' + (d.current_situation || '—'),
      'Problema: ' + (d.main_problem || '—'),
      'Área: ' + (d.primary_area || '—'),
      'Meta 30d: ' + (d.goal_30_days || '—'),
      'Meta 90d: ' + (d.goal_90_days || '—'),
      'Éxito: ' + (d.success_definition || '—'),
      'Obstáculos: ' + (d.obstacles.length ? d.obstacles.join(', ') : '—'),
      'Compromiso: ' + (d.commitment_level || '—'),
      'Rutina: ' + JSON.stringify(d.current_routine, null, 2),
      'Preferencias: ' + JSON.stringify(d.coaching_preferences, null, 2),
    ];
    el('treatmentSummary').textContent = lines.join('\n\n');
  }

  async function saveDraft(silent) {
    var res = await fetch('/api/treatment/save-draft', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(collectData()),
    });
    var j = await res.json();
    if (j.ok) {
      profileId = j.profile_id;
      root.dataset.profileId = profileId;
      if (!silent) msgEl.textContent = 'Borrador guardado ✅';
    } else if (!silent) {
      msgEl.textContent = 'Error al guardar borrador';
    }
    return j;
  }

  async function activate(replace) {
    await saveDraft(true);
    if (!profileId) {
      msgEl.textContent = 'Error: no hay borrador';
      return;
    }
    var res = await fetch('/api/treatment/activate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ profile_id: profileId, replace: replace }),
    });
    var j = await res.json();
    if (j.ok) {
      msgEl.textContent = 'Tratamiento activado ✅ Redirigiendo...';
      setTimeout(function () { window.location.href = '/'; }, 1200);
      return;
    }
    if (j.error === 'ACTIVE_EXISTS') {
      if (confirm('Ya tienes un tratamiento activo. ¿Deseas reemplazarlo? El anterior quedará archivado.')) {
        await activate(true);
      }
      return;
    }
    msgEl.textContent = 'Error: ' + (j.error || 'desconocido');
  }

  function loadInitial() {
    if (!initial || !initial.id) {
      if (prefill.last_blocker) {
        el('obstaclesOther').placeholder = 'Sugerido: ' + prefill.last_blocker;
      }
      if (prefill.decisions && prefill.decisions.length) {
        el('mainProblem').placeholder = 'Decisiones pendientes: ' + prefill.decisions.join('; ');
      }
      return;
    }
    step = initial.wizard_step || 1;
    el('currentSituation').value = initial.current_situation || '';
    el('mainProblem').value = initial.main_problem || '';
    el('primaryArea').value = initial.primary_area || '';
    el('goal30').value = initial.goal_30_days || '';
    el('goal90').value = initial.goal_90_days || '';
    el('successDefinition').value = initial.success_definition || '';
    if (initial.obstacles) {
      initial.obstacles.forEach(function (o) {
        if (o.indexOf('otro:') === 0) {
          el('obstaclesOther').value = o.replace('otro:', '').trim();
        } else {
          var cb = document.querySelector('.obstacle-check[value="' + o + '"]');
          if (cb) cb.checked = true;
        }
      });
    }
    var r = initial.current_routine || {};
    if (r.start_time) el('routineStart').value = r.start_time;
    if (r.hours_available) el('routineHours').value = r.hours_available;
    if (r.work_blocks) el('routineBlocks').value = r.work_blocks;
    if (r.best_days) el('routineBestDays').value = r.best_days;
    if (r.habits) el('routineHabits').value = r.habits;
    if (initial.commitment_level) {
      var radio = document.querySelector('.commitment-radio[value="' + initial.commitment_level + '"]');
      if (radio) radio.checked = true;
    }
    var prefs = initial.coaching_preferences || {};
    Object.keys(prefs).forEach(function (k) {
      var p = document.querySelector('.pref-check[value="' + k + '"]');
      if (p) p.checked = !!prefs[k];
    });
    syncCards();
  }

  function syncCards() {
    document.querySelectorAll('.coach-option-card').forEach(function (card) {
      var cb = card.querySelector('input[type="checkbox"]');
      var rb = card.querySelector('input[type="radio"]');
      if (cb) card.classList.toggle('is-selected', cb.checked);
      if (rb) card.classList.toggle('is-selected', rb.checked);
    });
  }

  document.querySelectorAll('.coach-option-card').forEach(function (card) {
    card.addEventListener('click', function (e) {
      var cb = card.querySelector('input[type="checkbox"]');
      var rb = card.querySelector('input[type="radio"]');
      if (cb && e.target !== cb) {
        cb.checked = !cb.checked;
      }
      if (rb && e.target !== rb) {
        rb.checked = true;
      }
      syncCards();
    });
    var cb = card.querySelector('input');
    if (cb) cb.addEventListener('change', syncCards);
  });

  btnBack.addEventListener('click', async function () {
    if (step > 1) {
      await saveDraft(true);
      step--;
      showStep(step);
    }
  });

  btnNext.addEventListener('click', async function () {
    await saveDraft(true);
    if (step < total) {
      step++;
      showStep(step);
    }
  });

  btnSaveDraft.addEventListener('click', function () { saveDraft(false); });
  btnActivate.addEventListener('click', function () { activate(false); });

  loadInitial();
  showStep(step);
})();
