from collections import deque
from typing import Optional
from world.types import Pos, WalkContext
from world.world import GridWorld


def bfs_next_step(world: GridWorld, start: Pos, goal: Pos, ctx: WalkContext) -> Optional[Pos]:
    if start == goal:
        return None

    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break

        for neighbor in world.neighbors4(current, ctx):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    if goal not in came_from:
        return None

    current = goal
    while came_from[current] != start:
        current = came_from[current]
    return current
