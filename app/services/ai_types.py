# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class AIResponse:
    content: str = ""
    provider: str = "rules"
    model: str = "fallback"
    latency_ms: int = 0
    tokens_input: int = 0
    tokens_output: int = 0
    raw_response: Any = None
    error: Optional[str] = None
    used_fallback: bool = False

    @property
    def ok(self) -> bool:
        return bool(self.content) and not self.error
