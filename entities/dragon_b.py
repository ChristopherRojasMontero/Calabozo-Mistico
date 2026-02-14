from dataclasses import dataclass
from collections import deque
from .dragon import Dragon

@dataclass
class DragonB(Dragon):
    key: str = "B"
    lookahead: int = 3
    max_fallback_search: int = 30

    def nearest_walkable(self, start, world):
        ctx = self.walk_ctx()
        q = deque([start])
        seen = {start}
        steps = 0

        while q and steps < self.max_fallback_search:
            cur = q.popleft()
            steps += 1

            if world.in_bounds(cur) and world.is_walkable(cur, ctx):
                return cur

            r, c = cur
            for nb in ((r-1,c), (r+1,c), (r,c-1), (r,c+1)):
                if nb not in seen and world.in_bounds(nb):
                    seen.add(nb)
                    q.append(nb)

        return None

    def choose_goal(self, player_pos, player_dir, other_dragons, world):
        dr, dc = player_dir.delta

        desired = (player_pos[0] + dr * self.lookahead, player_pos[1] + dc * self.lookahead)

        desired = (
            max(0, min(world.rows - 1, desired[0])),
            max(0, min(world.cols - 1, desired[1]))
        )

        goal = desired if world.is_walkable(desired, self.walk_ctx()) else self.nearest_walkable(desired, world)

        return goal if goal is not None else player_pos

