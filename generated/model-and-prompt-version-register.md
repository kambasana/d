# Model and Prompt Version Register

| ID | Provider | Deployment | Roles | Model version | Prompt policy | Fallback | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AWG-AI-001 | Ollama | local/offline | dialogue realization, bounded option ranking, memory summarization, claim extraction | assigned per run | assigned per run | deterministic policy or no-op according to capability contract | adapter_required |
| AWG-AI-002 | OpenRouter | remote/hybrid | optional specialist reasoning and dialogue | assigned per run | assigned per run | local provider or deterministic policy according to scenario configuration | adapter_optional |
| AWG-AI-003 | Provider-neutral structured-output contract | core boundary | intent proposal, option ranking, dialogue realization, claim extraction, summarization | not applicable | versioned schema and policy | reject invalid output and preserve state | required |
