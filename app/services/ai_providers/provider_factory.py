# -*- coding: utf-8 -*-
import os
from .local_adapter import LocalAdapter
from .openai_adapter import OpenAIAdapter

def get_provider():
    provider = os.environ.get("AI_PROVIDER", "local").lower()
    if provider == "openai":
        return OpenAIAdapter()
    return LocalAdapter()
