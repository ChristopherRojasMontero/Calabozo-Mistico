from __future__ import annotations
from saves.save_load import save_game, load_game

def do_save(cfg, state) -> None:
    data = {
        "level": state.level_name,
        "player": state.player,
        "player_dir": state.last_dir,
        "keys_collected": state.keys_collected,
        "keys_remaining": state.keys,
        "dragons": {k: d.pos for k, d in state.dragons.items()},
    }
    save_game(cfg.save_path_for(state.level_name), data)

def do_load(cfg, loader, level_name: str) -> dict:
    return load_game(cfg.save_path_for(level_name), loader, keys_required=cfg.keys_required)
