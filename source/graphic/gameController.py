from pacmanGraphics import *
from graphicsUtils import *
from algorithms import *

class GameController:
	def __init__(self,maze,posPacman):
		self.pacman = None
		self.maze = np.array(maze,dtype = np.uint8)
		self.graphic = PacmanGraphics()
		self.width = len(maze[0])
		self.height = len(maze)
		self.posPacman = self.ConvertIndexGraphic(posPacman)
		self.posGhost = np.array(find_ghost(create_sup_matrix(maze)))
		self.walls = np.array(create_sup_matrix_wall(create_sup_matrix(maze)))
		self.isLose = False
		self.ghost = []
		self.movementList = [ [] for i in range(len(self.posGhost))]
		self.effort = 0
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
		# Call search stragety for list path
		# Call A* here
		__foodsPosition = np.argwhere(self.foods != None)
		if(len(__foodsPosition) != 0):
			travelsal,cost = astar_function(self.maze,self.ConvertIndexMaze(self.posPacman),self.ConvertIndexMaze(__foodsPosition[0]),self.height,self.width)
			if(cost < 20):
				for i in travelsal:
					self.AgentMove(i,0,True)
	def Level3(self):
		# Turn base
		visited_map = [[False]* self.height for _ in range(self.width)]
		queue_food = Q.PriorityQueue()
		while(True):
			# Pacman turn
			__next_move,__vision = self.PacmanTurn(queue_food,visited_map)
			if(__next_move is None):
				return
			self.AgentMove(__next_move,0,True)
			# Draw Aura
			__auraImg = self.graphic.DrawAura([self.ConvertIndexGraphic(i) for i in __vision])
			# Check is end game?
			if(self.IsEndGame() == True):
				return
			# Monster turn
			for i in range(len(self.ghost)):
				__next_move = self.GhostTurn(i,3)
				if (__next_move is not None):
					self.AgentMove(__next_move,i,False)
				if(self.IsEndGame() == True):
					return
			# Remove aura
			self.graphic.RemoveAura(__auraImg)
	def GhostTurn(self,index,_level):
		__next_move = None
		if(_level == 3):
			__next_move = self.ConvertIndexMaze(self.posGhost[index])
			if(len(self.movementList[index]) == 0):
				crossMovement = [[(-1,0),(-1,0),(1,0),(1,0),(1,0),(1,0),(-1,0),(-1,0)],[(0,1),(0,1),(0,-1),(0,-1),(0,-1),(0,-1),(0,1),(0,1)]]
				squareMovement = [[(-1,0),(0,1),(1,0),(0,-1)],[(-1,0),(0,-1),(1,0),(0,1)]]
				if(randint(0,1) == 0):
					# Cross movement
					if(randint(0,1) == 1):
						self.movementList[index] = crossMovement[randint(0,1)]
					else:
						self.movementList[index] = [ (i[0]*-1,i[1]*-1) for i in crossMovement[randint(0,1)]]
				else:
					# Square movement
					if(randint(0,1) == 1):
						self.movementList[index] = squareMovement[randint(0,1)]
					else:
						self.movementList[index] = [ (i[0]*-1,i[1]*-1) for i in squareMovement[randint(0,1)]]
			while(True):
				__next_move = tuple(map(operator.add, __next_move , self.movementList[index].pop(0)))
				if(__next_move[0] < self.height and __next_move[1] < self.width and self.maze[__next_move] != 1):
					break
		else:
			travelsal,cost = astar_function(self.maze,self.ConvertIndexMaze(self.posGhost[index]),self.ConvertIndexMaze(self.posPacman),self.height,self.width)
			__next_move = travelsal.pop(1) if len(travelsal)> 1 else None
		return __next_move
	def IsEndGame(self):
		for i in self.posGhost:
			if(i[0] == self.posPacman[0] and i[1] == self.posPacman[1]):
				self.isLose = True
				return True
		return False
	def PacmanTurn(self,queue_food,visited_map):
		__vision,foods,ghost = get_vision(self.maze,self.ConvertIndexMaze(self.posPacman),self.height,self.width)
		__next_move = self.ConvertIndexMaze(self.posPacman)
		if(len(ghost) > 0):
			# Case 4, minimax
			__next_move,estimatedScore = cal_monster_with_minimax(self.maze,self.ConvertIndexMaze(self.posPacman),foods,ghost)
			print(estimatedScore)
			if(estimatedScore < -1000):
				__next_move = None
		elif(len(foods) >= 1 or not queue_food.empty()):
			# Case 2,3, has foods
			__next_move = cal_pos(self.maze,self.ConvertIndexMaze(self.posPacman),queue_food,foods)
			print(__next_move)
			if(__next_move is not None and __next_move == queue_food.queue[0]):
				top = queue_food.get()
				while (top == queue_food.queue[0]):
					queue_food.get()
				print(top)
			elif(__next_move is None):
				__next_move = cal_pos_nothing(self.maze,self.ConvertIndexMaze(self.posPacman),False,visited_map)
		else:
			# Case 1
			__next_move = cal_pos_nothing(self.maze,self.ConvertIndexMaze(self.posPacman),False,visited_map)
		if(__next_move is None):
			return None,None

		__vision,foods,ghost = get_vision(self.maze,__next_move,self.height,self.width)
		update_dis_to_food(queue_food,__next_move)
		return __next_move,__vision
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
				self.maze[self.ConvertIndexMaze(pos)] = 0
			self.graphic.UpdateScore(scoreBonus)
		else:
			self.graphic.AnimateGhost(self.posGhost[index],pos,index,self.ghost[index])
			self.maze[self.ConvertIndexMaze(pos)] = 3
			self.maze[self.ConvertIndexMaze(self.posGhost[index])] = 0
			self.posGhost[index] = pos
	def ConvertIndexGraphic(self,index):
		return (index[1],self.height - 1 - index[0])

	def ConvertIndexMaze(self,index):
		return ((self.height - 1) - index[1],index[0])

	