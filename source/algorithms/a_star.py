from queue import heappop,heappush
import types

def h_n(start_pos:tuple,des_pos:tuple):
    return abs(start_pos[0] - des_pos[0]) + abs(start_pos[1] - des_pos[1])
def astar_function(_map:list,start_pos:tuple,des_pos:tuple,n_rol:int,n_col:int):
    min_heap = []
    heappush(min_heap,(h_n(start_pos,des_pos),start_pos))
    visited_node = {}
    direction = [(1,0),(0,1),(-1,0),(0,-1)]
    while min_heap:
        cur_f_x,cur_pos = heappop(min_heap)
        cur_h_n = h_n(cur_pos,des_pos)
        if cur_pos == des_pos:
            path = []
            path.append(cur_pos)
            while path[-1] != start_pos:
                path.append(visited_node[path[-1]])
            path.reverse()
            return path, len(path)
        adj_node = ()
        for i in direction: 
            adj_node = ((cur_pos[0] + i[0]),(cur_pos[1] + i[1]))
            if adj_node[0] == n_rol or adj_node[1] == n_col or adj_node[0] * adj_node[1] < 0:
                continue
            if adj_node not in visited_node and _map[adj_node[0]][adj_node[1]] != 1:
                adj_f_x = (cur_f_x - cur_h_n) + 1 + h_n(adj_node,des_pos)
                heappush(min_heap,(adj_f_x,adj_node))
                visited_node[adj_node] = cur_pos
    return [],0
        

        
# start_pos = (1,1)
# des_pos = (14,14)
# _map = [[1,1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
# [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
# [0, 2, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0],
# [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 2, 0, 0, 0, 0],
# [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]]
# print(_map)
# print(astar_function(_map,start_pos,des_pos,15,15))
