# Agent Journey Example

```text
08:10 Schedule wakes Agent A
08:10 A decides to travel to work
08:10 TravelToPlace(workplace, bus) command submitted
08:10 Validator confirms bus/walking route and access
08:10 JourneyStarted emitted
08:11 A walks toward bus stop
08:17 A arrives at stop
08:20 Bridge closure intervention occurs
08:22 Routing service invalidates planned downstream segment
08:22 JourneyRerouted emitted
08:46 A arrives at workplace entrance
08:47 A enters building through valid entrance
```

No location is assigned simply because the agent said it intended to travel.
