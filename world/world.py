"""
Aqui tenemos el GridWorld, que es el mundo del juego o sea el modelo del mapa

contenemos la representacion del mapa y sus reglas basicas como:
Limite del mapa 
que tile hay en una posicion
si se puede caminar en una posicion
vecinos en las 4 direcciones caminables
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from world.tile_grid import TileGrid
from world.types import Pos, TileType, WalkContext
from world.policies import WalkabilityPolicy, DefaultWalkabilityPolicy


@dataclass
class GridWorld:
    grid: TileGrid
    door_pos: Optional[Pos] = None
    policy: WalkabilityPolicy = DefaultWalkabilityPolicy()

    @property
    def rows(self) -> int:
        return self.grid.rows

    @property
    def cols(self) -> int:
        return self.grid.cols

    def in_bounds(self, pos: Pos) -> bool:
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def tile_at(self, pos: Pos) -> TileType:
        return self.grid.get(pos)

    def is_walkable(self, pos: Pos, ctx: WalkContext) -> bool:
        if not self.in_bounds(pos):
            return False
        return self.policy.is_walkable(self.tile_at(pos), pos, ctx)

    def neighbors4(self, pos: Pos, ctx: WalkContext) -> list[Pos]:
        r, c = pos
        candidates = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        return [p for p in candidates if self.is_walkable(p, ctx)]