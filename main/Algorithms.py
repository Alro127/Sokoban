from collections import deque
import time
import heapq
import numpy as np
import heapq
from collections import defaultdict
import time
from Node import Node


def BFS(start_node):
    queue = deque([start_node])
    visited = set()

    while queue:
        current = queue.popleft()

        if current.check_win():
            return current  # Trả về node để truy vết

        for next in current.get_valid_state():
            state_tuple = tuple(map(tuple, next.state))
            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            next.parent = current
            queue.append(next)

    return None

def DFS(start_node, max_steps=50):
    stack = [start_node]  
    visited = set()
    steps = 0  

    while stack:
        if steps > max_steps:
            print(f"Exceeded maximum steps ({max_steps}).")
            return None

        current = stack.pop()
        steps += 1

        if current.check_win():
            return current  # Trả về node để truy vết

        state_tuple = tuple(map(tuple, current.state))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        for next in current.get_valid_state():
            state_tuple_next = tuple(map(tuple, next.state))
            if state_tuple_next not in visited:
                next.parent = current
                stack.append(next)

    return None

def UCS(start_node):
    heap = []  # priority queue
    visited = set()

    start_node.depth = 0
    heapq.heappush(heap, (start_node.depth, id(start_node), start_node))

    while heap:
        current_depth, _, current = heapq.heappop(heap)

        if current.check_win():
            return current

        state_tuple = tuple(map(tuple, current.state))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        for next in current.get_valid_state():
            state_tuple_next = tuple(map(tuple, next.state))
            if state_tuple_next in visited:
                continue

            step_depth = 1  # hoặc tự tính theo hành động
            next.depth = current.depth + step_depth
            next.parent = current

            heapq.heappush(heap, (next.depth, id(next), next))

    return None

def IDS(start_node, max_depth=50):
    for depth_limit in range(max_depth):
        stack = [(start_node, 0)]  # (node, current_depth)
        visited = set()

        while stack:
            current, depth = stack.pop()

            if current.check_win():
                return current

            state_tuple = tuple(map(tuple, current.state))
            if state_tuple in visited:
                continue
            visited.add(state_tuple)

            if depth < depth_limit:
                for next in current.get_valid_state():
                    next.parent = current
                    stack.append((next, depth + 1))
    
    return None

def Greedy(start_node):
    heap = []
    visited = set()

    heapq.heappush(heap, (start_node.heuristic(), id(start_node), start_node))

    while heap:
        _, _, current = heapq.heappop(heap)

        if current.check_win():
            return current

        state_tuple = tuple(map(tuple, current.state))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        for next in current.get_valid_state():
            if tuple(map(tuple, next.state)) in visited:
                continue
            next.parent = current
            heapq.heappush(heap, (next.heuristic(), id(next), next))

    return None

def A_star(start_node):
    heap = []
    visited = set()

    start_node.depth = 0
    heapq.heappush(heap, (start_node.depth + start_node.heuristic(), id(start_node), start_node))

    while heap:
        current_f, _, current = heapq.heappop(heap)

        if current.check_win():
            return current

        state_tuple = tuple(map(tuple, current.state))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        for next in current.get_valid_state():
            if tuple(map(tuple, next.state)) in visited:
                continue

            step_depth = 1  # Giả sử mỗi bước tốn depth = 1
            next.depth = current.depth + step_depth
            next.parent = current

            f_score = next.depth + next.heuristic()
            heapq.heappush(heap, (f_score, id(next), next))

    return None

def IDA_star(start_node, timeout=10):
    def dfs(node, g, depth_limit, visited, start_time):
        if time.time() - start_time > timeout:
            raise TimeoutError("IDA* timeout exceeded.")

        f = g + node.heuristic()
        if f > depth_limit:
            return None, f
        if node.check_win():
            return node, f

        min_exceed = float('inf')
        state_tuple = tuple(map(tuple, node.state))
        visited.add(state_tuple)

        for next_node in node.get_valid_state():
            next_tuple = tuple(map(tuple, next_node.state))
            if next_tuple in visited:
                continue

            next_node.parent = node
            next_node.depth = g + 1
            try:
                found, temp_f = dfs(next_node, g + 1, depth_limit, visited, start_time)
            except TimeoutError:
                raise
            if found:
                return found, temp_f
            if temp_f < min_exceed:
                min_exceed = temp_f

        visited.remove(state_tuple)
        return None, min_exceed

    depth_limit = start_node.heuristic()
    start_time = time.time()

    while True:
        visited = set()
        try:
            result, new_limit = dfs(start_node, 0, depth_limit, visited, start_time)
        except TimeoutError:
            print("Timeout! IDA* did not finish.")
            return None

        if result:
            return result
        if new_limit == float('inf'):
            return None
        depth_limit = new_limit

def A_star_advanced(start_node):
    heap = []
    visited = dict()

    start_node.depth = 0
    heapq.heappush(heap, (start_node.depth + start_node.heuristic(), id(start_node), start_node))

    while heap:
        current_f, _, current = heapq.heappop(heap)

        if current.check_win():
            return current

        state_tuple = tuple(map(tuple, current.state))
        if state_tuple in visited and visited[state_tuple] <= current.depth:
            continue
        visited[state_tuple] = current.depth

        for next_node in current.get_valid_state():
            next_tuple = tuple(map(tuple, next_node.state))
            if next_tuple in visited and visited[next_tuple] <= current.depth + 1:
                continue

            # DEADLOCK DETECTION:
            if next_node.check_deadlock():
                continue  # Bỏ qua node kẹt

            next_node.parent = current
            next_node.depth = current.depth + 1

            f_score = next_node.depth + next_node.heuristic()
            heapq.heappush(heap, (f_score, id(next_node), next_node))

    return None

def backtracking_fc(node):
    # Kiểm tra nếu đã đạt mục tiêu
    if node.check_win():
        return node

    # Kiểm tra deadlock
    if node.check_deadlock() or node.depth > 200 :
        return None

    # Miền giá trị: Các node tiếp theo
    next_nodes = node.get_valid_state()

    # Duyệt qua từng node tiếp theo
    for next_node in next_nodes:
        next_node.depth += 1
        next_node.parent = node
        # Kiểm tra ràng buộc: Deadlock
        if not next_node.check_deadlock():
            result = backtracking_fc(next_node)
            if result:
                return result
            
class QLearning:
    def __init__(self, initial_state, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.initial_state = initial_state
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = {}

    def get_state_key(self, state):
        return str(state)

    def get_actions(self, node):
        return node.get_valid_state()

    def get_max_q_value(self, state_key):
        return max(self.q_table.get(state_key, {}).values(), default=0)

    def choose_action(self, node):
        state_key = self.get_state_key(node.state)
        if np.random.rand() < self.epsilon:
            actions = self.get_actions(node)
            return np.random.choice(actions) if actions else None

        if state_key in self.q_table:
            action_key = max(self.q_table[state_key], key=self.q_table[state_key].get)
            # Tìm Node tương ứng với action_key
            for action in self.get_actions(node):
                if self.get_state_key(action.state) == action_key:
                    return action
        return None

    def update_q_table(self, state_key, action_key, reward, next_state_key):
        old_q_value = self.q_table.get(state_key, {}).get(action_key, 0)
        future_reward = self.get_max_q_value(next_state_key)
        new_q_value = (1 - self.alpha) * old_q_value + self.alpha * (reward + self.gamma * future_reward)
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        self.q_table[state_key][action_key] = new_q_value

    def train(self, episodes=1000):
        for _ in range(episodes):
            node = self.initial_state
            while not node.check_win():
                state_key = self.get_state_key(node.state)
                action = self.choose_action(node)
                if not action:
                    break
                next_state_key = self.get_state_key(action.state)
                reward = self.calculate_reward(node, action)
                self.update_q_table(state_key, next_state_key, reward, next_state_key)
                node = action

    def calculate_reward(self, current_node, next_node):
        # Reward for winning the game
        if next_node.check_win():
            return 100

        # Penalty for deadlock
        if next_node.check_deadlock():
            return -1000

        # Calculate heuristic values
        current_heuristic = current_node.heuristic()
        next_heuristic = next_node.heuristic()

        # Reward/Penalty based on heuristic improvement
        if next_heuristic < current_heuristic:
            heuristic_reward = (current_heuristic - next_heuristic) * 5
        else:
            heuristic_reward = (current_heuristic - next_heuristic) * 2

        # Small penalty for each move to encourage shorter paths
        step_penalty = -1

        # Calculate total reward
        total_reward = heuristic_reward + step_penalty

        return total_reward

    def solve(self):
        node = self.initial_state
        while not node.check_win():
            action = self.choose_action(node)
            if not action:
                break
            action.parent = node
            node = action
        return node


def q_learning(initial_state):
    ql = QLearning(initial_state, alpha=0.1, gamma=0.9, epsilon=0.1)
    ql.train(episodes=1000)
    return ql.solve()

def beam_search(start_node, beam_width=30, max_depth=500):

    try:
        start_time = time.time()
        
        # Khởi tạo beam với node bắt đầu
        current_beam = [start_node]
        visited = set()
        best_nodes = []  # Lưu các node tốt nhất đã tìm thấy
        best_heuristic = float('inf')  # Lưu heuristic tốt nhất đã tìm thấy
        no_improvement_count = 0  # Đếm số lần không cải thiện
        
        depth = 0
        while current_beam and depth < max_depth:
            if time.time() - start_time > 60:  # Tăng timeout lên 60 giây
                print("Search timeout reached. Returning best solution found.")
                break
                
            next_beam = []
            depth += 1
        
            # Duyệt qua tất cả các node trong beam hiện tại
            for current in current_beam:
                if current.check_win():
                    
                    return current
                    
                # Lấy tất cả các trạng thái tiếp theo
                for next_node in current.get_valid_state():
                    state_tuple = tuple(map(tuple, next_node.state))
                    if state_tuple in visited:
                        continue
                        
                    # Kiểm tra deadlock
                    if next_node.check_deadlock():
                        continue
                        
                    visited.add(state_tuple)
                    next_node.parent = current
                    next_node.depth = depth
                    
                    # Tính f-score = g(n) + h(n) + p(n)
                    h_score = next_node.heuristic()
                    g_score = depth
                    p_score = 0
                    
                    # Cập nhật heuristic tốt nhất
                    if h_score < best_heuristic:
                        best_heuristic = h_score
                        no_improvement_count = 0
                        
                    else:
                        no_improvement_count += 1
                    
                    # Thêm penalty cho các trạng thái không mong muốn
                    if h_score > current.heuristic():  # Nếu heuristic xấu đi
                        p_score = 0.5  # Giảm penalty để cho phép khám phá nhiều hơn
                    
                    f_score = g_score + h_score + p_score
                    heapq.heappush(next_beam, (f_score, id(next_node), next_node))
                    
                    # Lưu node tốt nhất
                    if h_score < best_heuristic + 5:  # Mở rộng điều kiện lưu node tốt
                        best_nodes.append((h_score, next_node))
            
            # Chọn k node tốt nhất cho beam tiếp theo
            current_beam = []
            for _ in range(min(beam_width, len(next_beam))):
                if next_beam:
                    _, _, node = heapq.heappop(next_beam)
                    current_beam.append(node)
            
            # Nếu không có node nào trong beam tiếp theo hoặc không cải thiện trong thời gian dài
            if (not current_beam or no_improvement_count > 50) and best_nodes:
                # Sắp xếp các node tốt nhất theo heuristic
                best_nodes.sort(key=lambda x: x[0])
                
                # Lấy một số node tốt nhất để thử lại
                num_nodes_to_try = min(10, len(best_nodes))
                current_beam = [node for _, node in best_nodes[:num_nodes_to_try]]
                best_nodes = best_nodes[num_nodes_to_try:]  # Giữ lại các node còn lại
                
                # Reset counter
                no_improvement_count = 0
                
                # Nếu best_nodes quá lớn, chỉ giữ lại một số node tốt nhất
                if len(best_nodes) > 100:
                    best_nodes = best_nodes[:50]
                continue
        
        
        # Nếu không tìm thấy giải pháp, trả về node tốt nhất đã tìm được
        if best_nodes:
            best_nodes.sort(key=lambda x: x[0])
           
            return best_nodes[0][1]
        
        # Nếu không có node tốt nào, trả về node cuối cùng trong beam
        if current_beam:
            return current_beam[0]
            
        return None
        
    except Exception as e:
        print(f"Error in beam_search: {str(e)}")
        # Trả về node tốt nhất đã tìm được nếu có lỗi
        if best_nodes:
            best_nodes.sort(key=lambda x: x[0])
            print(f"Returning best node after error with heuristic: {best_nodes[0][0]}")
            return best_nodes[0][1]
        return None
