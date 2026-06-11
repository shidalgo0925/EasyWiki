(function () {
  'use strict';

  var S = window.AI_SETTINGS;
  if (!S) return;

  var providerEl = document.getElementById('api_provider');
  var baseUrlField = document.getElementById('baseUrlField');
  var useCustomEl = document.getElementById('use_custom_base_url');
  var baseUrlEl = document.getElementById('base_url');
  var modelEl = document.getElementById('model');
  var modelList = document.getElementById('modelList');
  var hintEl = document.getElementById('providerHint');
  var warnEl = document.getElementById('providerWarning');
  var apiKeyHint = document.getElementById('apiKeyHint');

  function syncProvider() {
    var p = providerEl.value;
    var meta = S.providers[p] || {};
    if (!useCustomEl.checked && meta.base_url) {
      baseUrlEl.value = meta.base_url;
    }
    if (hintEl) hintEl.textContent = meta.hint || '';
    if (warnEl) {
      warnEl.textContent = p === 'ollama' ? 'Does not support MCP and Focus Chain' : '';
    }
    if (apiKeyHint) {
      apiKeyHint.textContent = p === 'ollama'
        ? 'Optional API key for authenticated Ollama instances or cloud services. Leave empty for local installations.'
        : 'API key for ' + p + '. Leave empty to use .env fallback.';
    }
    baseUrlField.classList.toggle('is-hidden', p === 'rules');
    useCustomEl.closest('.settings-field').classList.toggle('is-hidden', p === 'rules');
    loadModelSuggestions(p);
  }

  function loadModelSuggestions(provider) {
    if (!modelList) return;
    modelList.innerHTML = '';
    (S.modelSuggestions[provider] || []).forEach(function (m) {
      var opt = document.createElement('option');
      opt.value = m;
      modelList.appendChild(opt);
    });
  }

  async function fetchOllamaModels() {
    var base = baseUrlEl.value.replace(/\/$/, '');
    if (!base) return;
    var res = await fetch('/settings/ai/models?provider=ollama&base_url=' + encodeURIComponent(base));
    var j = await res.json();
    if (j.ok && j.models && j.models.length) {
      modelList.innerHTML = '';
      j.models.forEach(function (m) {
        var opt = document.createElement('option');
        opt.value = m;
        modelList.appendChild(opt);
      });
      if (!modelEl.value && j.models[0]) modelEl.value = j.models[0];
    }
  }

  providerEl.addEventListener('change', syncProvider);
  useCustomEl.addEventListener('change', function () {
    baseUrlField.classList.toggle('is-hidden', !useCustomEl.checked && providerEl.value === 'rules');
  });

  document.getElementById('btnLoadModels').addEventListener('click', fetchOllamaModels);

  document.getElementById('btnTestConnection').addEventListener('click', async function () {
    var resultEl = document.getElementById('testResult');
    resultEl.textContent = 'Probando…';
    resultEl.className = 'settings-test-result';
    var form = document.getElementById('aiConfigForm');
    var fd = new FormData(form);
    await fetch(form.action, { method: 'POST', body: fd });
    var res = await fetch('/settings/ai/test', { method: 'POST' });
    var j = await res.json();
    if (j.ok) {
      resultEl.textContent = '✓ Conexión OK — ' + (j.message || '').slice(0, 60);
      resultEl.className = 'settings-test-result is-ok';
    } else {
      resultEl.textContent = '✗ ' + (j.error || 'Error');
      resultEl.className = 'settings-test-result is-error';
    }
  });

  syncProvider();
})();
