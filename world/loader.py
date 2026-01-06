"""
Aqui cargamos niveles desde JSON desde levels
Path para rutas, Json para...parsear JSON, y any para el tipado para el dict del Json
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from world.types import Pos, TileType
from world.tile_grid import TileGrid
from world.world import GridWorld
from world.level import Level


class JsonLevelLoader:
    """Convierte un archivo JSON de levels/ en un Level del dominio."""

    def __init__(self, levels_dir: str | Path = "levels") -> None:
        self.levels_dir = Path(levels_dir)

    def load(self, filename: str) -> Level:
        data = self._read_json_file(self.levels_dir / filename)

        rows = int(data["rows"])
        cols = int(data["cols"])

        grid = TileGrid.filled(rows, cols, TileType.FLOOR)

        walls = {self._to_pos(p) for p in data.get("walls", [])}
        for pos in walls:
            self._ensure_in_bounds(pos, rows, cols, "wall")
            grid.set(pos, TileType.WALL)

        door_pos = self._to_pos(data["door"])
        self._ensure_in_bounds(door_pos, rows, cols, "door")
        grid.set(door_pos, TileType.DOOR)

        world = GridWorld(grid=grid, door_pos=door_pos)

        player_start = self._to_pos(data["player_start"])
        self._ensure_in_bounds(player_start, rows, cols, "player_start")

        dragons_raw = data["dragons_start"]
        dragons_start = {k: self._to_pos(v) for k, v in dragons_raw.items()}
        for k, pos in dragons_start.items():
            self._ensure_in_bounds(pos, rows, cols, f"dragon_start '{k}'")

        keys_positions = {self._to_pos(p) for p in data.get("keys", [])}
        for pos in keys_positions:
            self._ensure_in_bounds(pos, rows, cols, "key")

        return Level(
            world=world,
            player_start=player_start,
            dragons_start=dragons_start,
            keys_positions=keys_positions,
            door_pos=door_pos,
        )

    def _read_json_file(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(f"No existe el nivel: {path}")
        with path.open("r", encoding="utf-8-sig") as f:
            return json.load(f)

    def _to_pos(self, value: Any) -> Pos:
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise ValueError(f"Posición inválida (esperaba [row, col]): {value}")
        return int(value[0]), int(value[1])

    def _ensure_in_bounds(self, pos: Pos, rows: int, cols: int, field: str) -> None:
        r, c = pos
        if not (0 <= r < rows and 0 <= c < cols):
            raise ValueError(f"{field} fuera de límites: {pos} en {rows}x{cols}")