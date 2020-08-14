from collections import deque
import numpy as np
import queue as Q
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
def cal_pos_nothing(_map,pacman_pos : tuple, visited_center):
    adj_node = (0,0)
    direction = [(1,0),(0,1),(-1,0),(0,-1)]
    cen_pos = cal_center(_map)
    traversal , cost = astar_function(_map, pacman_pos , cen_pos, len(_map[1]), len(_map[0]))
    if(visited_center==True):
        adj_node =  traversal[1]
    else:
        for i in direction:
            adj_node = ((pacman_pos[0] + i[0]),(pacman_pos[1] + i[1]))
            if _map[adj_node[0]][adj_node[1]] != 1 : 
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


if __name__ == '__main__':
    start_pos = (3,11)
    # des_pos = (14,14)
    
    _map = [[1, 1, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
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
    cen_pos = cal_center(_map)
    ans,food,monster= get_vision(_map,start_pos,15,15)
    queue_food = Q.PriorityQueue()
    queue_food.put((6,(0,8)))
    next_move = (0,0)
    if(len(food)==0):
        next_move = cal_pos_nothing(_map,start_pos,visited_center)
    else:
        next_move = cal_pos(_map,start_pos,queue_food,food)
        
    print(next_move)
    start_pos = next_move
    update_dis_to_food(queue_food,start_pos)    
    print(queue_food.queue[0])
    
   
    
    
    
    
    
    
    
    
    
    
    
                