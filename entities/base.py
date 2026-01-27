from dataclasses import dataclass
from world.types import Pos
from world.world import GridWorld

@dataclass
class Entity:
    pos: Pos
    world: GridWorld
    
    def teleport(self, pos: Pos):
        self.pos = pos
        