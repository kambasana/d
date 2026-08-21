---
title: Example Scenario Package
document_id: AWG-SCN-005
status: draft
version: 0.2.0
last_updated: '2026-08-20'
normative: false
owners:
- AWG architecture
audience:
- engineering
- research
- product
depends_on:
- AWG-SCN-001
linear_issue: null
supersedes: []
---

# Example Scenario Package

This is an illustrative structure, not a committed schema.

```yaml
scenario_id: AWG-EXAMPLE-ROAD-001
version: 0.1.0
purpose: explore mobility and information response to bridge closure
world:
  geography_package: city-region-v1
  start_time: 2026-08-20T08:00:00+01:00
population:
  synthesis_package: pop-v3
systems:
  mobility: default
  information: default
plugins:
  ai_provider: ollama-local
  routing: local-routing-v1
seeds:
  world: 1001
  mobility: 2001
  information: 3001
interventions:
  - at: 2026-08-20T08:20:00+01:00
    command: CloseInfrastructure
    target: bridge-B
measurements:
  - mean_travel_delay
  - reroute_count
  - claim_exposure_count
  - official_message_reach
stop:
  at: 2026-08-20T18:00:00+01:00
```

## Expected sequence

1. Bridge closes through explicit scenario intervention.
2. Routing state changes and affected journeys may reroute.
3. Agents physically near the closure can perceive relevant effects according to perception rules.
4. Other agents learn through messages/news/social posts if valid paths exist.
5. Work schedules, meetings, traffic, and organizations may be affected through downstream causality.
6. Firehose records every relevant physical/informational transition.
7. A branch without the closure provides the baseline comparison.
