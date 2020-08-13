from pacmanGraphics import *
from random import *
from graphicsUtils import *
import numpy as np
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

class GameController:
	def __init__(self,maze,posPacman):
		self.pacman = None
		self.maze = maze
		self.graphic = PacmanGraphics()
		self.width = len(maze[0])
		self.height = len(maze)
		self.posPacman = self.ConvertIndexGraphic(posPacman)
		self.posGhost = np.array(find_ghost(create_sup_matrix(maze)))
		self.walls = np.array(create_sup_matrix_wall(create_sup_matrix(maze)))
		self.isLose = False
		self.ghost = []
	def StartGame(self,_level = 1):
		self.graphic.Initialize(self.width,self.height)
		self.graphic.DrawWalls(self.walls)
		self.pacman = self.graphic.DrawPacman(self.posPacman,0)
		self.graphic.MovePacman(self.posPacman,"East",self.pacman)
		if(_level > 1):
			__totalGhost = len(self.posGhost)
			for i in range(__totalGhost):
				self.ghost.append(self.graphic.DrawGhost(self.posGhost[i],i%__totalGhost))
				self.graphic.AnimateGhost(self.posGhost[i],self.posGhost[i],i%__totalGhost,self.ghost[i])
		self.foods = np.array(self.graphic.DrawFood(create_sup_matrix_food(create_sup_matrix(self.maze))))
		if(_level == 1 or _level == 2):
			self.Level1_2(_level)
		elif(_level == 3):
			self.Level3()
		elif(_level == 4):
			pass
		sleep(1)
		if(self.isLose):
			text(self.graphic.to_screen((0, self.height/2)), formatColor(255.0/255.0,0,0),"LOSE GAME", "Times", int(0.08*self.width*self.graphic.gridSize), "bold")
		else:
			_canvas_xs = (2+self.graphic.width)*self.graphic.gridSize
			_canvas_ys = (2+self.graphic.height)*self.graphic.gridSize + INFO_PANE_HEIGHT
			_color = formatColor(96.0/255.0,172.0/255.0,172.0/255.0)
			polygon([(0,0), (0, _canvas_ys), (_canvas_xs, _canvas_ys), (_canvas_xs, 0)],_color , fillColor = _color , filled=True, smoothed=False)
			text(self.graphic.to_screen((0, self.height/2)), formatColor(148.0/255.0,0,211.0/255.0),"OPTIMAL SCORE: " + str(self.graphic.score), "Times", int(0.065*self.width*self.graphic.gridSize), "bold")
		print("MAX SCORE: ",self.graphic.score)
		sleep(2)
		self.graphic.EndGraphics()
	def Level1_2(self,_level):
		# Call search strategy for list path
		# Call A* here
		__foodsPosition = np.argwhere(self.foods != None)
		if(len(__foodsPosition) != 0):
			travelsal,cost = astar_function(self.maze,self.ConvertIndexMaze(self.posPacman),self.ConvertIndexMaze(__foodsPosition[0]),self.height,self.width)
			if(cost < 20):
				for i in travelsal:
					self.AgentMove(i,0,True)
	def Level3(self):
		# Turn base
		while(True):
			__actionPos = self.PacmanTurn()
			self.AgentMove(__actionPos,0,True)
			if(self.IsEndGame() == True):
				self.isLose = True
				return
			for i in range(len(self.ghost)):
				__actionPos = self.GhostTurn(i,_level)
				self.AgentMove(__actionPos,i,False)
				if(self.IsEndGame() == True):
					self.isLose = True
					return
	def GhostTurn(self,index,_level):
		__actionPos = (0,0)
		if(_level == 3):
			pass
		else:
			travelsal,cost = astar_function(self.maze,self.ConvertIndexMaze(self.posGhost[index]),self.ConvertIndexMaze(self.posPacman),self.height,self.width)
			__actionPos = (travelsal[0][0],travelsal[0][1]) if lend(travelsal) != 0 else self.posGhost[index]
		return __actionPos
	def IsEndGame(self):
		for i in self.posGhost:
			if(i[0] == self.posPacman[0] and i[1] == self.posPacman[1]):
				self.isLose = True
				return True
		return False
	def PacmanTurn(self):
		__actionPos = (0,0)
		temp = [(-1,0),(1,0),(0,1),(0,-1)]
		temp2 = temp[randint(0,3)]
		__actionPos = (self.posPacman[0]+temp2[0],self.posPacman[1]+temp2[1])
		return __actionPos
	def AgentMove(self,pos,index,isPacman = True):
		pos = self.ConvertIndexGraphic(pos)
		if(isPacman):
			self.graphic.AnimatePacman(self.posPacman,pos,self.pacman)
			self.posPacman = pos
			scoreBonus = 0
			if(self.foods[pos] is not None):
				self.graphic.RemoveFood(pos,self.foods)
				scoreBonus = 20
				self.foods[pos] = None
			self.graphic.UpdateScore(scoreBonus)
		else:
			self.graphic.AnimateGhost(self.posGhost[index],pos,index,self.ghost[index])
			self.posGhost[index] = pos
	def ConvertIndexGraphic(self,index):
		return (index[1],self.height - 1 - index[0])

	def ConvertIndexMaze(self,index):
		return ((self.height - 1) - index[1],index[0])