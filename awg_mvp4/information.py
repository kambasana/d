from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from typing import Any

UTC = timezone.utc
WORLD_TRUTH = "electrical transformer failure"


class CommandRejected(ValueError):
    """A typed information command failed validation."""


class InformationKernel:
    """Event-sourced claims, exposure, social actions, and beliefs."""

    def __init__(self) -> None:
        self.world_id = "world:mvp4-information"
        self.scenario_id = "scenario:mvp4-reference"
        self.branch_id = "branch:main"
        self.now = datetime(2042, 5, 4, 14, 30, tzinfo=UTC)
        self.world_truth = WORLD_TRUTH
        self.actors: dict[str, dict[str, Any]] = {}
        self.claims: dict[str, dict[str, Any]] = {}
        self.posts: dict[str, dict[str, Any]] = {}
        self.messages: dict[str, dict[str, Any]] = {}
        self.exposed: dict[str, set[str]] = {}
        self.beliefs: dict[str, dict[str, str]] = {}
        self.likes: dict[str, set[str]] = {}
        self.follows: dict[str, set[str]] = {}
        self.blocks: dict[str, set[str]] = {}
        self.events: list[dict[str, Any]] = []
        self.rank_config = {"recency_weight": 1.0, "follow_weight": 1.0, "seed": 7}
        self._seed_society()

    def _seed_society(self) -> None:
        for index in range(100):
            actor_id = f"agent:info-{index:03d}"
            self.actors[actor_id] = {
                "embodiment": "physical",
                "information_only": False,
                "tokens": 10,
            }
            self.exposed[actor_id] = set()
            self.beliefs[actor_id] = {}
            self.likes[actor_id] = set()
            self.follows[actor_id] = set()
            self.blocks[actor_id] = set()
        self.actors["org:news-desk"] = {
            "embodiment": "none",
            "information_only": True,
            "tokens": 0,
        }
        self.exposed["org:news-desk"] = set()
        self.beliefs["org:news-desk"] = {}
        self.likes["org:news-desk"] = set()
        self.follows["org:news-desk"] = set()
        self.blocks["org:news-desk"] = set()
        publisher = "agent:info-002"
        for index in range(3, 90):
            follower = f"agent:info-{index:03d}"
            self.follows[follower].add(publisher)

    def _format_time(self) -> str:
        return self.now.astimezone(UTC).isoformat().replace("+00:00", "Z")

    def _event(
        self,
        event_type: str,
        *,
        actor_id: str | None,
        payload: dict[str, Any],
        target_ids: tuple[str, ...] = (),
        parent_event_ids: tuple[str, ...] = (),
        command_id: str | None = None,
    ) -> dict[str, Any]:
        event = {
            "schema_version": "0.2.0",
            "event_id": f"event:mvp4-{len(self.events) + 1:08d}",
            "event_type": event_type,
            "world_id": self.world_id,
            "scenario_id": self.scenario_id,
            "branch_id": self.branch_id,
            "simulation_time": self._format_time(),
            "sequence": len(self.events) + 1,
            "recorded_at": self._format_time(),
            "actor_id": actor_id,
            "target_ids": list(target_ids),
            "command_id": command_id,
            "parent_event_ids": list(parent_event_ids),
            "caused_by_event_ids": list(parent_event_ids),
            "location": {},
            "payload": payload,
        }
        self.events.append(event)
        self._apply(event)
        return event

    def _apply(self, event: dict[str, Any]) -> None:
        payload = event["payload"]
        if event["event_type"] == "ClaimAsserted":
            self.claims[payload["claim_id"]] = dict(payload)
        elif event["event_type"] in {"ClaimReceived", "PostViewed", "MessageDelivered"}:
            agent_id = payload["agent_id"]
            self.exposed[agent_id].add(payload["claim_id"])
        elif event["event_type"] == "PostCreated":
            self.posts[payload["post_id"]] = dict(payload)
        elif event["event_type"] == "PostLiked":
            self.likes[payload["agent_id"]].add(payload["post_id"])
        elif event["event_type"] == "BeliefUpdated":
            self.beliefs[payload["agent_id"]][payload["claim_id"]] = payload["new_disposition"]
        elif event["event_type"] == "ActorBlocked":
            self.blocks[payload["agent_id"]].add(payload["blocked_id"])
        elif event["event_type"] == "ClaimCorrected":
            self.claims[payload["claim_id"]] = {
                **self.claims[payload["claim_id"]],
                "corrected": True,
                "correction_text": payload["correction_text"],
            }

    def knows(self, agent_id: str, claim_id: str) -> bool:
        return claim_id in self.exposed[agent_id]

    def believes(self, agent_id: str, claim_id: str) -> bool:
        return self.beliefs[agent_id].get(claim_id) == "believed"

    def eligible_audience(self, post_id: str) -> set[str]:
        post = self.posts[post_id]
        author = post["actor_id"]
        visibility = post["visibility"]
        audience: set[str] = set()
        for actor_id in self.actors:
            if actor_id == author:
                continue
            if author in self.blocks[actor_id]:
                continue
            if visibility == "public":
                audience.add(actor_id)
            elif visibility == "followers" and author in self.follows[actor_id]:
                audience.add(actor_id)
            elif visibility == "private" and actor_id in post.get("recipient_ids", []):
                audience.add(actor_id)
        return audience

    def feed_for(self, agent_id: str) -> list[str]:
        ranked = []
        for post_id, post in self.posts.items():
            if agent_id not in self.eligible_audience(post_id) and post["actor_id"] != agent_id:
                continue
            score = self.rank_config["recency_weight"]
            if post["actor_id"] in self.follows[agent_id]:
                score += self.rank_config["follow_weight"]
            ranked.append((score, post_id))
        ranked.sort(key=lambda item: (-item[0], item[1]))
        return [post_id for _, post_id in ranked]

    def lineage(self, event_id: str) -> list[str]:
        by_id = {event["event_id"]: event for event in self.events}
        chain = []
        current = by_id[event_id]
        while current:
            chain.append(current["event_id"])
            parents = current.get("parent_event_ids") or []
            current = by_id.get(parents[0]) if parents else None
        chain.reverse()
        return chain

    def _expose(self, agent_id: str, claim_id: str, event_type: str, parent: dict[str, Any], extra: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = {"agent_id": agent_id, "claim_id": claim_id, **(extra or {})}
        return self._event(
            event_type,
            actor_id=agent_id,
            payload=payload,
            target_ids=(claim_id,),
            parent_event_ids=(parent["event_id"],),
        )

    def run_reference(self) -> None:
        observer = "agent:info-000"
        relay = "agent:info-001"
        publisher = "agent:info-002"
        liker = "agent:info-003"
        reposter = "agent:info-004"
        outsider = "agent:info-095"
        blocked = "agent:info-098"
        deceiver = "agent:info-099"
        claim_id = "claim:transformer:001"
        rumor_id = "claim:transformer:rumor"

        observed = self._event(
            "ObservationCreated",
            actor_id=observer,
            payload={"observation_id": "observation:0001", "world_truth": self.world_truth},
            target_ids=("observation:0001",),
        )
        asserted = self._event(
            "ClaimAsserted",
            actor_id=observer,
            payload={
                "claim_id": claim_id,
                "proposition": "A loud bang and smoke were observed near the substation.",
                "original_source": observer,
                "source_chain": [observer],
                "corrected": False,
            },
            parent_event_ids=(observed["event_id"],),
            target_ids=(claim_id,),
        )
        self._expose(observer, claim_id, "ClaimReceived", asserted)
        self._event(
            "BeliefUpdated",
            actor_id=observer,
            payload={
                "belief_id": "belief:info-000:001",
                "agent_id": observer,
                "claim_id": claim_id,
                "previous_disposition": None,
                "new_disposition": "believed",
                "confidence": 0.8,
                "evidence_refs": ["observation:0001"],
                "reason_code": "direct_experience",
            },
            parent_event_ids=(asserted["event_id"],),
        )

        sent = self._event(
            "MessageSent",
            actor_id=observer,
            command_id="command:send-message:001",
            payload={
                "message_id": "message:0001",
                "recipient_ids": [relay],
                "claim_id": claim_id,
                "channel_id": "channel:dm",
                "visibility": "private",
            },
            parent_event_ids=(asserted["event_id"],),
        )
        delivered = self._expose(relay, claim_id, "MessageDelivered", sent, {"message_id": "message:0001"})
        shared = self._event(
            "ClaimShared",
            actor_id=observer,
            payload={
                "claim_id": claim_id,
                "source_agent_id": observer,
                "recipient_ids": [relay],
                "channel_id": "channel:dm",
                "message_id": "message:0001",
                "parent_transmission_event_id": sent["event_id"],
            },
            parent_event_ids=(delivered["event_id"],),
        )
        self._expose(relay, claim_id, "ClaimReceived", shared)

        sent_b = self._event(
            "MessageSent",
            actor_id=relay,
            command_id="command:send-message:002",
            payload={
                "message_id": "message:0002",
                "recipient_ids": [publisher],
                "claim_id": claim_id,
                "channel_id": "channel:dm",
                "visibility": "private",
            },
            parent_event_ids=(shared["event_id"],),
        )
        delivered_b = self._expose(publisher, claim_id, "MessageDelivered", sent_b, {"message_id": "message:0002"})
        shared_b = self._event(
            "ClaimShared",
            actor_id=relay,
            payload={
                "claim_id": claim_id,
                "source_agent_id": relay,
                "recipient_ids": [publisher],
                "channel_id": "channel:dm",
                "message_id": "message:0002",
                "parent_transmission_event_id": sent_b["event_id"],
            },
            parent_event_ids=(delivered_b["event_id"],),
        )
        self._expose(publisher, claim_id, "ClaimReceived", shared_b)

        posted = self._event(
            "PostCreated",
            actor_id=publisher,
            command_id="command:create-social-post:001",
            payload={
                "post_id": "post:c-0003:001",
                "actor_id": publisher,
                "claim_id": claim_id,
                "visibility": "followers",
                "content": "Explosion reported downtown.",
                "recipient_ids": [],
            },
            parent_event_ids=(shared_b["event_id"],),
        )
        self.now += timedelta(seconds=1)
        viewed = self._expose(liker, claim_id, "PostViewed", posted, {"post_id": "post:c-0003:001"})
        self._event(
            "PostLiked",
            actor_id=liker,
            payload={"agent_id": liker, "post_id": "post:c-0003:001", "claim_id": claim_id},
            parent_event_ids=(viewed["event_id"],),
        )
        viewed_r = self._expose(reposter, claim_id, "PostViewed", posted, {"post_id": "post:c-0003:001"})
        reposted = self._event(
            "PostReposted",
            actor_id=reposter,
            payload={"agent_id": reposter, "post_id": "post:c-0003:001", "repost_id": "post:e-0005:001", "claim_id": claim_id},
            parent_event_ids=(viewed_r["event_id"],),
        )

        self._event(
            "ActorBlocked",
            actor_id=blocked,
            payload={"agent_id": blocked, "blocked_id": publisher},
        )
        for index in range(3, 90):
            actor_id = f"agent:info-{index:03d}"
            if actor_id in {liker, reposter} or actor_id not in self.eligible_audience("post:c-0003:001"):
                continue
            self._expose(actor_id, claim_id, "PostViewed", posted, {"post_id": "post:c-0003:001"})
        for index in range(5, 45):
            actor_id = f"agent:info-{index:03d}"
            self._event(
                "PostLiked",
                actor_id=actor_id,
                payload={"agent_id": actor_id, "post_id": "post:c-0003:001", "claim_id": claim_id},
            )
        for index in range(10, 30):
            actor_id = f"agent:info-{index:03d}"
            self._event(
                "CommentCreated",
                actor_id=actor_id,
                payload={"agent_id": actor_id, "post_id": "post:c-0003:001", "claim_id": claim_id, "text": "noted"},
            )
        for index in range(40, 50):
            actor_id = f"agent:info-{index:03d}"
            self._event(
                "PostReposted",
                actor_id=actor_id,
                payload={"agent_id": actor_id, "post_id": "post:c-0003:001", "repost_id": f"post:r-{index:03d}", "claim_id": claim_id},
                parent_event_ids=(posted["event_id"],),
            )

        self._event(
            "ClaimCorrected",
            actor_id=publisher,
            payload={
                "claim_id": claim_id,
                "original_post_id": "post:c-0003:001",
                "correction_text": "Clarification: transformer failure, not an attack.",
            },
            parent_event_ids=(posted["event_id"],),
        )
        self._event(
            "ClaimAsserted",
            actor_id=deceiver,
            payload={
                "claim_id": rumor_id,
                "proposition": "Attack happening downtown.",
                "original_source": deceiver,
                "source_chain": [deceiver],
                "corrected": False,
                "scenario_deception": True,
            },
        )
        self._event(
            "ClaimRetracted",
            actor_id=deceiver,
            payload={"claim_id": rumor_id, "original_preserved": True},
        )
        self._event(
            "FactCheckRequested",
            actor_id="agent:info-005",
            payload={"claim_id": claim_id, "outcome": "failed", "reason": "no_access_to_record"},
        )
        self._event(
            "SourceContacted",
            actor_id="agent:info-005",
            payload={"claim_id": claim_id, "source_id": observer, "outcome": "delivered"},
        )
        news = self._event(
            "PostCreated",
            actor_id="org:news-desk",
            payload={
                "post_id": "post:news:001",
                "actor_id": "org:news-desk",
                "claim_id": "claim:utility:001",
                "visibility": "public",
                "content": "Utility reports equipment failure.",
                "recipient_ids": [],
            },
            parent_event_ids=(asserted["event_id"],),
        )
        impression = 0
        while len(self.events) < 1000:
            impression += 1
            self.now += timedelta(seconds=1)
            for actor_id in sorted(self.eligible_audience("post:news:001")):
                if len(self.events) >= 1000:
                    break
                self._expose(
                    actor_id,
                    "claim:utility:001",
                    "PostViewed",
                    news,
                    {"post_id": "post:news:001", "impression": impression},
                )
            if impression > 50:
                raise RuntimeError("unable to reach 1000 information events")

        self.chain_anchor = reposted["event_id"]
        self.original_post = deepcopy(self.posts["post:c-0003:001"])
        self.outsider = outsider
        self.claim_id = claim_id
        self.liker = liker

    def participant_projection(self, agent_id: str) -> dict[str, Any]:
        return {
            "agent_id": agent_id,
            "exposed_claims": sorted(self.exposed[agent_id]),
            "beliefs": dict(self.beliefs[agent_id]),
            "feed": self.feed_for(agent_id),
            "world_truth": None,
        }

    def analyst_projection(self) -> dict[str, Any]:
        return {
            "world_truth": self.world_truth,
            "rank_config": dict(self.rank_config),
            "event_count": len(self.events),
        }

    def state_checksum(self) -> str:
        payload = {
            "exposed": {key: sorted(value) for key, value in sorted(self.exposed.items())},
            "beliefs": {key: dict(value) for key, value in sorted(self.beliefs.items())},
            "likes": {key: sorted(value) for key, value in sorted(self.likes.items())},
            "posts": self.posts,
            "claims": self.claims,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()

    @classmethod
    def replay(cls, events: list[dict[str, Any]]) -> InformationKernel:
        replayed = cls()
        replayed.events.clear()
        for expected, event in enumerate(events, start=1):
            if event["sequence"] != expected:
                raise ValueError("event sequence is not contiguous")
            replayed.events.append(event)
            replayed._apply(event)
        return replayed
