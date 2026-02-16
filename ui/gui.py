import pygame
import sys
import time
import os
from world.types import Direction, TileType

class GameGUI:
    def __init__(self, controller):
        self.controller = controller
        pygame.init()
        pygame.display.set_caption("Calabozo Místico")
        
        # Paleta de colores profesional
        self.colors = {
            "wall": (44, 62, 80),      # Azul oscuro
            "floor": (236, 240, 241),   # Blanco grisáceo
            "player": (231, 76, 60),    # Rojo
            "dragon": (142, 68, 173),   # Púrpura
            "key": (241, 196, 15),      # Dorado
            "door": (39, 174, 96),      # Verde
            "text": (255, 255, 255),    # Blanco
            "bg": (52, 73, 94),         # Gris azulado
            "panel": (44, 62, 80),
            "button": (44, 62, 80),
            "button_hover": (60, 80, 100)
        }
        
        self.cell_size = 30
        self.font = pygame.font.SysFont("Helvetica", 24, bold=True)
        self.small_font = pygame.font.SysFont("Helvetica", 18)
        self.screen = None
        self.clock = pygame.time.Clock()
        self.running = True
        self.mode = "menu" # "menu", "level_select", "game", "replay"
        self.pending_action = None # "new" o "load"
        self.replay_data = None
        self.replay_index = 0

    def center_window(self, width, height):
        self.screen = pygame.display.set_mode((width, height))

    def draw_text(self, text, x, y, color=None, center=False, font=None):
        if color is None: color = self.colors["text"]
        if font is None: font = self.font
        img = font.render(text, True, color)
        rect = img.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(img, rect)

    def main_menu(self):
        self.center_window(400, 450)
        self.mode = "menu"
        while self.mode == "menu":
            self.screen.fill(self.colors["bg"])
            self.draw_text("CALABOZO MÍSTICO", 200, 80, center=True)
            
            self.draw_button("Nueva Partida", 200, 180, 220, 45, lambda: self.prepare_level_select("new"))
            self.draw_button("Cargar Partida", 200, 250, 220, 45, lambda: self.prepare_level_select("load"))
            self.draw_button("Salir", 200, 320, 220, 45, sys.exit)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            pygame.display.flip()
            self.clock.tick(30)

    def draw_button(self, text, x, y, w, h, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(0, 0, w, h)
        rect.center = (x, y)
        
        if rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, self.colors["button_hover"], rect, border_radius=5)
            if click[0] == 1 and action:
                time.sleep(0.15)
                action()
        else:
            pygame.draw.rect(self.screen, self.colors["button"], rect, border_radius=5)
        
        self.draw_text(text, x, y, center=True, font=self.small_font)

    def prepare_level_select(self, action_type):
        self.pending_action = action_type
        self.mode = "level_select"
        self.show_level_selection()

    def show_level_selection(self):
        # Escanear niveles disponibles
        levels_dir = "levels"
        try:
            levels = [f for f in os.listdir(levels_dir) if f.endswith(".json")]
            levels.sort()
        except Exception:
            levels = []

        self.center_window(400, 150 + (len(levels) * 60))
        
        while self.mode == "level_select":
            self.screen.fill(self.colors["bg"])
            title = "Seleccionar Nivel" if self.pending_action == "new" else "Cargar Nivel"
            self.draw_text(title, 200, 50, center=True)
            
            y_offset = 120
            for lvl in levels:
                display_name = lvl.replace(".json", "").replace("_", " ").title()
                self.draw_button(display_name, 200, y_offset, 250, 40, lambda l=lvl: self.start_game(l))
                y_offset += 60
            
            self.draw_button("Volver", 200, y_offset + 20, 150, 35, self.main_menu)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.main_menu()
            
            pygame.display.flip()
            self.clock.tick(30)

    def start_game(self, level_name):
        if self.pending_action == "new":
            self.controller.start_new_gui(level_name)
        else:
            if not self.controller.load_game_gui(level_name):
                # Si falla la carga, podríamos mostrar un mensaje temporalmente
                print(f"Error: No hay partida guardada para {level_name}")
                return
        
        self.mode = "game"
        self.run_game()

    def run_game(self):
        state = self.controller.state
        width = state.world.cols * self.cell_size + 200
        height = state.world.rows * self.cell_size
        self.center_window(width, height)
        
        while self.mode == "game":
            self.screen.fill(self.colors["floor"])
            self.render_world()
            self.draw_ui_panel()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    key_map = {pygame.K_w: 'w', pygame.K_a: 'a', pygame.K_s: 's', pygame.K_d: 'd'}
                    if event.key in key_map:
                        status, _ = self.controller.step_gui(key_map[event.key])
                        if status in ["win", "death"]:
                            self.controller.finish_replay_gui(status)
                            self.end_screen(status)
                    elif event.key == pygame.K_g:
                        self.controller.save_game_gui()
                        # Feedback visual simple para el guardado
                        self.draw_text("¡Guardado!", self.screen.get_width() - 100, 250, color=(46, 204, 113), font=self.small_font)
                        pygame.display.flip()
                        time.sleep(0.5)
                    elif event.key == pygame.K_q:
                        self.main_menu()
            
            pygame.display.flip()
            self.clock.tick(30)

    def render_world(self):
            """Dibuja el grid y todas las entidades."""
            state = self.controller.state
            
            # 1. Dibujar el Suelo (Fondo)
            self.screen.fill(self.colors["floor"])

            # 2. DIBUJAR LA CUADRÍCULA (GRID) - Nueva parte estética
            grid_color = (200, 200, 200) # Gris claro para las líneas
            for r in range(state.world.rows + 1):
                pygame.draw.line(self.screen, grid_color, (0, r * self.cell_size), (state.world.cols * self.cell_size, r * self.cell_size), 1)
            for c in range(state.world.cols + 1):
                pygame.draw.line(self.screen, grid_color, (c * self.cell_size, 0), (c * self.cell_size, state.world.rows * self.cell_size), 1)

            # 3. Dibujar Paredes
            for r, c in state.walls:
                pygame.draw.rect(self.screen, self.colors["wall"], (c*self.cell_size, r*self.cell_size, self.cell_size, self.cell_size))
            
            # 4. Dibujar Puerta
            dr, dc = state.level.door_pos
            pygame.draw.rect(self.screen, self.colors["door"], (dc*self.cell_size, dr*self.cell_size, self.cell_size, self.cell_size))
            
            # 5. Dibujar Llaves
            for r, c in state.keys:
                pygame.draw.circle(self.screen, self.colors["key"], (c*self.cell_size + self.cell_size//2, r*self.cell_size + self.cell_size//2), self.cell_size//3)
                
            # 6. Dibujar Dragones
            for d in state.dragons.values():
                pygame.draw.rect(self.screen, self.colors["dragon"], (d.pos[1]*self.cell_size, d.pos[0]*self.cell_size, self.cell_size, self.cell_size))
                
            # 7. Dibujar Jugador
            pygame.draw.circle(self.screen, self.colors["player"], (state.player[1]*self.cell_size + self.cell_size//2, state.player[0]*self.cell_size + self.cell_size//2), self.cell_size//2 - 2)

    def draw_ui_panel(self):
        state = self.controller.state
        panel_x = state.world.cols * self.cell_size
        pygame.draw.rect(self.screen, self.colors["panel"], (panel_x, 0, 200, self.screen.get_height()))
        
        self.draw_text("ESTADO", panel_x + 20, 30, color=(200, 200, 200), font=self.small_font)
        self.draw_text(f"Nivel: {state.level_name.split('.')[0]}", panel_x + 20, 60, font=self.small_font)
        self.draw_text(f"Llaves: {state.keys_collected}/{self.controller.cfg.keys_required}", panel_x + 20, 90, font=self.small_font)
        
        self.draw_text("CONTROLES", panel_x + 20, 160, color=(200, 200, 200), font=self.small_font)
        self.draw_text("WASD - Mover", panel_x + 20, 190, font=self.small_font)
        self.draw_text("G - Guardar", panel_x + 20, 220, font=self.small_font)
        self.draw_text("Q - Salir", panel_x + 20, 250, font=self.small_font)

    def end_screen(self, status):
        self.center_window(400, 350)
        while True:
            self.screen.fill(self.colors["bg"])
            msg = "¡HAS GANADO!" if status == "win" else "HAS MUERTO..."
            color = self.colors["door"] if status == "win" else self.colors["player"]
            self.draw_text(msg, 200, 80, center=True, color=color)
            
            self.draw_button("Ver Repetición", 200, 180, 220, 45, self.start_replay)
            self.draw_button("Menú Principal", 200, 250, 220, 45, self.main_menu)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            pygame.display.flip()
            self.clock.tick(30)

    def start_replay(self):
        last_replay_path = self.controller.cfg.replay_path_for(self.controller.state.level_name)
        from replay.replay_system import load_replay
        try:
            self.replay_data = load_replay(last_replay_path)
            self.replay_index = 0
            self.mode = "replay"
            self.run_replay()
        except Exception:
            self.main_menu()

    def run_replay(self):
        frames = self.replay_data["frames"]
        state = self.controller.state
        width = state.world.cols * self.cell_size + 200
        height = state.world.rows * self.cell_size
        self.center_window(width, height)
        
        while self.mode == "replay":
            if self.replay_index < len(frames):
                self.screen.fill(self.colors["floor"])
                fr = frames[self.replay_index]
                
                # Renderizado estático
                for r, c in state.walls:
                    pygame.draw.rect(self.screen, self.colors["wall"], (c*self.cell_size, r*self.cell_size, self.cell_size, self.cell_size))
                dr, dc = state.level.door_pos
                pygame.draw.rect(self.screen, self.colors["door"], (dc*self.cell_size, dr*self.cell_size, self.cell_size, self.cell_size))
                
                # Renderizado dinámico del replay
                for r, c in fr["keys_remaining"]:
                    pygame.draw.circle(self.screen, self.colors["key"], (c*self.cell_size + self.cell_size//2, r*self.cell_size + self.cell_size//2), self.cell_size//3)
                for k, pos in fr["dragons_pos"].items():
                    pygame.draw.rect(self.screen, self.colors["dragon"], (pos[1]*self.cell_size, pos[0]*self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.circle(self.screen, self.colors["player"], (fr["player_pos"][1]*self.cell_size + self.cell_size//2, fr["player_pos"][0]*self.cell_size + self.cell_size//2), self.cell_size//2 - 2)
                
                # Panel de Replay
                pygame.draw.rect(self.screen, self.colors["panel"], (state.world.cols * self.cell_size, 0, 200, height))
                self.draw_text("MODO REPLAY", state.world.cols * self.cell_size + 20, 50, color=(46, 204, 113), font=self.small_font)
                self.draw_text(f"Frame: {self.replay_index+1}", state.world.cols * self.cell_size + 20, 80, font=self.small_font)
                self.draw_text("Presiona Q para salir", state.world.cols * self.cell_size + 20, 150, font=self.small_font, color=(200, 200, 200))
                
                self.replay_index += 1
                pygame.display.flip()
                time.sleep(self.controller.cfg.replay_delay)
            else:
                self.main_menu()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.main_menu()
            self.clock.tick(30)

    def run(self):
        self.main_menu()