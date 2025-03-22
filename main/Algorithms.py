from collections import deque
import numpy as np

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