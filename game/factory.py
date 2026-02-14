from __future__ import annotations
from world.types import Direction, Pos, TileType
from entities.dragon_a import DragonA
from entities.dragon_b import DragonB
from entities.dragon_c import DragonC
from game.state import GameState

def build_walls(world) -> set[Pos]:
    walls: set[Pos] = set()
    for r in range(world.rows):
        for c in range(world.cols):
            if world.tile_at((r, c)) == TileType.WALL:
                walls.add((r, c))
    return walls

def make_dragons(level, world, dragons_pos: dict[str, Pos] | None = None) -> dict[str, object]:
    pos = dragons_pos or level.dragons_start
    return {
        "A": DragonA(pos=pos["A"], world=world),
        "B": DragonB(pos=pos["B"], world=world, lookahead=3),
        "C": DragonC(pos=pos["C"], world=world),
    }

def new_game(loader, level_name: str) -> GameState:
    level = loader.load(level_name)
    world = level.world
    walls = build_walls(world)

    return GameState(
        level_name=level_name,
        level=level,
        world=world,
        walls=walls,
        player=level.player_start,
        last_dir=Direction.DOWN,
        keys=set(level.keys_positions),
        keys_collected=0,
        dragons=make_dragons(level, world),
        tick=0,
    )

def from_loaded(loader, loaded: dict) -> GameState:
    level = loaded["level"]
    world = loaded["world"]
    walls = build_walls(world)

    dragons = make_dragons(level, world, loaded["dragons_pos"])

    return GameState(
        level_name=loaded["level_name"],
        level=level,
        world=world,
        walls=walls,
        player=loaded["player"],
        last_dir=loaded["player_dir"],
        keys=set(loaded["keys_remaining"]),
        keys_collected=loaded["keys_collected"],
        dragons=dragons,
        tick=0,
    )
