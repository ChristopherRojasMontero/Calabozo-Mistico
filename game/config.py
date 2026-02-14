from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class GameConfig:
    keys_required: int = 4
    replay_delay: float = 0.25

    def replay_path_for(self, level_name: str) -> str:
        try:
            num = level_name.split("_")[1].split(".")[0]
        except Exception:
            num = "last"
        return f"replay/replay_{num}.json"

    def save_path_for(self, level_name: str) -> str:
        try:
            num = level_name.split("_")[1].split(".")[0]
        except Exception:
            num = "last"
        return f"saves/save_{num}.json"


