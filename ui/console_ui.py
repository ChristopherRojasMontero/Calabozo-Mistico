from __future__ import annotations

from world.types import TileType, Pos


def render(
    rows: int,
    cols: int,
    walls: set[Pos],
    door: Pos,
    keys: set[Pos],
    player: Pos,
    dragons: dict[str, object],  
) -> None:
    dragons_pos: dict[str, Pos] = {}
    for k, v in dragons.items():
        dragons_pos[k] = v.pos if hasattr(v, "pos") else v

    for r in range(rows):
        line = []
        for c in range(cols):
            pos = (r, c)

            if pos == player:
                line.append("P")
            else:
                dragon_here = None
                for k, p in dragons_pos.items():
                    if p == pos:
                        dragon_here = k
                        break

                if dragon_here:
                    line.append(dragon_here)
                elif pos in keys:
                    line.append("K")
                elif pos == door:
                    line.append("D")
                elif pos in walls:
                    line.append("#")
                else:
                    line.append(".")
        print("".join(line))
    print()


def choose_level() -> str:
    levels = ["level_01.json", "level_02.json", "level_03.json"]

    print("Selecciona un nivel:")
    for i, name in enumerate(levels, start=1):
        print(f"  {i}) {name}")

    while True:
        opt = input("Nivel (1/2/3) o nombre exacto (ej: level_02.json): ").strip()
        if opt in {"1", "2", "3"}:
            return levels[int(opt) - 1]
        if opt in levels:
            return opt
        print("Opción inválida. Intenta de nuevo.")


def build_walls(world) -> set[Pos]:
    walls: set[Pos] = set()
    for r in range(world.rows):
        for c in range(world.cols):
            if world.tile_at((r, c)) == TileType.WALL:
                walls.add((r, c))
    return walls
