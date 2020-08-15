from graphicsUtils import *
import math, time

###########################
#  GRAPHICS DISPLAY CODE  #
###########################


DEFAULT_GRID_SIZE = 30.0
INFO_PANE_HEIGHT = 35   
BACKGROUND_COLOR = formatColor(0,0,0)
WALL_COLOR = formatColor(0.0/255.0, 51.0/255.0, 255.0/255.0)
PACMAN_OUTLINE_WIDTH = 2
PACMAN_CAPTURE_OUTLINE_WIDTH = 4

GHOST_COLORS = []
GHOST_COLORS.append(formatColor(.9,0,0)) # Red
GHOST_COLORS.append(formatColor(0,.3,.9)) # Blue
GHOST_COLORS.append(formatColor(.98,.41,.07)) # Orange
GHOST_COLORS.append(formatColor(.1,.75,.7)) # Green
GHOST_COLORS.append(formatColor(1.0,0.6,0.0)) # Yellow
GHOST_COLORS.append(formatColor(.4,0.13,0.91)) # Purple

TEAM_COLORS = GHOST_COLORS[:2]

GHOST_SHAPE = [
    ( 0,    0.3 ),
    ( 0.25, 0.75 ),
    ( 0.5,  0.3 ),
    ( 0.75, 0.75 ),
    ( 0.75, -0.5 ),
    ( 0.5,  -0.75 ),
    (-0.5,  -0.75 ),
    (-0.75, -0.5 ),
    (-0.75, 0.75 ),
    (-0.5,  0.3 ),
    (-0.25, 0.75 )
  ]
GHOST_SIZE = 0.5

GHOST_VEC_COLORS = map(colorToVector, GHOST_COLORS)

PACMAN_COLOR = formatColor(255.0/255.0,255.0/255.0,61.0/255)
PACMAN_SCALE = 0.4
#pacman_speed = 0.25

# Food
FOOD_COLOR = formatColor(1,1,1)
FOOD_SIZE = 0.1

# Laser
LASER_COLOR = formatColor(1,0,0)


# Drawing walls
WALL_RADIUS = 0.15

class InfoPane:
  def __init__(self, width , height , gridSize):
    self.gridSize = gridSize
    self.width = width * gridSize
    self.base = (height + 1) * gridSize
    self.height = INFO_PANE_HEIGHT
    self.fontSize = 24
    self.textColor = LASER_COLOR
    self.drawPane()

  def toScreen(self, pos, y = None):
    """
      Translates a point relative from the bottom left of the info pane.
    """
    if y == None:
      x,y = pos
    else:
      x = pos

    x = self.gridSize + x
    y = self.base + y
    return x,y

  def drawPane(self):
    self.scoreText = text( self.toScreen(0, 0), self.textColor, "SCORE:    0", "Times", self.fontSize, "bold")

  def updateScore(self, score):
    changeText(self.scoreText, "SCORE: % 4d" % score)

class PacmanGraphics:
  def __init__(self, zoom=1.0, frameTime=0.0, capture=False):
    self.have_window = 0
    self.currentGhostImages = {}
    self.pacmanImage = None
    self.zoom = zoom
    self.gridSize = DEFAULT_GRID_SIZE * zoom
    self.capture = capture
    self.frameTime = frameTime

  def Initialize(self, width,height, isBlue = False):
    self.isBlue = isBlue
    self.StartGraphics(width,height)

  def StartGraphics(self, width,height):
    self.width = width
    self.height = height
    self.Make_window(self.width, self.height)
    self.infoPane = InfoPane(width,height, self.gridSize)
  def Make_window(self, width, height):
    grid_width = (width) * self.gridSize
    grid_height = (height) * self.gridSize
    screen_width = 2*self.gridSize + grid_width
    screen_height = 2*self.gridSize + grid_height + INFO_PANE_HEIGHT
    begin_graphics(screen_width,screen_height,BACKGROUND_COLOR,"TaLang_AI")
    skin = PACMAN_SCALE * 15/0.4
    line((self.gridSize-skin,self.gridSize-skin),(self.gridSize-skin,skin+grid_height),WALL_COLOR,3)
    line((self.gridSize-skin,skin+grid_height),(grid_width+skin,skin+grid_height),WALL_COLOR,3)
    line((self.gridSize-skin,self.gridSize-skin),(grid_width+skin,self.gridSize-skin),WALL_COLOR,3)
    line((grid_width+skin,self.gridSize-skin),(grid_width+skin,skin+grid_height),WALL_COLOR,3)


  def DrawPacman(self, position, index,direction = "East"):
    screen_point = self.to_screen(position)
    endpoints = self.GetEndpoints(direction,screen_point)
    width = PACMAN_OUTLINE_WIDTH
    outlineColor = PACMAN_COLOR
    fillColor = PACMAN_COLOR
    self.score = 0
    if self.capture:
      outlineColor = TEAM_COLORS[index % 2]
      fillColor = GHOST_COLORS[index]
      width = PACMAN_CAPTURE_OUTLINE_WIDTH
    return [circle(screen_point, PACMAN_SCALE * self.gridSize,fillColor = fillColor, outlineColor = outlineColor,endpoints = endpoints,width = width)]

  def GetEndpoints(self, direction, position=(0,0)):
    x, y = position
    pos = x - int(x) + y - int(y)
    width = 30 + 80 * math.sin(math.pi* pos)

    delta = width / 2
    if (direction == 'West'):
      endpoints = (180+delta, 180-delta)
    elif (direction == 'North'):
      endpoints = (90+delta, 90-delta)
    elif (direction == 'South'):
      endpoints = (270+delta, 270-delta)
    else:
      endpoints = (0+delta, 0-delta)
    return endpoints

  def to_screen(self, point):
    ( x, y ) = point
    x = (x + 1)*self.gridSize
    y = (self.height  - y)*self.gridSize
    return ( x, y )

  def to_screen2(self, point):
    ( x, y ) = point
    x = (x + 1)*self.gridSize
    y = (self.height  - y)*self.gridSize
    return ( x, y )

  def MovePacman(self, position, direction, image):
    screenPosition = self.to_screen(position)
    endpoints = self.GetEndpoints( direction, position )
    r = PACMAN_SCALE * self.gridSize
    moveCircle(image[0], screenPosition, r, endpoints)
    refresh()

  def AnimatePacman(self, posPrevPacman,posPacman, image):
    self.frameTime = 0.1
    if self.frameTime > 0.01 or self.frameTime < 0:
      start = time.time()
      fx, fy = posPrevPacman[0],posPrevPacman[1]
      px, py = posPacman[0],posPacman[1]
      frames = 1.0
      for i in range(1,int(frames) + 1):
        pos = px*i/frames + fx*(frames-i)/frames, py*i/frames + fy*(frames-i)/frames
        self.MovePacman(pos, self.GetDirection(posPrevPacman,posPacman), image)
        refresh()
        sleep(abs(self.frameTime) / frames)
    else:
      self.MovePacman(posPacman, self.GetDirection(posPrevPacman,posPacman), image)
    refresh()
    #self.score -= 1

  def UpdateScore(self,scoreBonus = 0):
      self.score += scoreBonus-1
      self.infoPane.updateScore(self.score)

  def GetDirection(self,posX,posY):
      dir = ["West","East","North","South"]
      w = (posX[0]-1, posX[1])
      min = dist(w,posY)
      i = 0
      e = (posX[0]+1, posX[1])
      if(dist(e,posY) < min):
          i = 1
          min = dist(e,posY)
      n = (posX[0], posX[1]+1)
      if(dist(n,posY) < min):
          i = 2
          min = dist(n,posY)
      s = (posX[0], posX[1]-1)
      if(dist(s,posY) < min):
          i = 3
      return dir[i]
  def DrawGhost(self, position, agentIndex,direction = "East"):
    pos = position
    dir = direction
    (screen_x, screen_y) = (self.to_screen(pos))
    coords = []
    for (x, y) in GHOST_SHAPE:
      coords.append((x*self.gridSize*GHOST_SIZE + screen_x, y*self.gridSize*GHOST_SIZE + screen_y))

    colour = GHOST_COLORS[agentIndex]
    body = polygon(coords, colour, filled = 1)
    WHITE = formatColor(1.0, 1.0, 1.0)
    BLACK = formatColor(0.0, 0.0, 0.0)

    dx = 0
    dy = 0
    if dir == 'North':
      dy = -0.2
    if dir == 'South':
      dy = 0.2
    if dir == 'East':
      dx = 0.2
    if dir == 'West':
      dx = -0.2
    leftEye = circle((screen_x+self.gridSize*GHOST_SIZE*(-0.3+dx/1.5), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy/1.5)), self.gridSize*GHOST_SIZE*0.2, WHITE, WHITE)
    rightEye = circle((screen_x+self.gridSize*GHOST_SIZE*(0.3+dx/1.5), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy/1.5)), self.gridSize*GHOST_SIZE*0.2, WHITE, WHITE)
    leftPupil = circle((screen_x+self.gridSize*GHOST_SIZE*(-0.3+dx), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy)), self.gridSize*GHOST_SIZE*0.08, BLACK, BLACK)
    rightPupil = circle((screen_x+self.gridSize*GHOST_SIZE*(0.3+dx), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy)), self.gridSize*GHOST_SIZE*0.08, BLACK, BLACK)
    ghostImageParts = []
    ghostImageParts.append(body)
    ghostImageParts.append(leftEye)
    ghostImageParts.append(rightEye)
    ghostImageParts.append(leftPupil)
    ghostImageParts.append(rightPupil)

    return ghostImageParts

  def AnimateGhost(self, posPrevGhost, posGhost, ghostIndex, ghostImageParts):
    old_x, old_y = posPrevGhost[0],posPrevGhost[1]
    new_x, new_y = posGhost[0],posGhost[1]
    self.frameTime = 0.1
    start = time.time()
    frames = 1.0
    for i in range(1,int(frames) + 1):
        pos = new_x*i/frames + old_x*(frames-i)/frames, new_y*i/frames + old_y*(frames-i)/frames
        for ghostImagePart in ghostImageParts:
            move_to(ghostImagePart, self.to_screen(pos))
        self.MoveEyes(pos, self.GetDirection(posPrevGhost,posGhost), ghostImageParts[-4:])
        refresh()
        sleep(abs(self.frameTime) / frames)
    color = GHOST_COLORS[ghostIndex]
    edit(ghostImageParts[0], ('fill', color), ('outline', color))
    refresh()

  def MoveEyes(self, pos, dir, eyes):
    (screen_x, screen_y) = (self.to_screen(pos) )
    dx = 0
    dy = 0
    if dir == 'North':
      dy = -0.2
    if dir == 'South':
      dy = 0.2
    if dir == 'East':
      dx = 0.2
    if dir == 'West':
      dx = -0.2
    moveCircle(eyes[0],(screen_x+self.gridSize*GHOST_SIZE*(-0.3+dx/1.5), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy/1.5)), self.gridSize*GHOST_SIZE*0.2)
    moveCircle(eyes[1],(screen_x+self.gridSize*GHOST_SIZE*(0.3+dx/1.5), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy/1.5)), self.gridSize*GHOST_SIZE*0.2)
    moveCircle(eyes[2],(screen_x+self.gridSize*GHOST_SIZE*(-0.3+dx), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy)), self.gridSize*GHOST_SIZE*0.08)
    moveCircle(eyes[3],(screen_x+self.gridSize*GHOST_SIZE*(0.3+dx), screen_y-self.gridSize*GHOST_SIZE*(0.3-dy)), self.gridSize*GHOST_SIZE*0.08)

  def DrawWalls(self, wallMatrix):
    wallColor = WALL_COLOR
    for xNum, x in enumerate(wallMatrix):
      if self.capture and (xNum * 2) < len(wallMatrix): wallColor = TEAM_COLORS[0]
      if self.capture and (xNum * 2) >= len(wallMatrix): wallColor = TEAM_COLORS[1]

      for yNum, cell in enumerate(x):
        if cell: # There's a wall here
          pos = (xNum, yNum)
          screen = self.to_screen(pos)
          screen2 = self.to_screen2(pos)

          # draw each quadrant of the square based on adjacent walls
          wIsWall = self.IsWall(xNum-1, yNum, wallMatrix)
          eIsWall = self.IsWall(xNum+1, yNum, wallMatrix)
          nIsWall = self.IsWall(xNum, yNum+1, wallMatrix)
          sIsWall = self.IsWall(xNum, yNum-1, wallMatrix)
          nwIsWall = self.IsWall(xNum-1, yNum+1, wallMatrix)
          swIsWall = self.IsWall(xNum-1, yNum-1, wallMatrix)
          neIsWall = self.IsWall(xNum+1, yNum+1, wallMatrix)
          seIsWall = self.IsWall(xNum+1, yNum-1, wallMatrix)

          # NE quadrant
          if (not nIsWall) and (not eIsWall):
            # inner circle
            circle(screen2, WALL_RADIUS * self.gridSize, wallColor, wallColor, (0,91), 'arc')
          if (nIsWall) and (not eIsWall):
            # vertical line
            line(add(screen, (self.gridSize*WALL_RADIUS, 0)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-0.5)-1)), wallColor)
          if (not nIsWall) and (eIsWall):
            # horizontal line
            line(add(screen, (0, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(-1)*WALL_RADIUS)), wallColor)
          if (nIsWall) and (eIsWall) and (not neIsWall):
            # outer circle
            circle(add(screen2, (self.gridSize*2*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, wallColor, wallColor, (180,271), 'arc')
            line(add(screen, (self.gridSize*2*WALL_RADIUS-1, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(-1)*WALL_RADIUS)), wallColor)
            line(add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS+1)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-0.5))), wallColor)

          # NW quadrant
          if (not nIsWall) and (not wIsWall):
            # inner circle
            circle(screen2, WALL_RADIUS * self.gridSize, wallColor, wallColor, (90,181), 'arc')
          if (nIsWall) and (not wIsWall):
            # vertical line
            line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, 0)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-0.5)-1)), wallColor)
          if (not nIsWall) and (wIsWall):
            # horizontal line
            line(add(screen, (0, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5)-1, self.gridSize*(-1)*WALL_RADIUS)), wallColor)
          if (nIsWall) and (wIsWall) and (not nwIsWall):
            # outer circle
            circle(add(screen2, (self.gridSize*(-2)*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, wallColor, wallColor, (270,361), 'arc')
            line(add(screen, (self.gridSize*(-2)*WALL_RADIUS+1, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5), self.gridSize*(-1)*WALL_RADIUS)), wallColor)
            line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS+1)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-0.5))), wallColor)

          # SE quadrant
          if (not sIsWall) and (not eIsWall):
            # inner circle
            circle(screen2, WALL_RADIUS * self.gridSize, wallColor, wallColor, (270,361), 'arc')
          if (sIsWall) and (not eIsWall):
            # vertical line
            line(add(screen, (self.gridSize*WALL_RADIUS, 0)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(0.5)+1)), wallColor)
          if (not sIsWall) and (eIsWall):
            # horizontal line
            line(add(screen, (0, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(1)*WALL_RADIUS)), wallColor)
          if (sIsWall) and (eIsWall) and (not seIsWall):
            # outer circle
            circle(add(screen2, (self.gridSize*2*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, wallColor, wallColor, (90,181), 'arc')
            line(add(screen, (self.gridSize*2*WALL_RADIUS-1, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5, self.gridSize*(1)*WALL_RADIUS)), wallColor)
            line(add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS-1)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(0.5))), wallColor)

          # SW quadrant
          if (not sIsWall) and (not wIsWall):
            # inner circle
            circle(screen2, WALL_RADIUS * self.gridSize, wallColor, wallColor, (180,271), 'arc')
          if (sIsWall) and (not wIsWall):
            # vertical line
            line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, 0)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(0.5)+1)), wallColor)
          if (not sIsWall) and (wIsWall):
            # horizontal line
            line(add(screen, (0, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5)-1, self.gridSize*(1)*WALL_RADIUS)), wallColor)
          if (sIsWall) and (wIsWall) and (not swIsWall):
            # outer circle
            circle(add(screen2, (self.gridSize*(-2)*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, wallColor, wallColor, (0,91), 'arc')
            line(add(screen, (self.gridSize*(-2)*WALL_RADIUS+1, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5), self.gridSize*(1)*WALL_RADIUS)), wallColor)
            line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS-1)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(0.5))), wallColor)

  def IsWall(self, x, y, walls):
    if x < 0 or y < 0:
      return False
    if x >= len(walls) or y >= len(walls[0]):
      return False
    return True if walls[x][y] == 1 else False

  def DrawFood(self, foodMatrix ):
    foodImages = []
    color = FOOD_COLOR
    for xNum, x in enumerate(foodMatrix):
      imageRow = []
      foodImages.append(imageRow)
      for yNum, cell in enumerate(x):
        if cell: # There's food here
          screen = self.to_screen((xNum, yNum ))
          dot = circle( screen,
                        FOOD_SIZE * self.gridSize,
                        outlineColor = color, fillColor = color,
                        width = 1)
          imageRow.append(dot)
        else:
          imageRow.append(None)
    return foodImages

  def RemoveFood(self, cell, foodImages ):
    x, y = cell
    remove_from_screen(foodImages[x][y])

  def DrawAura(self, auraIndex):
      auraIndex.pop(0)
      auraImages = []
      color = LASER_COLOR
      for pos in auraIndex:
          screen = self.to_screen((pos[0], pos[1]))
          dot = circle( screen,
                        FOOD_SIZE * self.gridSize,
                        outlineColor = color, fillColor = color,
                        width = 1.5)
          auraImages.append(dot)
      return auraImages
  def RemoveAura(self,auraImages):
      for pos in auraImages:
          remove_from_screen(pos)
  def EndGraphics(self):
    clear_screen()
    end_graphics()
def add(x, y):
    return (x[0] + y[0], x[1] + y[1])
def dist(posX,posY):
    return math.sqrt(math.pow(posX[0]-posY[0],2)+math.pow(posX[1]-posY[1],2))