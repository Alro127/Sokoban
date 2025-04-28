import numpy as np

class Node():
    def __init__(self, state, parent=None, move_direction=None, cost=0):
        self.state = state
        self.parent = parent
        self.move_direction = move_direction 
        self.heuristic = 0
        self.cost = cost

    def can_move(self, x, y):
        """Kiểm tra xem người chơi có thể di chuyển vào ô (x, y) không"""
        return str(self.state[x, y]) in (" ", ".") 

    def copy(self):
        """Tạo bản sao của trạng thái"""
        return Node(self.state.copy(), self.parent, self.move_direction, self.cost)

    def move(self, player_x, player_y, dx, dy):
        new_x = player_x + dx
        new_y = player_y + dy

        new_node = self.copy()
        current_tile = str(self.state[player_x, player_y])  # Ô hiện tại của người chơi
        new_tile = str(self.state[new_x, new_y])  # Ô tiếp theo

        if self.can_move(new_x, new_y):
            # Cập nhật vị trí cũ của người chơi
            new_node.state[player_x, player_y] = "." if current_tile == "+" else " "
            # Cập nhật vị trí mới của người chơi
            new_node.state[new_x, new_y] = "+" if new_tile == "." else "@"
        
        elif new_tile in ("$", "*"):  # Nếu là hộp hoặc hộp trên ô đích
            box_x = new_x + dx
            box_y = new_y + dy
            
            box_tile = str(self.state[box_x, box_y])  # Ô phía sau hộp

            if not self.can_move(box_x, box_y): 
                return None  # Hộp không thể di chuyển

            # Cập nhật ô cũ của hộp
            new_node.state[new_x, new_y] = "+" if new_tile == "*" else "@"
            # Cập nhật ô mới của hộp
            new_node.state[box_x, box_y] = "*" if box_tile == "." else "$"
            # Cập nhật ô cũ của người chơi
            new_node.state[player_x, player_y] = "." if current_tile == "+" else " "

        else:
            return None  # Không thể di chuyển

        return new_node

    def get_valid_state(self):
        """Lấy danh sách các trạng thái hợp lệ sau khi di chuyển"""
        moves = []
        x, y = np.where((self.state == '@') | (self.state == '+'))
        x, y = x[0], y[0]  # Lấy tọa độ người chơi

        directions = {
            "Up": (-1, 0),
            "Down": (1, 0),
            "Left": (0, -1),
            "Right": (0, 1)
        }

        for move_direction, (dx, dy) in directions.items():
            new_state = self.move(x, y, dx, dy)
            if new_state:
                moves.append(new_state)

        return moves

    def check_win(self):
        """Kiểm tra nếu tất cả hộp đã vào vị trí mục tiêu"""
        return not np.any(self.state == "$")  
    
    def get_path(self):
        path = []
        node = self
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]
