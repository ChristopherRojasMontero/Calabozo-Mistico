from dataclasses import dataclass
from .dragon import Dragon


@dataclass
class DragonB(Dragon):
    key: str = "B"
    lookahead: int = 3

    def choose_goal(self, player_pos, player_dir, other_dragons, world):
        dr, dc = player_dir.delta
        target = player_pos

        for _ in range(self.lookahead):
            candidate = (target[0] + dr, target[1] + dc)
            if world.in_bounds(candidate) and world.is_walkable(candidate, self.walk_ctx()):
                target = candidate
            else:
                break

        return target
