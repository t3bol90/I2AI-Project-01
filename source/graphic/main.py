from gameController import *
import numpy as np

def read_txt(path):
    f = open(path)

    line1 = f.readline().rstrip("\n")
    list1 = line1.split(" ")
    n,m=int(list1[0]),int(list1[1])
    main_matrix = np.zeros((n,m))
    
    for i in range(n):
        line = f.readline().rstrip("\n")
        list = line.split(" ")
        for j in range(m):
            main_matrix[i,j]=int(list[j])
            
    list2 = (f.readline().rstrip("\n")).split(" ")
    
    pacman_coordinate = ((int(list2[0]), int(list2[1])))
    return n,m,main_matrix,pacman_coordinate
def main():
	n,m,main_matrix,pacman_coordinate = read_txt("../random_map/map3.txt")
	game = GameController(main_matrix,pacman_coordinate)
	game.StartGame(2)
main()