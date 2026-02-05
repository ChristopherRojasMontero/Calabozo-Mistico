from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import json
import time


@dataclass
class ReplayRecorder:
    level_name: str
    keys_required: int
    frames: list[dict[str, Any]] = field(default_factory=list)

    def record(
        self,
        t: int,
        player_pos,
        player_dir,
        keys_collected: int,
        dragons_pos: dict[str, Any],
        keys_remaining,
        event: str | None = None,
    ) -> None:
        self.frames.append(
            {
                "t": t,
                "player_pos": list(player_pos),  
                "player_dir": player_dir.name if player_dir else None,  
                "keys_collected": keys_collected,
                "dragons_pos": {k: list(v) for k, v in dragons_pos.items()},
                "keys_remaining": [list(k) for k in keys_remaining],
                "event": event,
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "meta": {
                "level_name": self.level_name,
                "keys_required": self.keys_required,
            },
            "frames": self.frames,
        }


def save_replay(path: str, data: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_replay(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def play_replay(
    loader,
    replay_data: dict[str, Any],
    render,
    mode: str,
    delay: float,
) -> None:
    from world.types import TileType 

    meta = replay_data["meta"]
    frames = replay_data["frames"]

    level = loader.load(meta["level_name"])

    rows = level.world.rows
    cols = level.world.cols


    walls = set()
    for r in range(rows):
        for c in range(cols):
            if level.world.grid.get((r, c)) == TileType.WALL:
                walls.add((r, c))

    print("\n=== REPLAY ===")
    print(f"Modo: {mode.upper()}  |  Frames: {len(frames)}")
    print("================\n")

    for fr in frames:
        keys_remaining = {tuple(k) for k in fr["keys_remaining"]}
        player_pos = tuple(fr["player_pos"])
        dragons_pos = {k: tuple(v) for k, v in fr["dragons_pos"].items()}

        render(
            rows,
            cols,
            walls,
            level.door_pos,
            keys_remaining,
            player_pos,
            dragons=dragons_pos,
        )

        if fr.get("event"):
            print(f"Evento: {fr['event']}")

        if mode == "step":
            cmd = input("Enter = siguiente | q = salir > ").strip().lower()
            if cmd == "q":
                break
        else:
            time.sleep(delay)
