import pygame
import numpy as np
import timeit
import tracemalloc

import Levels as lv
import Algorithms as agrm
from Node import Node

class SokobanSolver:
    TILE_SIZE = 64

    def __init__(self, level_index, algorithm_function):
        pygame.init()

        self.level_index = level_index
        self.algorithm_function = algorithm_function

        self.level_map = np.array([list(row) for row in lv.levels[self.level_index]])
        self.ROWS = len(self.level_map)
        self.COLS = max(len(row) for row in self.level_map)
        self.WIDTH, self.HEIGHT = self.COLS * self.TILE_SIZE, self.ROWS * self.TILE_SIZE

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)

        pygame.display.set_caption(f"Sokoban - Level {self.level_index}")

        self.load_images()

    def load_images(self):
        images = lv.level_img[0]
        self.wall_img = pygame.transform.scale(pygame.image.load(images["wall"]), (self.TILE_SIZE, self.TILE_SIZE))
        self.floor_img = pygame.transform.scale(pygame.image.load(images["floor"]), (self.TILE_SIZE, self.TILE_SIZE))
        self.goal_img = pygame.transform.scale(pygame.image.load(images["goal"]), (self.TILE_SIZE, self.TILE_SIZE))
        self.box_img = pygame.transform.scale(pygame.image.load(images["box"]), (self.TILE_SIZE, self.TILE_SIZE))

        # Load player images
        self.player_imgs = {
            "up": pygame.transform.scale(pygame.image.load(images["player_up"]), (self.TILE_SIZE, self.TILE_SIZE)),
            "down": pygame.transform.scale(pygame.image.load(images["player_down"]), (self.TILE_SIZE, self.TILE_SIZE)),
            "left": pygame.transform.scale(pygame.image.load(images["player_left"]), (self.TILE_SIZE, self.TILE_SIZE)),
            "right": pygame.transform.scale(pygame.image.load(images["player_right"]), (self.TILE_SIZE, self.TILE_SIZE)),
        }

    def draw_map(self, state, prev_state=None):
        self.screen.fill((255, 255, 255))

        for row in range(self.ROWS):
            for col in range(self.COLS):
                if col >= len(state[row]):
                    continue

                tile = state[row][col]
                x, y = col * self.TILE_SIZE, row * self.TILE_SIZE

                self.screen.blit(self.floor_img, (x, y))

                if tile == "#":
                    self.screen.blit(self.wall_img, (x, y))
                elif tile == ".":
                    self.screen.blit(self.goal_img, (x, y))
                elif tile in ["$", "*"]:
                    self.screen.blit(self.box_img, (x, y))

        # Xác định hướng nhân vật
        direction = "down"  # mặc định hướng xuống

        if prev_state is not None:
            curr_player = self.find_pos(state, ["@", "+"])
            prev_player = self.find_pos(prev_state, ["@", "+"])

            dx, dy = curr_player[1] - prev_player[1], curr_player[0] - prev_player[0]

            if dx == 1:
                direction = "right"
            elif dx == -1:
                direction = "left"
            elif dy == -1:
                direction = "up"
            elif dy == 1:
                direction = "down"

        curr_player = self.find_pos(state, ["@", "+"])
        self.screen.blit(self.player_imgs[direction], (curr_player[1] * self.TILE_SIZE, curr_player[0] * self.TILE_SIZE))

    def find_pos(self, state, symbols):
        for y, row in enumerate(state):
            for x, char in enumerate(row):
                if char in symbols:
                    return (y, x)
        return None

    def reconstruct_path(self, start_node, goal_node):
        if goal_node is None:
            return []
        path = []
        while goal_node:
            path.append(goal_node)
            if goal_node == start_node:
                break
            goal_node = goal_node.parent
        return path[::-1]

    def solve(self):
        start_node = Node(self.level_map)

        # Bắt đầu đo thời gian và bộ nhớ
        tracemalloc.start()
        start_time = timeit.default_timer()

        goal_node = self.algorithm_function(start_node)

        end_time = timeit.default_timer()
        memory_used, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Thời gian thực thi thuật toán: {(end_time - start_time):.5f} giây")
        print(f"Bộ nhớ sử dụng: {memory_used / (1024 ** 2):.5f} MB")
        print(f"Bộ nhớ tối đa: {peak_memory / (1024 ** 2):.5f} MB")

        if goal_node is not None:
            clock = pygame.time.Clock()
            path = self.reconstruct_path(start_node, goal_node)

            prev_state = None
            for node in path:
                self.draw_map(node.state, prev_state)
                prev_state = node.state
                pygame.display.flip()
                clock.tick(30)

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
        else:
            print("Không tìm thấy đường đi!")
