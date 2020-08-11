import MyPacmanGraphics
import time
from graphicsUtils import *
def main():
	graphic = MyPacmanGraphics.PacmanGraphics()
	graphic.initialize(5,5)
	pac = graphic.drawPacman((0,0),0)
	pac2 = graphic.drawPacman((0,0),0)
	pac3 = graphic.drawPacman((0,0),0)
	remove_from_screen(pac2)
	remove_from_screen(pac3)
	#pac4 = graphic.drawPacman((0,0),0)
	walls = [[0,0,0,0,0],[0,0,0,1,0],[0,1,1,1,0],[0,0,0,0,0],[0,0,0,0,0]]
	graphic.drawWalls(walls)
	graphic.animatePacman((0,0),(4,0),pac)
	graphic.animatePacman((4,0),(4,4),pac)
	graphic.animatePacman((4,4),(0,4),pac)
	graphic.animatePacman((0,4),(0,0),pac)
	ghosts = graphic.drawGhost((0,0),0)
	graphic.animateGhost((0,0),(4,0),0,ghosts)
	graphic.animateGhost((4,0),(4,4),0,ghosts)
	graphic.animateGhost((4,4),(0,4),0,ghosts)
	graphic.animateGhost((0,4),(0,0),0,ghosts)
	time.sleep(5)
main()