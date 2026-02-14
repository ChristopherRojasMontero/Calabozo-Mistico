from dataclasses import dataclass
from .dragon import Dragon

@dataclass
class DragonA(Dragon):
    key: str = "A"
    
    def choose_goal(self, player_pos, player_dir, other_dragons, world):
        return player_pos