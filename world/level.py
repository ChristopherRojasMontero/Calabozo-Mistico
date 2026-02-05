from __future__ import annotations

"""
world/level.py
--------------
Level = contenedor del "nivel completo".

Incluye:
- world: el GridWorld (terreno y reglas)
- player_start: inicio del jugador
- dragons_start: inicios de dragones (A/B/C)
- keys_positions: posiciones de llaves
- door_pos: posición de la puerta
"""

from dataclasses import dataclass

from world.types import Pos
from world.world import GridWorld


@dataclass(frozen=True)
class Level:
    world: GridWorld
    player_start: Pos
    dragons_start: dict[str, Pos]
    keys_positions: set[Pos]
    door_pos: Pos
