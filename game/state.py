from __future__ import annotations
from dataclasses import dataclass
from world.types import Direction, Pos

@dataclass
class GameState:
    level_name: str
    level: object
    world: object
    walls: set[Pos]

    player: Pos
    last_dir: Direction

    keys: set[Pos]
    keys_collected: int

    dragons: dict[str, object]

    tick: int = 0
