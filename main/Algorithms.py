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

def DFS(start_node):
    stack = [start_node]
    visited = set()

    while stack:
        current = stack.pop()

        if current.check_win():
            return current  # Trả về node để truy vết

        for next in current.get_valid_state():
            state_tuple = tuple(map(tuple, next.state))
            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            next.parent = current
            stack.append(next)  # DFS dùng stack thay vì queue

    return None
