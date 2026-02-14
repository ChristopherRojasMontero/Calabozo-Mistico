from __future__ import annotations

from replay.replay_system import (
    ReplayRecorder,
    save_replay,
    load_replay,
    play_replay,
)


def start_recorder(cfg, state) -> ReplayRecorder:
    rec = ReplayRecorder(
        level_name=state.level_name,
        keys_required=cfg.keys_required,
    )
    rec.record(
        t=state.tick,
        player_pos=state.player,
        player_dir=state.last_dir,
        keys_collected=state.keys_collected,
        dragons_pos={k: d.pos for k, d in state.dragons.items()},
        keys_remaining=state.keys,
        event="start",
    )
    return rec


def record_frame(state, rec: ReplayRecorder, event: str | None = None) -> None:
    state.tick += 1
    rec.record(
        t=state.tick,
        player_pos=state.player,
        player_dir=state.last_dir,
        keys_collected=state.keys_collected,
        dragons_pos={k: d.pos for k, d in state.dragons.items()},
        keys_remaining=state.keys,
        event=event,
    )


def finish_and_save(cfg, rec: ReplayRecorder, level_name: str, event: str) -> str:
    if rec.frames:
        last = rec.frames[-1]
        prev = last.get("event")


        if prev and prev != event:
            last["event"] = [prev, event]
        else:
            last["event"] = event

    path = cfg.replay_path_for(level_name)
    save_replay(path, rec.to_dict())
    return path



def play_replay_from_file(cfg, loader, render, path: str, mode: str) -> None:
    data = load_replay(path)
    delay = getattr(cfg, "replay_delay", 0.25)
    play_replay(
        loader=loader,
        replay_data=data,
        render=render,
        mode=mode,
        delay=delay,
    )


