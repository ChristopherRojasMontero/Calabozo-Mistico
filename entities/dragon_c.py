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
            cand = (target[0] + dr, target[1] + dc)
            if world.in_bounds(cand) and world.is_walkable(cand, self.walk_ctx()):
                target = cand
            else:
                break
        return target

    def pincer_goal(self, player_pos, other_dragons, world):
        a_pos = other_dragons.get("A")
        if not a_pos:
            return None

        pr, pc = player_pos
        ar, ac = a_pos


        dr = pr - ar
        dc = pc - ac

        step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
        step_c = 0 if dc == 0 else (1 if dc > 0 else -1)

        desired = (pr + step_r, pc + step_c) 

        if world.in_bounds(desired) and world.is_walkable(desired, self.walk_ctx()):
            return desired
        return None

    def choose_goal(self, player_pos, player_dir, other_dragons, world):
        dist = self.manhattan(self.pos, player_pos)

        if dist > self.switch_dist:
            return self.intercept(player_pos, player_dir, world)
      
        pinch = self.pincer_goal(player_pos, other_dragons, world)
        if pinch is not None:
            return pinch

        dr, dc = player_dir.delta
        ahead = (player_pos[0] + dr, player_pos[1] + dc)
        if world.in_bounds(ahead) and world.is_walkable(ahead, self.walk_ctx()):
            return ahead

        return player_pos

