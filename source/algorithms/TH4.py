from collections import deque
import numpy as np
import queue as Q
import random
from a_star import *
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
    def is_valid(_x,_y):
        return x in range(n_col) and y in range(n_row)
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
            if is_valid(x,y) and not visited[x][y]:
                dist[x][y] = dist[top[0]][top[1]] + 1
                if (dist[x][y] > 3):
                    continue
                q.append((x,y))
                visited[x][y] = True
    return ans,foods,monster






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

def getValidMove(agent):
    direction = [(1,0),(0,1),(-1,0),(0,-1)]
    validPos = []
    for d in direction:
        move = (agent[0] + d[0],agent[1] + d[1])
        if _map[move[0]][move[1]] != 1:
            validPos.append(move)
    return validPos
    

def minimax(_map,depth,food,agents,agents_index = 0,State_Value = 0,isPacmanTurn = True):
    if depth == 0:
        return State_Value,()

    # pac_man turn
    if isPacmanTurn:
        pacman_moves = getValidMove(agents[0]) # all move possible of pacman_move
        scores = []
        next_state = agents.copy()
        for move in pacman_moves:
            next_state[0] = move # update state
            scores.append(minimax(_map,depth - 1,food,next_state,1,State_Value + evaluationFunction(_map,next_state[0],next_state[1:],food),False)[0]) # best scores of each move 
        #  get best of best-list scores 
        bestScore = max(scores)
        bestScore_Index = [score_index for score_index in range(len(scores)) if scores[score_index] == bestScore]
        next_move = pacman_moves[bestScore_Index[random.randint(0,len(bestScore_Index) - 1)]]
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

def cal_monster_with_minimax(_map,pacman_pos,queue_food,monster):
    agents = monster
    agents.insert(0,pacman_pos) # all agents, pac_man in index = 0 for default
    depth = 6
    score,next_move = minimax(_map,depth,queue_food,agents,agents_index=0,State_Value=0,isPacmanTurn=True)
    return next_move,score

#- --------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    start_pos = (3,11)
    # des_pos = (14,14)
           # 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14  
    _map = [[1, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 0],
            [0, 2, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 2, 0, 0, 0, 0],
            [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]]

    visited_center=True
    ans,food,monster= get_vision(_map,start_pos,15,15)
    queue_food = []
    queue_food.append((4,11))
    monster = [(3,9),(2,11)]
    print(cal_monster_with_minimax(_map,start_pos,queue_food.copy(),monster))
    # if(len(food)==0):
    #     next_move = cal_pos_nothing(_map,start_pos,visited_center)
    # else:
    #     next_move = cal_pos(_map,start_pos,queue_food,food)
        
    # print(next_move)
    
    
    
    
    
    
    
    
    
    
    
                