import pygame
import sys
from SokobanSolver import SokobanSolver
import Algorithms as agrm

pygame.init()
WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sokoban Menu")

try:
    font = pygame.font.SysFont("segoeui", 28)
    header_font = pygame.font.SysFont("segoeui", 48, bold=True)
except:
    font = pygame.font.SysFont("Arial", 28)
    header_font = pygame.font.SysFont("Arial", 48, bold=True)

levels = [f"Level {i}" for i in range(3)]
algorithms = {"BFS": agrm.BFS, 
              "DFS": agrm.DFS, 
              "UCS": agrm.UCS,
              "IDS": agrm.IDS,
              "Greedy": agrm.Greedy,
              "A star": agrm.A_star,
              "IDA star": agrm.IDA_star,
              "A star advanced": agrm.A_star_advanced,
              "Backtracking with FC": agrm.backtracking_fc,
              "Q Learning":  agrm.q_learning,
              "Beam Search": agrm.beam_search}

selected_level = 0
selected_algorithm_name = "BFS"

level_scroll_offset = 0
algorithm_scroll_offset = 0

BG_COLOR = (25, 25, 45)
PANEL_COLOR = (40, 40, 70)
TEXT_COLOR = (220, 220, 220)
HIGHLIGHT_COLOR = (100, 200, 250)
BUTTON_COLOR = (0, 180, 100)
BUTTON_HOVER = (0, 220, 130)

ITEM_HEIGHT = 40
VISIBLE_ITEMS = 4
SCROLL_SPEED = 1

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

    algo_keys = list(algorithms.keys())

    while running:
        screen.fill(BG_COLOR)

        header = header_font.render("Sokoban Solver", True, (255, 215, 0))
        screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 20))

        level_panel = pygame.Rect(40, 100, 220, 240)
        algo_panel = pygame.Rect(340, 100, 440, 240)

        level_surface = pygame.Surface((level_panel.width, level_panel.height), pygame.SRCALPHA)
        algo_surface = pygame.Surface((algo_panel.width, algo_panel.height), pygame.SRCALPHA)

        draw_rounded_rect(level_surface, PANEL_COLOR, level_surface.get_rect(), radius=15)
        draw_rounded_rect(algo_surface, PANEL_COLOR, algo_surface.get_rect(), radius=15)

        draw_text(level_surface, "Level:", (20, 10))
        draw_text(algo_surface, "Algorithm:", (20, 10))

        start_idx = level_scroll_offset
        end_idx = min(start_idx + VISIBLE_ITEMS, len(levels))
        for idx, lvl in enumerate(levels[start_idx:end_idx]):
            y_pos = 50 + idx * ITEM_HEIGHT
            draw_text(level_surface, lvl, (40, y_pos), selected=(start_idx + idx == selected_level))

        start_idx_a = algorithm_scroll_offset
        end_idx_a = min(start_idx_a + VISIBLE_ITEMS, len(algo_keys))
        for idx, algo in enumerate(algo_keys[start_idx_a:end_idx_a]):
            y_pos = 50 + idx * ITEM_HEIGHT
            draw_text(algo_surface, algo, (40, y_pos), selected=(algo == selected_algorithm_name))

        screen.blit(level_surface, (level_panel.x, level_panel.y))
        screen.blit(algo_surface, (algo_panel.x, algo_panel.y))

        start_rect = pygame.Rect(200, 380, 200, 60)
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

                if level_panel.collidepoint(x, y):
                    local_y = y - level_panel.top - 50
                    if 0 <= local_y <= VISIBLE_ITEMS * ITEM_HEIGHT:
                        idx = local_y // ITEM_HEIGHT
                        real_idx = level_scroll_offset + idx
                        if real_idx < len(levels):
                            selected_level = real_idx

                if algo_panel.collidepoint(x, y):
                    local_y = y - algo_panel.top - 50
                    if 0 <= local_y <= VISIBLE_ITEMS * ITEM_HEIGHT:
                        idx = local_y // ITEM_HEIGHT
                        real_idx = algorithm_scroll_offset + idx
                        if real_idx < len(algo_keys):
                            selected_algorithm_name = algo_keys[real_idx]

                if start_rect.collidepoint(x, y):
                    solver = SokobanSolver(level_index=selected_level, algorithm_function=algorithms[selected_algorithm_name])
                    solver.solve()
                    pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

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
