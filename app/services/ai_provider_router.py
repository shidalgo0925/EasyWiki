# -*- coding: utf-8 -*-
"""Router de proveedores IA — soporta config por usuario (pantalla CLINE)."""
import os
import time
from typing import List, Dict, Optional

import config as app_config
from app.services.ai_types import AIResponse

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import requests
except ImportError:
    requests = None


class AIProviderRouter:
    def __init__(self, provider: str = None, model: str = None, user_config: dict = None):
        cfg = user_config or {}
        self.user_config = cfg
        self.provider = (provider or cfg.get("api_provider") or app_config.AI_PROVIDER or "rules").lower()
        self.model = model or cfg.get("model") or app_config.AI_MODEL or "gpt-4o-mini"
        self.context_window = int(cfg.get("context_window") or 4096)
        self.timeout_sec = int(cfg.get("request_timeout_ms") or 180000) / 1000.0
        self.use_compact_prompt = bool(cfg.get("use_compact_prompt"))
        self._api_key = cfg.get("_resolved_api_key", "")
        self._base_url = self._resolve_base_url(cfg)

    def _resolve_base_url(self, cfg: dict) -> str:
        if cfg.get("use_custom_base_url") and cfg.get("base_url"):
            return cfg["base_url"].rstrip("/")
        defaults = {
            "openai": "https://api.openai.com/v1",
            "kimi": os.environ.get("KIMI_BASE_URL", "https://api.moonshot.cn/v1"),
            "ollama": os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
        }
        return defaults.get(self.provider, "")

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> dict:
        if self.use_compact_prompt:
            messages = [m for m in messages if m["role"] != "system"][:6]
            messages.insert(0, {"role": "system", "content": "Eres EasyCoach. Responde breve en español."})

        handlers = {
            "openai": self._chat_openai_compatible,
            "kimi": self._chat_openai_compatible,
            "claude": self._chat_claude,
            "gemini": self._chat_gemini,
            "ollama": self._chat_ollama,
            "local": self._chat_rules_only,
            "rules": self._chat_rules_only,
        }
        handler = handlers.get(self.provider, self._chat_openai_compatible)
        try:
            content = handler(messages, temperature)
            if content:
                return {"content": content, "provider": self.provider, "model": self.model, "used_fallback": False}
        except Exception as exc:
            last_error = str(exc)
        else:
            last_error = "empty response"

        if self.provider not in ("openai", "rules", "local") and (self._api_key or app_config.OPENAI_API_KEY):
            try:
                content = self._chat_openai_compatible(messages, temperature, force_openai=True)
                if content:
                    return {"content": content, "provider": "openai", "model": app_config.AI_MODEL, "used_fallback": True}
            except Exception:
                pass
        raise RuntimeError(last_error)

    def _chat_openai_compatible(self, messages, temperature, force_openai=False):
        key = app_config.OPENAI_API_KEY if force_openai else (self._api_key or app_config.OPENAI_API_KEY)
        if not OpenAI or not key:
            raise RuntimeError("OpenAI-compatible no configurado")
        base = self._base_url if self._base_url and not force_openai else None
        client = OpenAI(api_key=key, base_url=base) if base else OpenAI(api_key=key)
        max_tokens = min(1200, self.context_window // 2)
        resp = client.chat.completions.create(
            model=self.model if not force_openai else app_config.AI_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=self.timeout_sec,
        )
        return resp.choices[0].message.content

    def _chat_claude(self, messages, temperature):
        key = self._api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        if not key or not requests:
            raise RuntimeError("Claude no configurado")
        system = "\n".join(m["content"] for m in messages if m["role"] == "system")
        user_msgs = [m for m in messages if m["role"] != "system"]
        payload = {
            "model": self.model,
            "max_tokens": min(1200, self.context_window // 2),
            "system": system,
            "messages": [{"role": m["role"], "content": m["content"]} for m in user_msgs if m["role"] in ("user", "assistant")],
        }
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json=payload,
            timeout=self.timeout_sec,
        )
        r.raise_for_status()
        return r.json()["content"][0]["text"]

    def _chat_gemini(self, messages, temperature):
        key = self._api_key or os.environ.get("GEMINI_API_KEY", "")
        if not key or not requests:
            raise RuntimeError("Gemini no configurado")
        text = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={key}"
        r = requests.post(url, json={"contents": [{"parts": [{"text": text}]}]}, timeout=self.timeout_sec)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]

    def _chat_ollama(self, messages, temperature):
        if not requests:
            raise RuntimeError("requests no disponible")
        base = self._base_url or "http://127.0.0.1:11434"
        headers = {}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        r = requests.post(
            f"{base}/v1/chat/completions",
            headers=headers,
            json={"model": self.model, "messages": messages, "temperature": temperature},
            timeout=self.timeout_sec,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    def _chat_rules_only(self, messages, temperature):
        raise RuntimeError("Modo rules — usar coach_fallback_rules")

    def generate(
        self,
        messages: List[Dict[str, str]],
        provider: str = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None,
        timeout: int = None,
    ) -> AIResponse:
        temperature = temperature if temperature is not None else app_config.AI_TEMPERATURE
        max_tokens = max_tokens or app_config.AI_MAX_TOKENS
        if timeout:
            self.timeout_sec = timeout

        providers_to_try = [provider or self.provider]
        if app_config.AI_FALLBACK_ENABLED:
            for p in app_config.AI_FALLBACK_PROVIDERS:
                p = p.strip().lower()
                if p and p not in providers_to_try:
                    providers_to_try.append(p)

        last_error = ""
        for prov in providers_to_try:
            if prov in ("rules", "local"):
                continue
            saved = self.provider
            self.provider = prov
            if model:
                self.model = model
            t0 = time.time()
            try:
                result = self.chat(messages, temperature=temperature)
                elapsed = int((time.time() - t0) * 1000)
                return AIResponse(
                    content=result["content"],
                    provider=result.get("provider", prov),
                    model=result.get("model", self.model),
                    latency_ms=elapsed,
                    used_fallback=result.get("used_fallback", False),
                )
            except Exception as e:
                last_error = str(e)
            finally:
                self.provider = saved

        return AIResponse(content="", provider="rules", model="fallback", error=last_error or "all providers failed")


def log_ai_call(user_id: int, response: AIResponse, source: str = "") -> None:
    from app.extensions import get_db
    from app.models.coach_ai_log import CoachAICallLog
    db = get_db()
    db.add(CoachAICallLog(
        user_id=user_id,
        provider=response.provider,
        model=response.model,
        latency_ms=response.latency_ms,
        tokens_input=response.tokens_input,
        tokens_output=response.tokens_output,
        source=source,
        success=bool(response.content),
        error_code=(response.error or "")[:100] or None,
    ))
    db.commit()


def get_router(provider: str = None, model: str = None, user_config: dict = None) -> AIProviderRouter:
    return AIProviderRouter(provider=provider, model=model, user_config=user_config)


def build_router_for_user(user_id: int, provider: str = None, model: str = None) -> AIProviderRouter:
    from app.services.ai_config_service import get_user_ai_config_row, resolve_api_key, config_to_dict
    row = get_user_ai_config_row(user_id)
    if row:
        cfg = config_to_dict(row)
        cfg["_resolved_api_key"] = resolve_api_key(row)
        return get_router(provider=provider, model=model, user_config=cfg)
    from app.services.ai_config_service import env_defaults
    return get_router(provider=provider, model=model, user_config=env_defaults())
