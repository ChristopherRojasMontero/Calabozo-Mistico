from __future__ import annotations
from world.types import Direction, WalkContext

def step_turn(cfg, state, cmd: str) -> tuple[str, str | None]:
    """
    Retorna (status, event)
      status: "continue" | "death" | "win"
      event:  None | "key"
    """
    mapping = {"w": Direction.UP, "s": Direction.DOWN, "a": Direction.LEFT, "d": Direction.RIGHT}
    if cmd not in mapping:
        return ("continue", None)

    ctx = WalkContext(keys_collected=state.keys_collected, keys_required=cfg.keys_required)

    state.last_dir = mapping[cmd]
    dr, dc = state.last_dir.delta
    new_pos = (state.player[0] + dr, state.player[1] + dc)

    if state.world.is_walkable(new_pos, ctx):
        state.player = new_pos

    event: str | None = None
    if state.player in state.keys:
        state.keys.remove(state.player)
        state.keys_collected += 1
        event = "key"
        print("✅ Recogiste una llave!")

    pos_snapshot = {k: d.pos for k, d in state.dragons.items()}
    for d in state.dragons.values():
        d.step(player_pos=state.player, player_dir=state.last_dir, other_dragons=pos_snapshot)

    if any(d.pos == state.player for d in state.dragons.values()):
        return ("death", event)

    if state.player == state.level.door_pos and state.keys_collected >= cfg.keys_required:
        return ("win", event)

    return ("continue", event)
