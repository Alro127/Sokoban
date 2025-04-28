import pygame
import numpy as np

import Levels as lv
from Player import Player
import Algorithms as agrm
from Node import Node

# Khởi tạo pygames
pygame.init()

# Kích thước ô vuông
TILE_SIZE = 64  # Tăng kích thước ô để hiển thị rõ hơn

level_map = np.array([list(row) for row in lv.levels[2]])

# Xác định kích thước màn hình
ROWS = len(level_map)
COLS = max(len(row) for row in level_map)
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE

# Tạo cửa sổ game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sokoban - Level 1")

def load_level_images(level_index):
    """Tải hình ảnh của level hiện tại"""
    paths = lv.level_img[level_index]
    return {
        "wall": pygame.image.load(paths["wall"]),
        "floor": pygame.image.load(paths["floor"]),
        "goal": pygame.image.load(paths["goal"]),
        "box": pygame.image.load(paths["box"]),
        "player": pygame.image.load(paths["player"])
    }

images = load_level_images(0)

# Thay đổi kích thước ảnh cho phù hợp
wall_img = pygame.transform.scale(images["wall"], (TILE_SIZE, TILE_SIZE))
floor_img = pygame.transform.scale(images["floor"], (TILE_SIZE, TILE_SIZE))
goal_img = pygame.transform.scale(images["goal"], (TILE_SIZE, TILE_SIZE))
box_img = pygame.transform.scale(images["box"], (TILE_SIZE, TILE_SIZE))
player_img = pygame.transform.scale(images["player"], (TILE_SIZE, TILE_SIZE))

# Hàm vẽ bản đồ
def draw_map(state):
    screen.fill((255, 255, 255))  # Xóa màn hình

    for row in range(ROWS):
        for col in range(COLS):
            if col >= len(state[row]):  
                continue  # Bỏ qua nếu cột vượt quá độ dài của dòng

            tile = state[row][col]
            x, y = col * TILE_SIZE, row * TILE_SIZE

            # Vẽ sàn trước để tạo nền
            screen.blit(floor_img, (x, y))

            # Vẽ từng loại đối tượng
            if tile == "#":
                screen.blit(wall_img, (x, y))  # Vẽ tường
            elif tile == ".":
                screen.blit(goal_img, (x, y))  # Vẽ điểm đích
            elif tile == "$" or tile == "*":
                screen.blit(box_img, (x, y))  # Vẽ hộp
            elif tile == "@" or tile == "+":
                screen.blit(player_img, (x, y))  # Vẽ nhân vật


def reconstruct_path(start_node, goal_node):
    if goal_node is None:
        return []  # Không có đường đi

    path = []
    while goal_node:
        path.append(goal_node)
        if goal_node == start_node:
            break
        goal_node = goal_node.parent

    return path[::-1]  # Trả về đường đi ngược


start_node = Node(level_map)
goal_node = agrm.BFS(start_node)

if goal_node is not None:

    clock = pygame.time.Clock()
    path = reconstruct_path(start_node, goal_node)  

    for node in path:
        draw_map(node.state)
        pygame.display.flip()
        clock.tick(30)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  
    pygame.quit()
else:
    print("Không tìm thấy đường đi!")