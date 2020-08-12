import numpy as np
import random 
def random_wall(_map,n_rol,n_col,max_length_wall,num_wall):
    wall_direction = [(0,1),(-1,0),(1,0),(0,-1)]
    for i in range(num_wall):
        wall_index = np.random.randint(0,n_rol * n_col,2)
        for j in range(max_length_wall):
            wall_index += random.sample(wall_direction,1)[0]
            wall_index[0] %= n_rol
            wall_index[1] %= n_col 

            # check neibor
            neibor = np.array([wall_index + x for x in wall_direction])
            count_neibor = 0

            for n in range(4):
                count_neibor += _map[(neibor[n][0] % n_rol,neibor[n][1] % n_rol)]

            if count_neibor <= 1:
                _map[wall_index[0] % n_rol ,wall_index[1] % n_col] = 1
    return _map

def generate_map(n_rol,n_col,n_food,n_monster,max_length_wall,num_wall):
    _map  = np.zeros((n_col,n_rol))
    _map = random_wall(_map,n_rol,n_col,max_length_wall,num_wall)
    # generate food
    for i in range(n_food):
        food_index = np.random.randint(0,n_rol * n_col,2)
        _map[food_index[0] % n_rol,food_index[1] % n_col] = 2
        print(food_index[0] % n_rol,food_index[1] % n_col)

    # generate monster
    for i in range(n_monster):
        monster_index = np.random.randint(0,n_rol * n_col,2)
        _map[monster_index[0] % n_rol,monster_index[1] % n_col] = 3
        print(monster_index[0] % n_rol,monster_index[1] % n_col)
    pacman = [random.randint(0,n_rol),random.randint(0,n_col)]
    _map[pacman[0],pacman[1]] = 0
    return _map,pacman


# n_rol = 15
# n_col = 15
# n_food = 4
# n_monster = 0
n_rol,n_col,n_food,n_monster,max_length_wall,num_wall = list(map(int,input().split()))
_map,pacman = generate_map(n_col,n_rol,n_food,n_monster,max_length_wall,num_wall)
h = f'{n_rol} {n_col}'
f = f'{pacman[0]} {pacman[1]}'
np.savetxt('map.txt',_map,header = h,footer = f,fmt='%.0f',comments= '')

