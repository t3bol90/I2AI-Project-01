# from A_star import *
import algorithms
from algorithms import a_star
from graphic import *
from read_data import utils
from random_map import *
import sys, getopt
import MyPacmanGraphics
from graphicsUtils import *
import time

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
# print(a_star.astar_function(_map,start_pos,des_pos,15,15))


    



def main(argv):
    input_file = ''
    output_file = ''
    flag = [0, 0]
    level = 1
    try:
        opts, args = getopt.getopt(argv, "hi:o:l:", ["ifile=", "ofile=", "level="])
    except getopt.GetoptError:
        print('pacman.py -i <input_file> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('pacman.py -i <input_file> -o <output_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
            flag[0] = 1
        elif opt in ("-o", "--ofile"):
            output_file = arg
            flag[1] = 1
        elif opt in ("-l", "--level"):
            level = arg

    import os
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    path = "../random_map/Maze-15_3.txt"
    if flag[0]:
        input_file = os.path.join(THIS_FOLDER, input_file)
        path = input_file
    if flag[1]:
        out_file = os.path.join(THIS_FOLDER, output_file)

    if level == 1:
        n,m,main_matrix,pacman_coordinate = utils.read_txt(path)   
        sup_matrix = utils.create_sup_matrix(main_matrix)
        sup_matrix_wall = utils.create_sup_matrix_wall(sup_matrix)
        sup_matrix_food = utils.create_sup_matrix_food(sup_matrix)
        list_ghost = utils.find_ghost(main_matrix)
        print("Main matrix:", main_matrix)
        print("Sup matrix:",sup_matrix)
        print("Wall matrix:",sup_matrix_wall)
        print("Food matrix:",sup_matrix_food)
        print("Ghost matrix:",list_ghost)
        graphic = MyPacmanGraphics.PacmanGraphics()
        graphic.initialize(n,m)

        graphic.drawWalls(sup_matrix_wall)
        pac = graphic.drawPacman(pacman_coordinate,0)
        graphic.drawWalls(sup_matrix_wall)
        foods_position = utils.find_food(sup_matrix_food)
        if len(foods_position) != 1:
            assert "n food cells of level 1 need to be 1!"
        travelsal, cost = a_star.astar_function(sup_matrix,pacman_coordinate,foods_position[0],n,m)
        
        if cost < 20:
            cur = pacman_coordinate
            foods_position = graphic.drawGhost(foods_position[0],0) # Dung tam - thieu ham draw food
            for cell in travelsal:
                graphic.animatePacman(cur,cell,pac)
                cur = cell
        time.sleep(5)


if __name__ == "__main__":
    main(sys.argv[1:])