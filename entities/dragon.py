from dataclasses import dataclass
from world.types import WalkContext
from .base import Entity
from .pathfinding import bfs_next_step


@dataclass
class Dragon(Entity):
    key: str = "?"

    def walk_ctx(self) -> WalkContext:
        #Los dragones nunca pueden abrir la puerta
        return WalkContext(keys_collected=0, keys_required=4)

    def choose_goal(self, player_pos, player_dir, other_dragons, world):
        raise NotImplementedError

    def step(self, player_pos, player_dir, other_dragons):
        goal = self.choose_goal(player_pos, player_dir, other_dragons, self.world)
        next_pos = bfs_next_step(self.world, self.pos, goal, self.walk_ctx())
        if next_pos is not None:
            self.pos = next_pos
