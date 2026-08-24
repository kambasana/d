"""Bounded, provider-neutral AI proposal adapters for MVP 3."""

from .adapter import (
    CAPABILITIES,
    AIProviderAdapter,
    AdapterResult,
    ModelProvenance,
    OllamaAdapter,
    OpenRouterAdapter,
    RecordedTransport,
)

__all__ = [
    "CAPABILITIES",
    "AIProviderAdapter",
    "AdapterResult",
    "ModelProvenance",
    "OllamaAdapter",
    "OpenRouterAdapter",
    "RecordedTransport",
]
