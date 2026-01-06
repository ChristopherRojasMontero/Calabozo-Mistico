"""
Validaciones bases de 
Carga nivel de JSON
colisiones con paredes
recoger llaves
puerta que se abre con llaves
"""

from __future__ import annotations

from world.loader import JsonLevelLoader
from world.types import Direction, WalkContext, TileType, Pos

def render(rows: int, cols: int, walls: set[Pos], door: Pos, keys: set[Pos], player: Pos) -> None:
    for r in range(rows):
        line = []
        for c in range(cols):
            pos = (r, c)
            if pos == player:
                line.append("P")
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


def main() -> None:
    loader = JsonLevelLoader("levels")
    level = loader.load("level_01.json")

    world = level.world
    player = level.player_start
    keys = set(level.keys_positions)

    # Para render: sacar walls del grid (simple para demo)
    walls = set()
    for r in range(world.rows):
        for c in range(world.cols):
            if world.tile_at((r, c)) == TileType.WALL:
                walls.add((r, c))

    keys_collected = 0

    print("WASD para moverte, q para salir.\n")
    while True:
        render(world.rows, world.cols, walls, level.door_pos, keys, player)

        ctx = WalkContext(keys_collected=keys_collected, keys_required=4)
        print(f"Llaves: {keys_collected}/4")
        cmd = input("Move (w/a/s/d): ").strip().lower()
        if cmd == "q":
            break

        mapping = {"w": Direction.UP, "s": Direction.DOWN, "a": Direction.LEFT, "d": Direction.RIGHT}
        if cmd not in mapping:
            continue

        dr, dc = mapping[cmd].delta
        new_pos = (player[0] + dr, player[1] + dc)

        if world.is_walkable(new_pos, ctx):
            player = new_pos

        # recoger llave
        if player in keys:
            keys.remove(player)
            keys_collected += 1
            print("✅ Recogiste una llave!")

        # ganar
        if player == level.door_pos and keys_collected >= 4:
            render(world.rows, world.cols, walls, level.door_pos, keys, player)
            print("🎉 Ganaste! (demo consola)")
            break


if __name__ == "__main__":
    main()