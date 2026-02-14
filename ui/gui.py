import tkinter as tk
from tkinter import messagebox
from world.types import Direction, TileType
import time

class GameGUI:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Calabozo Místico")
        
        self.colors = {
            "wall": "#2c3e50",
            "floor": "#ecf0f1",
            "player": "#e74c3c",
            "dragon": "#8e44ad",
            "key": "#f1c40f",
            "door": "#27ae60",
            "text": "#ffffff",
            "bg": "#34495e"
        }
        
        self.cell_size = 30
        self.canvas = None
        self.status_label = None
        
        self.setup_main_menu()

    
    def setup_main_menu(self):
        self.clear_window()
        self.root.configure(bg=self.colors["bg"])
        
        frame = tk.Frame(self.root, bg=self.colors["bg"])
        frame.pack(expand=True)
        
        tk.Label(frame, text="CALABOZO MÍSTICO", font=("Helvetica", 24, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["text"]).pack(pady=20)
        
        btn_style = {"font": ("Helvetica", 12), "width": 20, "pady": 10}
        
        tk.Button(frame, text="Nueva Partida", command=self.new_game, **btn_style).pack(pady=5)
        tk.Button(frame, text="Cargar Partida", command=self.load_game, **btn_style).pack(pady=5)
        tk.Button(frame, text="Salir", command=self.root.quit, **btn_style).pack(pady=5)

        self.center_window()

    def center_window(self):

        self.root.geometry("") 
        self.root.update_idletasks()
        
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        
        self.root.geometry(f'+{x}+{y}')


    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def new_game(self):
        self.show_level_selection(mode="new")

    def load_game(self):
        self.show_level_selection(mode="load")

    def show_level_selection(self, mode):
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Seleccionar Nivel")
        selection_window.configure(bg=self.colors["bg"])
        
        levels = ["level_01.json", "level_02.json", "level_03.json"]
        
        tk.Label(selection_window, text="Elige un nivel:", font=("Helvetica", 12), 
                 bg=self.colors["bg"], fg=self.colors["text"]).pack(pady=10)
        
        for lvl in levels:
            tk.Button(selection_window, text=lvl, width=20,
                      command=lambda l=lvl: self.start_with_level(l, mode, selection_window)).pack(pady=5, padx=20)
           

    def start_with_level(self, level_name, mode, window):
        window.destroy()
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
        self.clear_window()
        state = self.controller.state
        
        self.root.bind("<Key>", self.handle_keypress)
        
        # Panel info
        info_panel = tk.Frame(self.root, bg=self.colors["bg"], width=200)
        info_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        self.status_label = tk.Label(info_panel, text=f"Llaves: 0/{self.controller.cfg.keys_required}", 
                                     font=("Helvetica", 14), bg=self.colors["bg"], fg=self.colors["text"])
        self.status_label.pack(pady=20)
        
        tk.Label(info_panel, text="Controles:\nWASD - Mover\nG - Guardar\nQ - Salir", 
                 font=("Helvetica", 10), bg=self.colors["bg"], fg=self.colors["text"], justify=tk.LEFT).pack(pady=20)

        # Canvas para el mapa
        self.canvas = tk.Canvas(self.root, width=state.world.cols * self.cell_size, 
                                height=state.world.rows * self.cell_size, bg=self.colors["floor"])
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.render_game()

        self.center_window()

    def render_game(self):
        if not self.canvas: return
        self.canvas.delete("all")
        state = self.controller.state
        
        # paredes
        for r, c in state.walls:
            self.draw_cell(r, c, self.colors["wall"])
            
        # puerta
        dr, dc = state.level.door_pos
        self.draw_cell(dr, dc, self.colors["door"])
        
        #  llaves
        for r, c in state.keys:
            self.draw_cell(r, c, self.colors["key"], "oval")
            
        # dragones
        for d in state.dragons.values():
            self.draw_cell(d.pos[0], d.pos[1], self.colors["dragon"])
            
        #jugador
        self.draw_cell(state.player[0], state.player[1], self.colors["player"], "oval")
        
        self.status_label.config(text=f"Llaves: {state.keys_collected}/{self.controller.cfg.keys_required}")

    def draw_cell(self, r, c, color, shape="rect"):
        x1, y1 = c * self.cell_size, r * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        if shape == "rect":
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")
        else:
            self.canvas.create_oval(x1+2, y1+2, x2-2, y2-2, fill=color, outline="white")

    def handle_keypress(self, event):
        key = event.char.lower()
        if key in ['w', 'a', 's', 'd']:
            status, event_type = self.controller.step_gui(key)
            self.render_game()
            if status == "death":
                messagebox.showinfo("Fin del Juego", " Un dragón te alcanzó.")
                self.post_game_options()
            elif status == "win":
                messagebox.showinfo("¡Victoria!", " ¡Has escapado del calabozo!")
                self.post_game_options()
        elif key == 'g':
            self.controller.save_game_gui()
            messagebox.showinfo("Guardado", "Partida guardada correctamente.")
        elif key == 'q':
            self.setup_main_menu()

    def post_game_options(self):
        self.setup_main_menu()

    def run(self):
        self.root.mainloop()

def choose_level_gui_dialog():
    return "level_01.json"
