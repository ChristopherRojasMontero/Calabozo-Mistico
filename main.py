from __future__ import annotations

from world.loader import JsonLevelLoader
from ui.console_ui import render, choose_level
from game.controller import GameController
from game import persistence, factory
from game.config import GameConfig


def main() -> None:
    loader = JsonLevelLoader("levels")
    cfg = GameConfig()

    while True:
        print("\n=== CALABOZO MÍSTICO ===")
        print("1) Jugar (nuevo)")
        print("2) Cargar partida")
        print("3) Salir")

        opt = input("> ").strip()

        if opt == "3":
            print("👋 Hasta luego.")
            break

        if opt == "1":
            game = GameController(
                loader=loader,
                render=render,
                choose_level=choose_level,
                cfg=cfg,
            )
            game.run()
            continue

        if opt == "2":
            level_name = choose_level()
            try:
                loaded = persistence.do_load(cfg, loader, level_name)
                game = GameController(
                    loader=loader,
                    render=render,
                    choose_level=choose_level,
                    cfg=cfg,
                )
                game.state = factory.from_loaded(loader, loaded)

                from game import replay_manager
                game.rec = replay_manager.start_recorder(cfg, game.state)
                game.rec.frames[-1]["event"] = "load"
                
                game.run_loaded()
            except Exception as e:
                print(e)
            continue

        print("Opción inválida.")


if __name__ == "__main__":
    main()


