# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 21:05:21 2020

@author: admin
"""
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

def create_sup_matrix(main_matrix):
    sup_matrix = main_matrix.T
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
            


if __name__ == "__main__":

    path = "D:\\cc.txt"
    n,m,main_matrix,pacman_coordinate = read_txt(path)   
    sup_matrix = create_sup_matrix(main_matrix)
    sup_matrix_wall = create_sup_matrix_wall(sup_matrix)
    sup_matrix_food = create_sup_matrix_food(sup_matrix)
    list_ghost = find_ghost(main_matrix)
    print(sup_matrix)
    print(sup_matrix_wall)
    print(sup_matrix_food)
    print(list_ghost)














