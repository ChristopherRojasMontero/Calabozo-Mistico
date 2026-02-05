from __future__ import annotations

from game.config import GameConfig
from game import factory, persistence, step as step_mod, replay_manager


class GameController:
    def __init__(self, loader, render, choose_level, cfg: GameConfig | None = None):
        self.loader = loader
        self.render = render
        self.choose_level = choose_level
        self.cfg = cfg or GameConfig()

        self.state = None
        self.rec = None

    # Métodos para la GUI
    def start_new_gui(self, level_name: str) -> None:
        self.state = factory.new_game(self.loader, level_name)
        self.rec = replay_manager.start_recorder(self.cfg, self.state)

    def load_game_gui(self, level_name: str) -> bool:
        try:
            loaded = persistence.do_load(self.cfg, self.loader, level_name)
            self.state = factory.from_loaded(self.loader, loaded)
            self.rec = replay_manager.start_recorder(self.cfg, self.state)
            return True
        except Exception:
            return False

    def step_gui(self, cmd: str) -> tuple[str, str | None]:
        status, event = step_mod.step_turn(self.cfg, self.state, cmd)
        replay_manager.record_frame(self.state, self.rec, event=event)
        return status, event

    def save_game_gui(self) -> None:
        persistence.do_save(self.cfg, self.state)
        replay_manager.record_frame(self.state, self.rec, event="save")

    def choose_level_gui(self) -> str | None:
        return "level_01.json"

    # -------------------------
    # Inicio / reinicio
    # -------------------------

    def start_new(self) -> None:
        level_name = self.choose_level()
        self.state = factory.new_game(self.loader, level_name)
        self.rec = replay_manager.start_recorder(self.cfg, self.state)

        print(f"\nNivel cargado: {self.state.level_name}")
        print("WASD para moverte | g=guardar | q=salir\n")

    def restart_same_level(self) -> None:
        same_level = self.state.level_name
        self.state = factory.new_game(self.loader, same_level)
        self.rec = replay_manager.start_recorder(self.cfg, self.state)

        print(f"\nReiniciando nivel: {self.state.level_name}")

    # -------------------------
    # Render
    # -------------------------

    def draw(self) -> None:
        s = self.state
        self.render(
            s.world.rows,
            s.world.cols,
            s.walls,
            s.level.door_pos,
            s.keys,
            s.player,
            dragons={k: d.pos for k, d in s.dragons.items()},
        )
        print(f"Llaves: {s.keys_collected}/{self.cfg.keys_required}")

    # -------------------------
    # Menú post-partida
    # -------------------------

    def post_game_menu(self, last_replay_path: str | None) -> str:
        """
        Menú después de ganar o morir.
        Retorna: "restart_same" | "restart_choose" | "exit"
        """
        while True:
            print("\n=== FIN DE PARTIDA ===")
            print("1) Guardar partida (save del nivel)")
            print("2) Ver replay (partida recién terminada)")
            print("3) Jugar de nuevo (mismo nivel)")
            print("4) Jugar de nuevo (elegir nivel)")
            print("5) Salir")

            opt = input("Opción: ").strip()

            if opt == "1":
                try:
                    save_path = self.cfg.save_path_for(self.state.level_name)
                    persistence.do_save(self.cfg, self.state)
                    replay_manager.record_frame(self.state, self.rec, event="save")
                    print(f" Guardado en: {save_path}\n")
                except Exception as e:
                    print(e)
                continue

            if opt == "2":
                if not last_replay_path:
                    print(" No hay replay guardado.")
                    continue

                print("\nModo replay:")
                print("1) Automático")
                print("2) Paso a paso")

                m = input("> ").strip()
                mode = "auto" if m != "2" else "step"

                replay_manager.play_replay_from_file(
                    self.cfg,
                    self.loader,
                    self.render,
                    last_replay_path,
                    mode,
                )
                continue

            if opt == "3":
                return "restart_same"

            if opt == "4":
                return "restart_choose"

            if opt == "5":
                return "exit"

            print("Opción inválida.")

    # -------------------------
    # Loop principal
    # -------------------------

    def run(self) -> None:
        self.start_new()

        running = True
        while running:
            self.draw()
            cmd = input("Move (w/a/s/d) o (g/q): ").strip().lower()

            if cmd == "q":
                break

            if cmd == "g":
                try:
                    save_path = self.cfg.save_path_for(self.state.level_name)
                    persistence.do_save(self.cfg, self.state)
                    replay_manager.record_frame(self.state, self.rec, event="save")
                    print(f" Guardado en: {save_path}\n")
                except Exception as e:
                    print(e)
                continue

           
            status, event = step_mod.step_turn(self.cfg, self.state, cmd)
            replay_manager.record_frame(self.state, self.rec, event=event)

            if status not in {"death", "win"}:
                continue

            # -------------------------
            # FIN DE PARTIDA
            # -------------------------
            self.draw()

            if status == "death":
                print(" Un dragón te alcanzó. Fin del juego.")
            else:
                print(" ¡Ganaste el juego!")

            last_replay_path = replay_manager.finish_and_save(
                self.cfg,
                self.rec,
                self.state.level_name,
                event=status,
            )
            print(f" Replay guardado en: {last_replay_path}")

            action = self.post_game_menu(last_replay_path)

            if action == "exit":
                running = False
                break

            if action == "restart_same":
                self.restart_same_level()
                continue

            if action == "restart_choose":
                self.start_new()
                continue




