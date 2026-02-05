from dataclasses import dataclass
from .dragon import Dragon


@dataclass
class DragonC(Dragon):
    key: str = "C"
    lookahead: int = 2
    switch_dist: int = 6

    def manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def intercept(self, player_pos, player_dir, world):
        dr, dc = player_dir.delta
        target = player_pos
        for _ in range(self.lookahead):
            candidate = (target[0] + dr, target[1] + dc)
            if world.in_bounds(candidate) and world.is_walkable(candidate, self.walk_ctx()):
                target = candidate
            else:
                break
        return target

    def choose_goal(self, player_pos, player_dir, other_dragons, world):
        if self.manhattan(self.pos, player_pos) > self.switch_dist:
            return self.intercept(player_pos, player_dir, world)

        return player_pos
