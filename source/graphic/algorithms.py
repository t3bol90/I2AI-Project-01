import numpy as np
from queue import heappop,heappush
import queue as Q
import types
from random import *
from collections import deque
import operator

FOODS = 2
MONSTER = 3
WALL = 1
NOTWALL = 0

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
            if adj_node[0] not in range (n_rol) or adj_node[1] not in range (n_col):
                continue
            if adj_node not in visited_node and _map[adj_node[0]][adj_node[1]] in [FOODS, NOTWALL]:
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
    VISITED_LIMIT = 1
    visited_map[pacman_pos[0]][pacman_pos[1]] += 1 
    direction = [(1,0),(0,1),(-1,0),(0,-1)]
    cen_pos = cal_center(_map)
    possible_move = []
    for dx, dy in direction:
        x = pacman_pos[0] + dx
        y = pacman_pos[1] + dy
        if x in range(len(_map[0])) and y in range(len(_map)) and _map[x][y] not in [1,3] and visited_map[x][y] < VISITED_LIMIT:
            possible_move.append((h_n((x,y),cen_pos),(x,y)))
    possible_move.sort()
    if possible_move:
        adj_node = possible_move[0][1]
    else: adj_node = None
    # for i in visited_map:
    #     print(i)
    return adj_node
#Xét có food thì gọi hàm này   
def cal_pos(_map, pacman_pos : tuple, queue_food : Q.PriorityQueue, food : list):
    for i in food:
        traversal, cost = astar_function(_map,pacman_pos,i,len(_map[0]), len(_map))
        if i in [tup[1] for tup in queue_food.queue]:
            continue
        if(len(traversal) > 1):
            queue_food.put((cost,i))
    closest_food = queue_food.queue[0]
    print("Is going to", closest_food)
    traversal, cost = astar_function(_map,pacman_pos,closest_food[1],len(_map[0]), len(_map))
    print("Path: ", traversal)
    if(len(traversal) > 1):
        return traversal[1]
    
    return None

# Level 4
#----------------------------------------------------------------------------------------------------------------------
def monster_pos_minimizing(_map:list,pacman_pos:tuple,monster:tuple):
    path,path_len = astar_function(_map,monster,pacman_pos,len(_map),len(_map[0]))
    if path_len < 2:
        return monster
    monster_move = path[1]
    return monster_move

def evaluationFunction(_map,pacman_pos,monster,food:list):
    if pacman_pos in monster:
        return -1000000
    if pacman_pos in food:
        food.remove(pacman_pos)
        return 20
    else:
        return -1

def getValidMove(agent,_map):
    direction = [(1,0),(0,1),(-1,0),(0,-1)]
    validPos = []
    for d in direction:
        move = (agent[0] + d[0],agent[1] + d[1])
        if (is_valid(move[0],move[1],len(_map[0]),len(_map)) and _map[move[0]][move[1]] != 1):
            validPos.append(move)
    return validPos
    

def minimax(_map,depth,food,agents,agents_index = 0,State_Value = 0,isPacmanTurn = True):
    if depth == 0:
        return State_Value,()
    # pac_man turn
    if isPacmanTurn:
        pacman_moves = getValidMove(agents[0],_map) # all move possible of pacman_move
        scores = []
        next_state = agents.copy()
        for move in pacman_moves:
            next_state[0] = move # update state
            scores.append(minimax(_map,depth - 1,food,next_state,1,State_Value + evaluationFunction(_map,next_state[0],next_state[1:],food),False)[0]) # best scores of each move 
        #  get best of best-list scores 
        bestScore = max(scores)
        bestScore_Index = [score_index for score_index in range(len(scores)) if scores[score_index] == bestScore]
        # next_move = pacman_moves[bestScore_Index[randint(0,len(bestScore_Index) - 1)]]
        next_move = [pacman_moves[bestScore_Index[i]] for i in range(len(bestScore_Index))]
        return bestScore,next_move
    #monster turn 
    else:
        monster_move = monster_pos_minimizing(_map,agents[0],agents[agents_index]) # monster move, use a star to get minimum-score move

        if monster_move == agents[0]: # meet mr.pacman
            State_Value += -1000000

        next_state = agents.copy()
        if agents_index == len(agents) - 1: # if out out monster -> depth - 1
            next_state[agents_index] = monster_move  # update state
            min_score = minimax(_map,depth - 1,food,next_state,0,State_Value,True)[0]
        else:
            next_state[agents_index] = monster_move # update state
            min_score = minimax(_map,depth,food,next_state,agents_index + 1,State_Value,False)[0]


        return min_score, monster_move

def cal_monster_with_minimax(_map,pacman_pos,queue_food,monster,frequency):
    agents = monster
    agents.insert(0,pacman_pos) # all agents, pac_man in index = 0 for default
    depth = 4
    score,next_move = minimax(_map,depth,queue_food,agents,agents_index=0,State_Value=0,isPacmanTurn=True)
    pq = []
    for i in range(len(next_move)):
        pq.append((frequency[next_move[i][0]][next_move[i][1]],next_move[i]))
    pq.sort()
    return pq[0][1],score

#- --------------------------------------------------------------------------------------------------------------------------

#def my_cal_pos_nothing(maze,pacman_pos : tuple,effortToCenter):
#    dir = np.array([(1,0),(0,1),(-1,0),(0,-1)])
#    dir += pacman_pos
#    __validMove = []
#    for i in range(4):
#        if(is_valid(dir[i][0],dir[i][1],len(maze[0]),len(maze)) and maze[dir[i][0],dir[i][1]] != 1):
#            __validMove.append(i)
#    if not __validMove:
#        return None
#    dir = dir[__validMove]
#    center = tuple(map(operator.add,cal_center(maze),(randint(-1,1),randint(-1,1))))
#    traversal , cost = astar_function(maze, pacman_pos , center, len(maze), len(maze[0]))
#    __bound = 5
#    if(effortToCenter < __bound and len(traversal) > 1):
#        __next_move =  traversal[1]
#    else:
#        effortToCenter += 1
#        __next_move = dir[randint(0,len(dir)-1)]
#    return tuple(__next_move),effortToCenter

