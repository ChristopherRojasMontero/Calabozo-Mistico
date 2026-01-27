
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from world.types import Direction, WalkContext, TileType, Pos


def _in_bounds(rows: int, cols: int, pos: Pos) -> bool:
    r, c = pos
    return 0 <= r < rows and 0 <= c < cols


def _is_not_wall(world, pos: Pos) -> bool:
    return world.tile_at(pos) != TileType.WALL


def _try_is_walkable(world, pos: Pos, ctx: WalkContext) -> bool:
    """
    Si world.is_walkable acepta ctx, lo usamos.
    Si no, caemos al check de pared (tile_at != WALL).
    """
    try:
        return world.is_walkable(pos, ctx) 
    except TypeError:
        return _is_not_wall(world, pos)


def save_game(path: str, game_state: dict[str, Any]) -> None:
    data = {
        "version": 1,
        "level": game_state["level"],
        "player": {
            "position": list(game_state["player"]),
            "direction": game_state["player_dir"].name,
            "keys_collected": int(game_state["keys_collected"]),
        },
        "dragons": {k: list(v) for k, v in game_state["dragons"].items()},
        "keys_remaining": [
            list(p) for p in sorted(game_state["keys_remaining"], key=lambda t: (t[0], t[1]))
        ],
    }

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"✔ Guardado: {p}")


def load_game(path: str, loader, keys_required: int = 4) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"❌ No existe el archivo de guardado: {p}")

    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Guardado corrupto (JSON inválido): {e}")

    for field in ("level", "player", "dragons", "keys_remaining"):
        if field not in data:
            raise ValueError(f"❌ Save inválido: falta '{field}'")

    level_name = data["level"]
    level = loader.load(level_name)
    world = level.world
    rows, cols = world.rows, world.cols


    player_pos = tuple(data["player"]["position"])
    if not _in_bounds(rows, cols, player_pos):
        raise ValueError("❌ Posición del jugador fuera del mapa")

    dir_str = data["player"].get("direction", "DOWN")
    try:
        player_dir = Direction[dir_str]
    except KeyError:
        raise ValueError(f"❌ Dirección inválida en save: {dir_str}")

    keys_collected = int(data["player"].get("keys_collected", 0))
    if keys_collected < 0 or keys_collected > keys_required:
        raise ValueError("❌ keys_collected fuera de rango")

   
    ctx = WalkContext(keys_collected=keys_collected, keys_required=keys_required)

    if not _try_is_walkable(world, player_pos, ctx):
        raise ValueError("❌ Posición inválida del jugador (no caminable)")

    
    dragons_pos: dict[str, Pos] = {}
    for k in ("A", "B", "C"):
        if k not in data["dragons"]:
            raise ValueError(f"❌ Save inválido: falta dragón '{k}'")
        pos = tuple(data["dragons"][k])
        if not _in_bounds(rows, cols, pos):
            raise ValueError(f"❌ Posición del dragón {k} fuera del mapa")
        if not _try_is_walkable(world, pos, ctx):
            raise ValueError(f"❌ Posición inválida del dragón {k} (no caminable)")
        dragons_pos[k] = pos

    
    keys_remaining = {tuple(p) for p in data["keys_remaining"]}
    level_keys = set(level.keys_positions)

    if not keys_remaining.issubset(level_keys):
        extra = keys_remaining - level_keys
        raise ValueError(f"❌ Save inválido: llaves que no pertenecen al nivel: {sorted(extra)}")

   
    total_level_keys = len(level_keys)
    if keys_collected + len(keys_remaining) != total_level_keys:
        raise ValueError(
            f"❌ Save inconsistente: keys_collected({keys_collected}) + "
            f"keys_remaining({len(keys_remaining)}) != total_keys_level({total_level_keys})"
        )

   
    for kp in keys_remaining:
        if not _in_bounds(rows, cols, kp) or not _is_not_wall(world, kp):
            raise ValueError("❌ Save inválido: llave en celda no válida")

    print(f"✔ Cargado: {p} (nivel: {level_name})")
    return {
        "level_name": level_name,
        "level": level,
        "world": world,
        "player": player_pos,
        "player_dir": player_dir,
        "keys_collected": keys_collected,
        "keys_remaining": keys_remaining,
        "dragons_pos": dragons_pos,
    }
