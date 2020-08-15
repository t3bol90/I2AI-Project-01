import numpy as np
from queue import heappop,heappush
import queue as Q
import types
from collections import deque

def is_valid(_x,_y,n_col,n_row):
    return _x in range(n_col) and _y in range(n_row)
def get_vision(_map:list,start_pos:tuple,n_row:int,n_col:int):
    q = deque()
    visited = [[False]* n_col for _ in range(n_row)]
    dist = [[0]* n_col for _ in range(n_row)]
    q.append(start_pos)
    visited[start_pos[0]][start_pos[1]] = True
    ans = []
    foods = []
    monster = []
    distx = [0,0,1,-1]
    disty = [1,-1,0,0]
    while q:
        top = q.popleft()
        ans.append(top)
        if _map[top[0]][top[1]] == 2:
            foods.append(top)
        elif _map[top[0]][top[1]] == 3:
            monster.append(top)
        for dx,dy in zip(distx,disty):
            x = top[0] + dx
            y = top[1] + dy 
            if is_valid(x,y,n_col,n_row) and not visited[x][y]:
                dist[x][y] = dist[top[0]][top[1]] + 1
                if (dist[x][y] > 3):
                    continue
                q.append((x,y))
                visited[x][y] = True
    return ans,foods,monster

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


def create_sup_matrix(main_matrix):
    sup_matrix = main_matrix.copy().T
    for i in range(sup_matrix.shape[0]):
        sup_matrix[:][i] = sup_matrix[:][i][::-1]  
    return sup_matrix

def create_sup_matrix_wall(sup_matrix):
    return np.array([[0 if sup_matrix[i,j] != 1 else 1 for i in range(sup_matrix.shape[0])] for j in range(sup_matrix.shape[1])]).T

def create_sup_matrix_food(sup_matrix):
    return np.array([[0 if sup_matrix[i,j] != 2 else 2 for i in range(sup_matrix.shape[0])] for j in range(sup_matrix.shape[1])]).T

def find_ghost(matrix):
    list_ghost = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if(matrix[i,j] == 3):
                list_ghost.append((i,j))
    return list_ghost    


#Cập nhật lại khoảng cách tới food đã tìm thấy sau khi đi 1 bước mới
def update_dis_to_food(queue_food : Q.PriorityQueue, pacman_pos):
    food_pos = []
    while not queue_food.empty():
        cur_food = queue_food.get()[1]
        food_pos.append(cur_food)
    for i in food_pos:
        cost = h_n(pacman_pos,i)
        queue_food.put((cost,i))

#tính trung tâm của map
def cal_center(_map: list):
    return (len(_map[0])//2,len(_map[1])//2)

#Xét food ko có trong vision thì gọi hàm này
def cal_pos_nothing(_map,pacman_pos : tuple, visited_center, visited_map):
    visited_map[pacman_pos[0]][pacman_pos[1]] = True
    adj_node = (0,0)
    direction = [(1,0),(0,1),(-1,0),(0,-1)]
    cen_pos = cal_center(_map)
    traversal , cost = astar_function(_map, pacman_pos , cen_pos, len(_map[1]), len(_map[0]))
    if(visited_center==True and len(traversal)>1):
        adj_node =  traversal[1]
    else:
        for i in direction:
            adj_node = ((pacman_pos[0] + i[0]),(pacman_pos[1] + i[1]))
            if(is_valid(adj_node[0],adj_node[1],len(_map[0]),len(_map)) and _map[adj_node[0]][adj_node[1]] != 1 and visited_map[adj_node[0]][adj_node[1]] == False):
                visited_map[adj_node[0]][adj_node[1]] = True
                break
    return adj_node


#Xét có food thì gọi hàm này   
def cal_pos(_map, pacman_pos : tuple, queue_food : Q.PriorityQueue, food : list):
    for i in food:
        cost = h_n(pacman_pos,i)
        queue_food.put((cost,i))
    
    closest_food = queue_food.queue[0]  
    traversal, cost = astar_function(_map,pacman_pos,closest_food[1],len(_map[1]), len(_map[0]))
    return traversal[1]  

# monster đi random -> các vị trí có thể của monster
def monster_move(monste_pos):
    direction = [(1,0),(0,1),(-1,0),(0,-1)]
    invalid_pos = [((m[0] + d[0]),(m[1] + d[1])) for m in monste_pos for d in direction]
    return invalid_pos

# nếu có monster trong vision
def cal_monster(_map,pacman_pos,queue_food,monster,visited_center):
    direction = [(1,0),(0,1),(-1,0),(0,-1)]
    valid_pos = []
    notsafe_pos = monster_move(monster)
    for d in direction:
        move = ((pacman_pos[0] + d[0]),(pacman_pos[1] + d[1]))
        if move in notsafe_pos:
            continue
        valid_pos.append(move)
    if len(valid_pos) == 0:
        d = direction[random.randint(0,3)]
        return ((pacman_pos[0] + d[0]),(pacman_pos[1] + d[1]))
        
    if not queue_food.empty():
        next_pos = cal_pos(_map,pacman_pos,queue_food,food)
        if next_pos not in valid_pos:
            cos_valid_pos = [h_n(adj_pos,queue_food.queue[0][1]) for adj_pos in valid_pos]
            for i in range(len(cos_valid_pos)):
                if cos_valid_pos[i] == min(cos_valid_pos):
                    next_pos = valid_pos[i]
                    break
    else:
        next_pos = cal_pos_nothing(_map,pacman_pos,visited_center)
        if next_pos not in valid_pos:
            center = cal_center(_map)
            cos_valid_pos = [h_n(adj_pos,center) for adj_pos in valid_pos]
            for i in range(len(cos_valid_pos)):
                if cos_valid_pos[i] == min(cos_valid_pos):
                    next_pos = valid_pos[i]
                    break 
    return next_pos


