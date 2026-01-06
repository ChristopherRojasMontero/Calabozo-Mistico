from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

# Pos representa una posición en el grid: (row, col)
Pos = tuple[int, int]

class TileType(Enum):
    WALL = 0
    FLOOR = 1
    DOOR = 2

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @property
    def delta(self) -> Pos:
        return self.value

@dataclass(frozen=True)
class WalkContext:
    """Contexto mínimo: llaves recolectadas y requeridas para abrir la puerta."""
    keys_collected: int
    keys_required: int = 4
