from dataclasses import dataclass
from world.types import Direction, WalkContext
from .base import Entity


@dataclass
class Player(Entity):
    keys_collected: int = 0
    last_dir: Direction = Direction.DOWN

    def walk_ctx(self, keys_required: int = 4) -> WalkContext:
        return WalkContext(keys_collected=self.keys_collected, keys_required=keys_required)

    def try_move(self, direction: Direction, keys_required: int = 4) -> bool:
        self.last_dir = direction
        dr, dc = direction.delta
        new_pos = (self.pos[0] + dr, self.pos[1] + dc)

        if self.world.is_walkable(new_pos, self.walk_ctx(keys_required)):
            self.pos = new_pos
            return True
        return False
