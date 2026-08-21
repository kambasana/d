from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Any, Mapping

from .bundle import DistrictBundle
from .model import AgentState


def semantic_clusters(
    agents: Mapping[str, AgentState],
    bundle: DistrictBundle,
    zoom: int,
) -> tuple[dict[str, Any], ...]:
    """Build a deterministic display projection without mutating world positions."""
    groups: dict[tuple[str, ...], list[AgentState]] = defaultdict(list)
    for agent in agents.values():
        if zoom <= 12:
            key = ("geographic", bundle.manifest["district_id"])
        elif zoom <= 15:
            key = ("geographic", agent.place_id)
        else:
            key = ("co_location", agent.place_id, agent.route_node_id)
        groups[key].append(agent)

    projection: list[dict[str, Any]] = []
    for key, members in sorted(groups.items()):
        members.sort(key=lambda agent: agent.agent_id)
        coordinates = [
            (
                bundle.nodes[member.route_node_id].longitude,
                bundle.nodes[member.route_node_id].latitude,
            )
            for member in members
        ]
        member_ids = [member.agent_id for member in members]
        digest = hashlib.sha256(f"{zoom}|{'|'.join(key)}|{'|'.join(member_ids)}".encode()).hexdigest()[:16]
        projection.append(
            {
                "cluster_id": f"cluster:{digest}",
                "cluster_type": key[0],
                "zoom_level": zoom,
                "member_count": len(members),
                "member_agent_ids": member_ids,
                "geographic_bounds": {
                    "west": min(item[0] for item in coordinates),
                    "south": min(item[1] for item in coordinates),
                    "east": max(item[0] for item in coordinates),
                    "north": max(item[1] for item in coordinates),
                },
                "representative_location": {
                    "longitude": sum(item[0] for item in coordinates) / len(coordinates),
                    "latitude": sum(item[1] for item in coordinates) / len(coordinates),
                },
                "place_id": key[1] if key[0] == "co_location" else None,
                "position_authority": "projection_only",
            }
        )
    return tuple(projection)


def building_occupancy(
    building_id: str,
    agents: Mapping[str, AgentState],
    bundle: DistrictBundle,
) -> dict[str, Any]:
    building = bundle.buildings[building_id]
    floors: dict[str, dict[str, Any]] = {}
    for floor in building["floors"]:
        floors[floor["floor_id"]] = {
            "floor_id": floor["floor_id"],
            "level": floor["level"],
            "occupant_count": 0,
            "rooms": {
                room_id: {"room_id": room_id, "occupant_count": 0, "agent_ids": []}
                for room_id in floor["room_ids"]
            },
        }
    outside_room: list[str] = []
    for agent in sorted(agents.values(), key=lambda item: item.agent_id):
        if agent.building_id != building_id:
            continue
        matched = False
        for floor in floors.values():
            if agent.room_id in floor["rooms"]:
                room = floor["rooms"][agent.room_id]
                room["occupant_count"] += 1
                room["agent_ids"].append(agent.agent_id)
                floor["occupant_count"] += 1
                matched = True
                break
        if not matched:
            outside_room.append(agent.agent_id)
    count = sum(floor["occupant_count"] for floor in floors.values()) + len(outside_room)
    return {
        "building_id": building_id,
        "name": building["name"],
        "capacity": building["capacity"],
        "occupant_count": count,
        "floors": list(floors.values()),
        "unresolved_room_agent_ids": outside_room,
        "position_authority": "authoritative_occupancy_projection",
    }
