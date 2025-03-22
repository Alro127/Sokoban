import numpy as np

class Player:
    def __init__(self, x, y):
        self.x = x  # Vị trí X của người chơi
        self.y = y  # Vị trí Y của người chơi

    def can_move(self, level_map, x, y):
        """Kiểm tra xem người chơi có thể di chuyển vào ô (x, y) không"""
        return level_map[x, y] in (" ", ".")

    def move(self, level_map, dx, dy):
        """Di chuyển người chơi hoặc đẩy hộp"""
        new_x = self.x + dx
        new_y = self.y + dy

        current_tile = level_map[self.x, self.y]  # Ô hiện tại của người chơi
        new_tile = level_map[new_x, new_y]  # Ô tiếp theo

        if self.can_move(level_map, new_x, new_y):
            # Cập nhật vị trí cũ của người chơi
            level_map[self.x, self.y] = "." if current_tile == "+" else " "
            
            # Cập nhật vị trí mới của người chơi
            level_map[new_x, new_y] = "+" if new_tile == "." else "@"
            
            # Cập nhật tọa độ người chơi
            self.x, self.y = new_x, new_y

        elif new_tile in ("$", "*"):  # Nếu là hộp hoặc hộp trên ô đích
            box_x = new_x + dx
            box_y = new_y + dy
            box_tile = level_map[box_x, box_y]  # Ô phía sau hộp

            if self.can_move(level_map, box_x, box_y):  # Nếu có thể đẩy hộp
                # Cập nhật ô cũ của hộp
                level_map[new_x, new_y] = "+" if new_tile == "*" else "@"
                
                # Cập nhật ô mới của hộp
                level_map[box_x, box_y] = "*" if box_tile == "." else "$"

                # Cập nhật ô cũ của người chơi
                level_map[self.x, self.y] = "." if current_tile == "+" else " "
                
                # Cập nhật vị trí người chơi
                self.x, self.y = new_x, new_y

    def check_win(self, level_map):
        """Kiểm tra nếu tất cả hộp đã vào vị trí mục tiêu"""
        return not np.any(level_map == "$") 
