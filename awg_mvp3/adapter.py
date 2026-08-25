from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping, Protocol

INTERFACE_VERSION = "0.2.0"
OUTPUT_SCHEMA_VERSION = "0.2.0"
CAPABILITIES = (
    "propose_intent",
    "rank_options",
    "realize_dialogue",
    "summarize_memories",
    "extract_claims",
)


class ProviderTransport(Protocol):
    def __call__(self, request: Mapping[str, Any], timeout_seconds: float) -> str | Mapping[str, Any]: ...


@dataclass(frozen=True)
class ModelProvenance:
    adapter_id: str
    adapter_version: str
    provider_id: str
    model_version: str
    prompt_policy_version: str
    interface_version: str
    output_schema_version: str
    request_id: str
    outcome: str


@dataclass(frozen=True)
class AdapterResult:
    capability: str
    accepted: bool
    proposal: dict[str, Any] | None
    error_code: str | None
    provenance: ModelProvenance

    def as_dict(self) -> dict[str, Any]:
        return {"artifact_version": OUTPUT_SCHEMA_VERSION, **asdict(self)}


class RecordedTransport:
    """Offline transport keyed by request id; never invokes a provider."""

    def __init__(self, records: Mapping[str, str | Mapping[str, Any]]) -> None:
        self._records = dict(records)
        self.calls = 0

    def __call__(self, request: Mapping[str, Any], timeout_seconds: float) -> str | Mapping[str, Any]:
        del timeout_seconds
        self.calls += 1
        request_id = str(request["request_id"])
        if request_id not in self._records:
            raise KeyError(f"no recorded output for {request_id}")
        return self._records[request_id]


class AIProviderAdapter:
    """Provider-neutral proposal boundary with no world-state references."""

    adapter_id = "ai-provider"
    adapter_version = "0.2.0"

    def __init__(
        self,
        *,
        provider_id: str,
        model_version: str,
        prompt_policy_version: str,
        transport: ProviderTransport,
        timeout_seconds: float = 5.0,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self.provider_id = provider_id
        self.model_version = model_version
        self.prompt_policy_version = prompt_policy_version
        self.transport = transport
        self.timeout_seconds = timeout_seconds

    def propose_intent(self, request_id: str, context: Mapping[str, Any]) -> AdapterResult:
        return self._invoke("propose_intent", request_id, context)

    def rank_options(self, request_id: str, context: Mapping[str, Any]) -> AdapterResult:
        return self._invoke("rank_options", request_id, context)

    def realize_dialogue(self, request_id: str, context: Mapping[str, Any]) -> AdapterResult:
        return self._invoke("realize_dialogue", request_id, context)

    def summarize_memories(self, request_id: str, context: Mapping[str, Any]) -> AdapterResult:
        return self._invoke("summarize_memories", request_id, context)

    def extract_claims(self, request_id: str, context: Mapping[str, Any]) -> AdapterResult:
        return self._invoke("extract_claims", request_id, context)

    def _invoke(self, capability: str, request_id: str, context: Mapping[str, Any]) -> AdapterResult:
        request = {
            "interface_version": INTERFACE_VERSION,
            "output_schema_version": OUTPUT_SCHEMA_VERSION,
            "capability": capability,
            "request_id": request_id,
            "context": dict(context),
        }
        try:
            raw = self.transport(request, self.timeout_seconds)
            output = json.loads(raw) if isinstance(raw, str) else dict(raw)
            proposal = self._validate(capability, output)
        except TimeoutError:
            return self._rejected(capability, request_id, "timeout")
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            return self._rejected(capability, request_id, "invalid_output")
        except Exception:
            return self._rejected(capability, request_id, "provider_error")
        return AdapterResult(
            capability=capability,
            accepted=True,
            proposal=proposal,
            error_code=None,
            provenance=self._provenance(request_id, "accepted"),
        )

    def _rejected(self, capability: str, request_id: str, error_code: str) -> AdapterResult:
        return AdapterResult(
            capability=capability,
            accepted=False,
            proposal=None,
            error_code=error_code,
            provenance=self._provenance(request_id, error_code),
        )

    def _provenance(self, request_id: str, outcome: str) -> ModelProvenance:
        return ModelProvenance(
            adapter_id=self.adapter_id,
            adapter_version=self.adapter_version,
            provider_id=self.provider_id,
            model_version=self.model_version,
            prompt_policy_version=self.prompt_policy_version,
            interface_version=INTERFACE_VERSION,
            output_schema_version=OUTPUT_SCHEMA_VERSION,
            request_id=request_id,
            outcome=outcome,
        )

    @staticmethod
    def _validate(capability: str, output: Mapping[str, Any]) -> dict[str, Any]:
        if output.get("schema_version") != OUTPUT_SCHEMA_VERSION:
            raise ValueError("output schema mismatch")
        if output.get("capability") != capability:
            raise ValueError("capability mismatch")
        proposal = output.get("proposal")
        if not isinstance(proposal, dict):
            raise TypeError("proposal must be an object")

        if capability == "propose_intent":
            required = {"proposal_type", "intent_kind", "parameters"}
            if proposal.get("proposal_type") not in {"IntentProposed", "CommandProposed"}:
                raise ValueError("invalid proposal type")
            if not isinstance(proposal.get("intent_kind"), str) or not isinstance(proposal.get("parameters"), dict):
                raise TypeError("invalid intent")
        elif capability == "rank_options":
            required = {"proposal_type", "ranked_options"}
            options = proposal.get("ranked_options")
            if proposal.get("proposal_type") != "OptionRanking" or not isinstance(options, list) or not options:
                raise ValueError("invalid option ranking")
            if any(
                not isinstance(item, dict)
                or not isinstance(item.get("option_id"), str)
                or not isinstance(item.get("score"), (int, float))
                for item in options
            ):
                raise TypeError("invalid ranked option")
        elif capability == "realize_dialogue":
            required = {"proposal_type", "text"}
            if proposal.get("proposal_type") != "DialogueRealization" or not isinstance(proposal.get("text"), str):
                raise ValueError("invalid dialogue")
        elif capability == "summarize_memories":
            required = {"proposal_type", "summary"}
            if proposal.get("proposal_type") != "MemorySummaryDraft" or not isinstance(proposal.get("summary"), str):
                raise ValueError("invalid memory summary")
        elif capability == "extract_claims":
            required = {"proposal_type", "claims"}
            claims = proposal.get("claims")
            if proposal.get("proposal_type") != "ClaimDrafts" or not isinstance(claims, list):
                raise ValueError("invalid claim drafts")
            if any(not isinstance(item, dict) or not isinstance(item.get("text"), str) for item in claims):
                raise TypeError("invalid claim")
        else:
            raise ValueError("unsupported capability")
        if not required.issubset(proposal):
            raise ValueError("proposal lacks required fields")
        return dict(proposal)


class OllamaAdapter(AIProviderAdapter):
    adapter_id = "ollama"

    def __init__(self, *, model_version: str, prompt_policy_version: str, transport: ProviderTransport, timeout_seconds: float = 5.0) -> None:
        super().__init__(
            provider_id="ollama",
            model_version=model_version,
            prompt_policy_version=prompt_policy_version,
            transport=transport,
            timeout_seconds=timeout_seconds,
        )


class OpenRouterAdapter(AIProviderAdapter):
    adapter_id = "openrouter"

    def __init__(self, *, model_version: str, prompt_policy_version: str, transport: ProviderTransport, timeout_seconds: float = 5.0) -> None:
        super().__init__(
            provider_id="openrouter",
            model_version=model_version,
            prompt_policy_version=prompt_policy_version,
            transport=transport,
            timeout_seconds=timeout_seconds,
        )
