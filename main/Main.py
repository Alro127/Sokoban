import pygame
import sys
from SokobanSolver import SokobanSolver
import Algorithms as agrm

# Cấu hình pygame
pygame.init()
WIDTH, HEIGHT = 600, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sokoban Menu")

# Load fonts
try:
    font = pygame.font.SysFont("segoeui", 28)
    header_font = pygame.font.SysFont("segoeui", 48, bold=True)
except:
    font = pygame.font.SysFont("Arial", 28)
    header_font = pygame.font.SysFont("Arial", 48, bold=True)

# Tùy chọn level và thuật toán
levels = [f"Level {i}" for i in range(20)]
algorithms = {"BFS": agrm.BFS, "DFS": agrm.BFS, "A*": agrm.BFS}

selected_level = 0
selected_algorithm_name = "BFS"

# Scroll offset
level_scroll_offset = 0
algorithm_scroll_offset = 0

# Các màu sắc hiện đại
BG_COLOR = (25, 25, 45)
PANEL_COLOR = (40, 40, 70)
TEXT_COLOR = (220, 220, 220)
HIGHLIGHT_COLOR = (100, 200, 250)
BUTTON_COLOR = (0, 180, 100)
BUTTON_HOVER = (0, 220, 130)

# Thông số giao diện
ITEM_HEIGHT = 40
VISIBLE_ITEMS = 5
SCROLL_SPEED = 1

# Các hàm vẽ giao diện
def draw_text(surface, text, pos, selected=False):
    color = HIGHLIGHT_COLOR if selected else TEXT_COLOR
    label = font.render(text, True, color)
    surface.blit(label, pos)

def draw_rounded_rect(surface, color, rect, radius=12):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def main_menu():
    global selected_level, selected_algorithm_name
    global level_scroll_offset, algorithm_scroll_offset

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BG_COLOR)

        # Header
        header = header_font.render("Sokoban Solver", True, (255, 215, 0))
        screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 20))

        # Panels
        level_panel = pygame.Rect(40, 100, 220, 200)
        algo_panel = pygame.Rect(340, 100, 220, 200)

        # Tạo surface tạm với alpha
        level_surface = pygame.Surface((level_panel.width, level_panel.height), pygame.SRCALPHA)
        algo_surface = pygame.Surface((algo_panel.width, algo_panel.height), pygame.SRCALPHA)

        # Vẽ panel bo góc lên surface
        draw_rounded_rect(level_surface, PANEL_COLOR, level_surface.get_rect(), radius=15)
        draw_rounded_rect(algo_surface, PANEL_COLOR, algo_surface.get_rect(), radius=15)

        # Vẽ tiêu đề vào surface
        draw_text(level_surface, "Level:", (20, 10))
        draw_text(algo_surface, "Algorithm:", (20, 10))

        # Vẽ levels lên level_surface
        start_idx = level_scroll_offset
        end_idx = min(start_idx + VISIBLE_ITEMS, len(levels))
        for idx, lvl in enumerate(levels[start_idx:end_idx]):
            y_pos = 50 + idx * ITEM_HEIGHT
            draw_text(level_surface, lvl, (40, y_pos), selected=(start_idx + idx == selected_level))

        # Vẽ algorithms lên algo_surface
        algo_keys = list(algorithms.keys())
        start_idx_a = algorithm_scroll_offset
        end_idx_a = min(start_idx_a + VISIBLE_ITEMS, len(algo_keys))
        for idx, algo in enumerate(algo_keys[start_idx_a:end_idx_a]):
            y_pos = 50 + idx * ITEM_HEIGHT
            draw_text(algo_surface, algo, (40, y_pos), selected=(algo == selected_algorithm_name))

        # Blit surface vào màn hình
        screen.blit(level_surface, (level_panel.x, level_panel.y))
        screen.blit(algo_surface, (algo_panel.x, algo_panel.y))

        # Vẽ nút Start
        start_rect = pygame.Rect(200, 340, 200, 60)
        mouse_pos = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse_pos):
            draw_rounded_rect(screen, BUTTON_HOVER, start_rect)
        else:
            draw_rounded_rect(screen, BUTTON_COLOR, start_rect)

        start_text = font.render("START", True, (255, 255, 255))
        screen.blit(start_text, (start_rect.centerx - start_text.get_width() // 2, start_rect.centery - start_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Kiểm tra chọn level
                if level_panel.collidepoint(x, y):
                    local_y = y - level_panel.top - 50
                    idx = local_y // ITEM_HEIGHT
                    real_idx = level_scroll_offset + idx
                    if 0 <= idx < VISIBLE_ITEMS and real_idx < len(levels):
                        selected_level = real_idx

                # Kiểm tra chọn thuật toán
                if algo_panel.collidepoint(x, y):
                    local_y = y - algo_panel.top - 50
                    idx = local_y // ITEM_HEIGHT
                    real_idx = algorithm_scroll_offset + idx
                    if 0 <= idx < VISIBLE_ITEMS and real_idx < len(algo_keys):
                        selected_algorithm_name = algo_keys[real_idx]

                # Kiểm tra click vào nút Start
                if start_rect.collidepoint(x, y):
                    solver = SokobanSolver(level_index=selected_level, algorithm_function=algorithms[selected_algorithm_name])
                    solver.solve()

            if event.type == pygame.MOUSEWHEEL:
                if level_panel.collidepoint(pygame.mouse.get_pos()):
                    level_scroll_offset -= event.y * SCROLL_SPEED
                    level_scroll_offset = max(0, min(level_scroll_offset, len(levels) - VISIBLE_ITEMS))
                if algo_panel.collidepoint(pygame.mouse.get_pos()):
                    algorithm_scroll_offset -= event.y * SCROLL_SPEED
                    algorithm_scroll_offset = max(0, min(algorithm_scroll_offset, len(algo_keys) - VISIBLE_ITEMS))

        clock.tick(60)

if __name__ == "__main__":
    main_menu()