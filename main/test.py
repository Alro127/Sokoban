import numpy as np
from Node import Node

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
        if next_node.check_win():
            return 100
        if next_node.check_deadlock():
            return -1000
        current_heuristic = current_node.heuristic()
        next_heuristic = next_node.heuristic()
        if next_heuristic < current_heuristic:
            return 10
        elif next_heuristic > current_heuristic:
            return -5
        return -1

    def solve(self):
        node = self.initial_state
        steps = []
        while not node.check_win():
            action = self.choose_action(node)
            if not action:
                break
            steps.append(action)
            node = action
        print("Steps:")
        for i, step in enumerate(steps):
            print(f"Step {i + 1}: {step.state}")
        return node


def q_learning(initial_state):
    ql = QLearning(initial_state, alpha=0.1, gamma=0.9, epsilon=0.1)
    ql.train(episodes=1000)
    return ql.solve()


if __name__ == "__main__":
    # Đầu vào Sokoban dạng danh sách các chuỗi
    input_map = [
        "######",
        "# @  #",
        "#  $ #",
        "#  . #",
        "######"
    ]

    # Chuyển đổi đầu vào thành mảng NumPy
    input_array = np.array([list(row) for row in input_map])

    # Tạo Node ban đầu
    initial_state = Node(input_array)

    # Thực hiện giải bài toán
    final_node = q_learning(initial_state)
    print("Kết thúc tại:")
    print(final_node.state)