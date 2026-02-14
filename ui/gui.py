import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from replay.replay_system import ReplayRecorder


class GameGUI:
    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("Calabozo Místico")
        self.root.minsize(820, 520)

        self.colors = {
            "wall": "#22313f",
            "floor": "#ecf0f1",
            "player": "#e74c3c",
            "dragon": "#8e44ad",
            "key": "#f1c40f",
            "door": "#27ae60",
            "text": "#f7f7f7",
            "muted": "#cfd8dc",
            "bg": "#2f3e4e",
            "card": "#253444",
            "card2": "#1f2c3a",
            "grid": "#dfe6e9",
        }

        self.cell_size = 30
        self.canvas = None
        self.status_label = None
        self.level_window = None

        self._replay_data = None
        self._replay_static = None 
        self._replay_i = 0
        self._replay_mode = "auto" 
        self._replay_running = False
        self._replay_speed_ms = 120 
        self._replay_screen = False  

        self.style = ttk.Style(self.root)
        self.setup_style()
        self.setup_main_menu()


    def setup_style(self):
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        bg = self.colors["bg"]
        card = self.colors["card"]
        fg = self.colors["text"]

        self.root.configure(bg=bg)

        self.font_title = ("Segoe UI", 28, "bold")
        self.font_h2 = ("Segoe UI", 12, "bold")
        self.font_body = ("Segoe UI", 11)
        self.font_small = ("Segoe UI", 10)

        self.style.configure("TFrame", background=bg)
        self.style.configure("Card.TFrame", background=card)
        self.style.configure("Card2.TFrame", background=self.colors["card2"])

        self.style.configure("TLabel", background=bg, foreground=fg, font=self.font_body)
        self.style.configure("Title.TLabel", background=bg, foreground=fg, font=self.font_title)
        self.style.configure("Card.TLabel", background=card, foreground=fg, font=self.font_body)
        self.style.configure("Muted.TLabel", background=card, foreground=self.colors["muted"], font=self.font_small)
        self.style.configure("H2.TLabel", background=card, foreground=fg, font=self.font_h2)

        self.style.configure(
            "Menu.TButton",
            font=self.font_body,
            padding=(18, 10),
            background="#f6f7f8",
            foreground="#111",
            borderwidth=0,
            relief="flat",
        )
        self.style.map(
            "Menu.TButton",
            background=[("active", "#e8eaed"), ("pressed", "#dfe3e6")],
        )

        self.style.configure(
            "Primary.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(18, 10),
            background="#2ecc71",
            foreground="#0b1a12",
            borderwidth=0,
            relief="flat",
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", "#28b463"), ("pressed", "#239b56")],
        )

        self.style.configure(
            "Danger.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(18, 10),
            background="#e74c3c",
            foreground="#2b0f0c",
            borderwidth=0,
            relief="flat",
        )
        self.style.map(
            "Danger.TButton",
            background=[("active", "#d64537"), ("pressed", "#c0392b")],
        )

        self.style.configure("TScale", background=card)


    def clear_window(self):
        for w in self.root.winfo_children():
            w.destroy()

    def center_window(self, win=None):
        win = win or self.root
        win.update_idletasks()
        w = win.winfo_reqwidth()
        h = win.winfo_reqheight()
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        win.geometry(f"+{x}+{y}")


    def setup_main_menu(self):
        self._replay_running = False
        self._replay_screen = False

        self.clear_window()
        try:
            self.root.unbind("<Key>")
        except Exception:
            pass

        outer = ttk.Frame(self.root)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(side="top", fill="x", pady=(36, 14))
        ttk.Label(header, text="CALABOZO MÍSTICO", style="Title.TLabel").pack()

        card = ttk.Frame(outer, style="Card.TFrame", padding=(26, 22))
        card.pack(side="top")

        ttk.Label(card, text="Menú", style="H2.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(card, text="Elige una opción para iniciar.", style="Muted.TLabel").pack(anchor="w", pady=(0, 16))

        btns = ttk.Frame(card, style="Card.TFrame")
        btns.pack(fill="x")

        ttk.Button(btns, text="Nueva Partida", command=self.new_game, style="Primary.TButton").pack(fill="x", pady=6)
        ttk.Button(btns, text="Cargar Partida", command=self.load_game, style="Menu.TButton").pack(fill="x", pady=6)
        ttk.Button(btns, text="Salir", command=self.root.quit, style="Menu.TButton").pack(fill="x", pady=6)

        tip = ttk.Label(
            outer,
            text="Tip: en partida usa WASD, G para guardar, Q para menú. En replay: Espacio/→ para avanzar.",
            font=self.font_small,
            foreground=self.colors["muted"],
            background=self.colors["bg"],
        )
        tip.pack(side="top", pady=(18, 0))

        self.center_window()

    def new_game(self):
        self.show_level_selection(mode="new")

    def load_game(self):
        self.show_level_selection(mode="load")

    def show_level_selection(self, mode: str):
        if self.level_window and self.level_window.winfo_exists():
            self.level_window.focus_force()
            return

        w = tk.Toplevel(self.root)
        self.level_window = w
        w.title("Seleccionar Nivel")
        w.configure(bg=self.colors["bg"])
        w.resizable(False, False)
        w.transient(self.root)
        w.grab_set()

        card = ttk.Frame(w, style="Card.TFrame", padding=(18, 16))
        card.pack(fill="both", expand=True)

        title = "Nueva partida" if mode == "new" else "Cargar partida"
        ttk.Label(card, text=title, style="H2.TLabel").pack(anchor="w", pady=(0, 6))
        ttk.Label(card, text="Elige un nivel:", style="Muted.TLabel").pack(anchor="w", pady=(0, 12))

        levels = ["level_01.json", "level_02.json", "level_03.json"]

        for lvl in levels:
            ttk.Button(
                card,
                text=lvl,
                style="Menu.TButton",
                command=lambda l=lvl: self.start_with_level(l, mode, w),
            ).pack(fill="x", pady=6)

        ttk.Button(card, text="Cancelar", style="Menu.TButton", command=w.destroy).pack(fill="x", pady=(10, 0))

        self.center_window(w)

    def start_with_level(self, level_name: str, mode: str, window: tk.Toplevel):
        window.destroy()
        self.level_window = None

        if mode == "new":
            self.controller.start_new_gui(level_name)
            self.setup_game_screen()
        else:
            success = self.controller.load_game_gui(level_name)
            if success:
                self.setup_game_screen()
            else:
                messagebox.showerror("Error", f"No hay partida guardada para {level_name}")


    def setup_game_screen(self):
        self._replay_screen = False
        self.clear_window()
        state = self.controller.state

        outer = ttk.Frame(self.root)
        outer.pack(fill="both", expand=True, padx=12, pady=12)

        map_card = ttk.Frame(outer, style="Card.TFrame", padding=(12, 12))
        map_card.pack(side="left", fill="both", expand=True)

        ttk.Label(map_card, text=f"Nivel: {state.level_name}", style="Card.TLabel").pack(anchor="w", pady=(0, 8))

        canvas_holder = ttk.Frame(map_card, style="Card2.TFrame", padding=8)
        canvas_holder.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            canvas_holder,
            width=state.world.cols * self.cell_size,
            height=state.world.rows * self.cell_size,
            bg=self.colors["floor"],
            highlightthickness=0,
        )
        self.canvas.pack()

        info_card = ttk.Frame(outer, style="Card.TFrame", padding=(16, 16))
        info_card.pack(side="right", fill="y", padx=(12, 0))

        ttk.Label(info_card, text="Estado", style="H2.TLabel").pack(anchor="w", pady=(0, 8))

        self.status_label = ttk.Label(
            info_card,
            text=f"Llaves: 0/{self.controller.cfg.keys_required}",
            style="Card.TLabel",
            font=("Segoe UI", 13, "bold"),
        )
        self.status_label.pack(anchor="w", pady=(0, 10))

        ttk.Separator(info_card, orient="horizontal").pack(fill="x", pady=14)

        ttk.Label(info_card, text="Controles", style="H2.TLabel").pack(anchor="w", pady=(0, 6))
        ttk.Label(
            info_card,
            text="WASD  - Mover\nG     - Guardar\nQ     - Menú",
            style="Card.TLabel",
            justify="left",
        ).pack(anchor="w")

        self.root.bind("<Key>", self.handle_keypress)

        self.render_game()
        self.center_window()

    def render_game(self):
        if not self.canvas:
            return

        self.canvas.delete("all")
        state = self.controller.state

        rows, cols = state.world.rows, state.world.cols
        self._draw_grid(rows, cols)

        for r, c in state.walls:
            self.draw_cell(r, c, self.colors["wall"], shape="rect")

        dr, dc = state.level.door_pos
        self.draw_cell(dr, dc, self.colors["door"], shape="rect")

        for r, c in state.keys:
            self.draw_cell(r, c, self.colors["key"], shape="oval")

        for d in state.dragons.values():
            self.draw_cell(d.pos[0], d.pos[1], self.colors["dragon"], shape="rect")

        self.draw_cell(state.player[0], state.player[1], self.colors["player"], shape="oval")

        if self.status_label:
            self.status_label.config(text=f"Llaves: {state.keys_collected}/{self.controller.cfg.keys_required}")

    def _draw_grid(self, rows: int, cols: int):
        for r in range(rows + 1):
            y = r * self.cell_size
            self.canvas.create_line(0, y, cols * self.cell_size, y, fill=self.colors["grid"])
        for c in range(cols + 1):
            x = c * self.cell_size
            self.canvas.create_line(x, 0, x, rows * self.cell_size, fill=self.colors["grid"])

    def draw_cell(self, r: int, c: int, color: str, shape: str = "rect"):
        x1, y1 = c * self.cell_size, r * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size

        pad = 3
        if shape == "rect":
            self.canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill=color, outline="")
        else:
            self.canvas.create_oval(x1 + pad, y1 + pad, x2 - pad, y2 - pad, fill=color, outline="")

    def handle_keypress(self, event):
        key = (event.char or "").lower()

        if key in ["w", "a", "s", "d"]:
            status, event_type = self.controller.step_gui(key)
            self.render_game()

            if status == "death":
                messagebox.showinfo("Fin del Juego", "Un dragón te alcanzó.")
                self.setup_main_menu()

            elif status == "win":
                messagebox.showinfo("¡Victoria!", "¡Has escapado del calabozo!")
                self.show_win_options()

        elif key == "g":
            self.controller.save_game_gui()
            messagebox.showinfo("Guardado", "Partida guardada correctamente.")

        elif key == "q":
            self.setup_main_menu()

    def show_win_options(self):
        """
        Requisito: al completar el juego, ofrecer "Ver repetición".
        Replay: auto (velocidad) o paso a paso (tecla).
        """
        rec = getattr(self.controller, "rec", None)
        if rec is None or not getattr(rec, "frames", None):
            messagebox.showwarning("Replay", "No hay datos de replay (¿se está grabando la partida?).")
            self.setup_main_menu()
            return
        try:
            self.root.unbind("<Key>")
        except Exception:
            pass

        win = tk.Toplevel(self.root)
        win.title("Partida completada")
        win.configure(bg=self.colors["bg"])
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        card = ttk.Frame(win, style="Card.TFrame", padding=(18, 16))
        card.pack(fill="both", expand=True)

        ttk.Label(card, text="¡Victoria!", style="H2.TLabel").pack(anchor="w", pady=(0, 6))
        ttk.Label(card, text="¿Quieres ver la repetición de la partida?", style="Muted.TLabel").pack(anchor="w", pady=(0, 14))

        btns = ttk.Frame(card, style="Card.TFrame")
        btns.pack(fill="x")

        ttk.Button(btns, text="Ver replay (Automático)", style="Primary.TButton",
                   command=lambda: self._start_replay_from_win(win, mode="auto")).pack(fill="x", pady=6)

        ttk.Button(btns, text="Ver replay (Paso a paso)", style="Menu.TButton",
                   command=lambda: self._start_replay_from_win(win, mode="step")).pack(fill="x", pady=6)

        ttk.Button(btns, text="Volver al menú", style="Menu.TButton",
                   command=lambda: (win.destroy(), self.setup_main_menu())).pack(fill="x", pady=(10, 0))

        self.center_window(win)

    def _start_replay_from_win(self, win_dialog: tk.Toplevel, mode: str):
        win_dialog.destroy()

        state = self.controller.state
        rows, cols = state.world.rows, state.world.cols
        walls = set(state.walls)
        door_pos = tuple(state.level.door_pos)

        rec: ReplayRecorder = self.controller.rec
        replay_data = rec.to_dict(extra_meta={"door_pos": list(door_pos), "rows": rows, "cols": cols})

        self.start_replay_gui(replay_data, rows, cols, walls, door_pos, mode=mode)

    def start_replay_gui(self, replay_data, rows, cols, walls, door_pos, mode: str):
        """
        Pantalla replay que reproduce sin congelar.
        - auto: usa after con velocidad configurable
        - step: avanza con Space o Right Arrow
        """
        self._replay_data = replay_data
        self._replay_static = (rows, cols, walls, door_pos)
        self._replay_i = 0
        self._replay_mode = mode
        self._replay_running = True
        self._replay_screen = True

        self.clear_window()

        outer = ttk.Frame(self.root)
        outer.pack(fill="both", expand=True, padx=12, pady=12)

        map_card = ttk.Frame(outer, style="Card.TFrame", padding=(12, 12))
        map_card.pack(side="left", fill="both", expand=True)

        ttk.Label(map_card, text="REPLAY", style="Card.TLabel").pack(anchor="w", pady=(0, 8))

        canvas_holder = ttk.Frame(map_card, style="Card2.TFrame", padding=8)
        canvas_holder.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            canvas_holder,
            width=cols * self.cell_size,
            height=rows * self.cell_size,
            bg=self.colors["floor"],
            highlightthickness=0,
        )
        self.canvas.pack()

        info_card = ttk.Frame(outer, style="Card.TFrame", padding=(16, 16))
        info_card.pack(side="right", fill="y", padx=(12, 0))

        ttk.Label(info_card, text="Controles Replay", style="H2.TLabel").pack(anchor="w", pady=(0, 8))

        self.status_label = ttk.Label(
            info_card,
            text="Frame: 0/0",
            style="Card.TLabel",
            font=("Segoe UI", 12, "bold"),
        )
        self.status_label.pack(anchor="w", pady=(0, 10))

        ttk.Label(info_card, text=f"Modo: {mode.upper()}", style="Muted.TLabel").pack(anchor="w", pady=(0, 12))

        ttk.Label(info_card, text="Velocidad (ms/frame)", style="H2.TLabel").pack(anchor="w", pady=(0, 6))

        speed = tk.IntVar(value=self._replay_speed_ms)
        scale = ttk.Scale(
            info_card,
            from_=40,
            to=400,
            orient="horizontal",
            command=lambda v: self._set_replay_speed(int(float(v))),
        )
        scale.set(self._replay_speed_ms)
        scale.pack(fill="x", pady=(0, 10))

        speed_label = ttk.Label(info_card, text=f"{self._replay_speed_ms} ms", style="Card.TLabel")
        speed_label.pack(anchor="w", pady=(0, 12))

        def _sync_speed_label():
            speed_label.config(text=f"{self._replay_speed_ms} ms")
            if self._replay_screen:
                self.root.after(120, _sync_speed_label)
        _sync_speed_label()

        ttk.Separator(info_card, orient="horizontal").pack(fill="x", pady=14)

        ttk.Button(info_card, text="Reiniciar replay", style="Menu.TButton", command=self._replay_restart).pack(fill="x", pady=6)
        ttk.Button(info_card, text="Volver al menú", style="Menu.TButton", command=self.setup_main_menu).pack(fill="x", pady=6)

        self.root.bind("<Key>", self._handle_replay_keypress)

        self._render_replay_frame()
        if mode == "auto":
            self._replay_tick_auto()

        self.center_window()

    def _set_replay_speed(self, ms: int):
        self._replay_speed_ms = max(20, ms)

    def _replay_restart(self):
        self._replay_i = 0
        self._replay_running = True
        self._render_replay_frame()
        if self._replay_mode == "auto":
            self._replay_tick_auto()

    def _handle_replay_keypress(self, event):
        if not self._replay_screen:
            return

        k = event.keysym.lower()

        if self._replay_mode == "step":
            if k in ("space", "right", "return"):
                self._replay_i += 1
                self._render_replay_frame()
            elif k == "escape":
                self.setup_main_menu()

        else:
            if k == "space":
                self._replay_running = not self._replay_running
                if self._replay_running:
                    self._replay_tick_auto()
            elif k == "escape":
                self.setup_main_menu()

    def _replay_tick_auto(self):
        if not self._replay_screen:
            return
        if not self._replay_running:
            return

        self._replay_i += 1
        self._render_replay_frame()
        
        frames = self._replay_data["frames"]
        if self._replay_i >= len(frames) - 1:
            self._replay_running = False
            return

        self.root.after(self._replay_speed_ms, self._replay_tick_auto)

    def _render_replay_frame(self):
        if not self.canvas or not self._replay_data:
            return

        rows, cols, walls, door_pos = self._replay_static
        frames = self._replay_data["frames"]
        n = len(frames)

        i = max(0, min(self._replay_i, n - 1))
        fr = frames[i]

        keys_remaining = {tuple(k) for k in fr.get("keys_remaining", [])}
        player_pos = tuple(fr["player_pos"])
        dragons_pos = {k: tuple(v) for k, v in fr.get("dragons_pos", {}).items()}
        keys_collected = fr.get("keys_collected", 0)

        self.canvas.delete("all")
        self._draw_grid(rows, cols)

        for r, c in walls:
            self.draw_cell(r, c, self.colors["wall"], shape="rect")

        self.draw_cell(door_pos[0], door_pos[1], self.colors["door"], shape="rect")

        for r, c in keys_remaining:
            self.draw_cell(r, c, self.colors["key"], shape="oval")

        for _, pos in dragons_pos.items():
            self.draw_cell(pos[0], pos[1], self.colors["dragon"], shape="rect")

        self.draw_cell(player_pos[0], player_pos[1], self.colors["player"], shape="oval")


        if self.status_label:
            self.status_label.config(
                text=f"Frame: {i + 1}/{n} | Llaves: {keys_collected}/{self._replay_data['meta'].get('keys_required', '?')}"
            )

    def run(self):
        self.root.mainloop()


def choose_level_gui_dialog():
    return "level_01.json"


