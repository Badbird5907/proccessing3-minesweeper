# Compilation Strategy: dev.badbird.processing.compiler.strategy.impl.graph.GraphCompilationStrategy
# GRAPH:
# isDirected: true, allowsSelfLoops: false, nodes: [renderer.renderer.py, renderer.score.py, util.ticker.py, renderer.input.py, util.board.py, util.bb.py, scene.initial.py, util.font.py, renderer.game.py, scene.end.py, main.py, scene.board.py, renderer.button.py, util.key.py, scene.scene.py], edges: [<renderer.renderer.py -> renderer.button.py>, <renderer.renderer.py -> renderer.input.py>, <renderer.input.py -> util.bb.py>, <renderer.input.py -> util.ticker.py>, <scene.initial.py -> renderer.button.py>, <scene.initial.py -> renderer.input.py>, <scene.initial.py -> util.board.py>, <scene.end.py -> renderer.button.py>, <scene.end.py -> util.board.py>, <main.py -> renderer.input.py>, <main.py -> renderer.renderer.py>, <main.py -> util.font.py>, <main.py -> scene.board.py>, <main.py -> renderer.button.py>, <main.py -> scene.scene.py>, <main.py -> util.ticker.py>, <scene.board.py -> util.board.py>, <renderer.button.py -> util.bb.py>, <scene.scene.py -> scene.board.py>, <scene.scene.py -> scene.end.py>, <scene.scene.py -> scene.initial.py>]

# COMPILER_BEGIN: util.bb.py


def fixBB(bb):
  return [(min(bb[0][0], bb[1][0]), min(bb[0][1], bb[1][1])), (max(bb[0][0], bb[1][0]), max(bb[0][1], bb[1][1]))]
def fixBBMin(bb):
  return (min(bb[0][0], bb[1][0]), min(bb[0][1], bb[1][1]))
def fixBBMax(bb):
  return (max(bb[0][0], bb[1][0]), max(bb[0][1], bb[1][1]))
def isInsideBB(bbMin, bbMax, pos):
  # min and max might be swapped
  fixedMin = fixBBMin((bbMin, bbMax))
  fixedMax = fixBBMax((bbMin, bbMax))
  if (pos[0] >= fixedMin[0] and pos[0] <= fixedMax[0] and pos[1] >= fixedMin[1] and pos[1] <= fixedMax[1]):
    return True
  return False

def isInsideBBList(bbList, pos):
  for bb in bbList:
    if isInsideBB(bb[0], bb[1], pos):
      return True
  return False

def isPlayerInsideBB(bb):
  global pX, pY
  return isInsideBB(bb[0], bb[1], (pX, pY))

def drawBB(min, max, rgb = (255, 0, 0)):
  stroke(rgb[0], rgb[1], rgb[2])
  noFill()
  rect(min[0], min[1], max[0] - min[0], max[1] - min[1])
  return

def isOnEdgeOfBB(bbMin, bbMax, pos):
  fixedMin = fixBBMin((bbMin, bbMax))
  fixedMax = fixBBMax((bbMin, bbMax))
  if (pos[0] == fixedMin[0] or pos[0] == fixedMax[0] or pos[1] == fixedMin[1] or pos[1] == fixedMax[1]):
    return True
  return False

# COMPILER_END: util.bb.py

# COMPILER_BEGIN: util.ticker.py
def update():
  global tick
  tick += 1
  if tick >= 60:
      tick = 0

def isInterval(interval):
  global tick
  return tick % interval == 0

def getTick():
  global tick
  return tick

# COMPILER_END: util.ticker.py

# COMPILER_BEGIN: renderer.input.py


# TODO: Add support for multiline, proper cursor, etc..

def initInputRenderer():
  global textInputs, currentFocusedTextInput
  textInputs = {}
  currentFocusedTextInput = None
  return

def getTextInputWidth(txt):
  textSize(20)
  return textWidth(txt) + 40

def updateInputs():
  global textInputs
  newInputs = {}
  for input in textInputs:
    if millis() - textInputs[input]["timestamp"] < 250:
      newInputs[input] = textInputs[input]
  textInputs = newInputs
  return

def drawTextInput(id, x, y, desc, tabIndex, defaultValue="", height=None, width=None):
  global currentFocusedTextInput, textInputs
  if height == None:
    height = 45
  if width == None:
    width = getTextInputWidth(desc)
  min = (x, y)
  max = (x + width, y + height)
  focused = currentFocusedTextInput == id
  currentInput = textInputs[id] if id in textInputs else None
  textInputs[id] = {
    "id": id,
    "min": min,
    "max": max,
    "description": desc,
    "timestamp": millis(),
    "tabIndex": tabIndex,
    "value": currentInput["value"] if currentInput != None else defaultValue
  }
  value = textInputs[id]["value"]
  mouse = (mouseX, mouseY)
  hovering = isInsideBB(min, max, mouse)
  fill(255)
  if hovering:
    fill(200)
  
  rect(x, y, width, height)
  fill(0)
  textSize(20)
  showDesc = value != "" or focused
  displayValue = value if showDesc else desc
  tw = textWidth(displayValue)
  if (showDesc):
    # gray
    fill(77, 77, 77)
  text(displayValue, x + 20, y + 30)
  if (focused):
    tick = getTick()
    if tick % 60 < 30:
      # displayValue += "|"
      text("|", x + 20 + tw, y + 30)
  if mousePressed:
    if hovering:
      currentFocusedTextInput = id
    elif currentFocusedTextInput == id:
      currentFocusedTextInput = None
  return value

def inputKeyPressed():
  global textInputs, currentFocusedTextInput
  if currentFocusedTextInput != None:
    currentInput = textInputs[currentFocusedTextInput]
    if key == BACKSPACE:
      textInputs[currentFocusedTextInput]["value"] = currentInput["value"][:-1]
    elif key == ENTER:
      currentFocusedTextInput = None
    elif key == TAB:
      currentFocusedTextInput = None
      tabIndex = currentInput["tabIndex"]
      nextInput = None
      lowestInput = None # (tabIndex, id)

      for input in textInputs:
        if textInputs[input]["tabIndex"] == tabIndex + 1:
          nextInput = input
        elif lowestInput == None or textInputs[input]["tabIndex"] < lowestInput[0]:
          lowestInput = (textInputs[input]["tabIndex"], input)
      if nextInput != None:
        currentFocusedTextInput = nextInput
      elif lowestInput != None:
        currentFocusedTextInput = lowestInput[1]
    else:
      print(key, type(key))
      # check if it is unicode
      if type(key) == str or type(key) == unicode:
        textInputs[currentFocusedTextInput]["value"] += key
  return

# COMPILER_END: renderer.input.py

# COMPILER_BEGIN: renderer.button.py


def initButtonRenderer():
  global buttonSprites, buttons, clicked_buttons
  buttonSprites = {}
  buttons = {}
  clicked_buttons = {}
  return

def getTxtButtonWidth(txt):
  textSize(20)
  return textWidth(txt) + 40

def updateButtons():
  global buttons, mspt_total, clicked_buttons
  new_buttons = {}
  for button in buttons: 
    if millis() - buttons[button]["timestamp"] < 250 + mspt_total:
      new_buttons[button] = buttons[button]
  buttons = new_buttons
  ids = []
  for button in clicked_buttons:
    if millis() - clicked_buttons[button]["timestamp"] > 250 + mspt_total: # if it isn't handled in 250ms
      ids.append(button)
  if len(ids) > 0:
    new_clicked_buttons = {}
    for button in clicked_buttons:
      if button not in ids:
        new_clicked_buttons[button] = clicked_buttons[button]
    clicked_buttons = new_clicked_buttons
  return

def buttonsHandleClick(): # handle release
  global buttons, clicked_buttons
  mouse = (mouseX, mouseY) 
  for button in buttons:
    btn = buttons[button]
    if (isInsideBB(btn["min"], btn["max"], mouse)):
      print("clicked", button)
      clicked_buttons[button] = {
        "id": button,
        "timestamp": millis()
      }

def isButtonClicked(id):
  global clicked_buttons
  if (id in clicked_buttons):
    # remove it
    del clicked_buttons[id]
    return True
  return False

def drawTextButton(id, x,y, txt, height=None,width=None):
  global buttons
  textSize(20)
  if height == None:
    height = 45
  if width == None:
    width = getTxtButtonWidth(txt)

  # button bounds
  min = (x, y)
  max = (x + width, y + height)
  buttons[id] = {
    "id": id,
    "min": min,
    "max": max,
    "txt": txt,
    "timestamp": millis()
  }
  mouse = (mouseX, mouseY)
  if (isInsideBB(min, max, mouse)):
    fill(0, 255, 0)
    # cursor(HAND)
  else:
    fill(255, 255, 255)
    # cursor(ARROW)
  
  rect(x, y, width, height)
  fill(0, 0, 0)
  # text(txt, x + 20, y + 30)
  # draw in the center of the button
  text(txt, x + (width - textWidth(txt)) / 2, y + 30)
  return

def getHoverScale(min, max):
  global currentHover, currentHoverTime
  mouse = (mouseX, mouseY)
  if (isInsideBB(min, max, mouse)):
    currentHover = True
    currentHoverTime += 1
    return 1 + (currentHoverTime / 10)
  currentHover = False
  currentHoverTime = 0
  return 1

# COMPILER_END: renderer.button.py

# COMPILER_BEGIN: renderer.renderer.py

def initRenderers():
  initButtonRenderer()
  initInputRenderer()

# COMPILER_END: renderer.renderer.py

# COMPILER_BEGIN: util.font.py

from java.lang import System #!compiler_ignore
def loadMineSweeperFont():
  java_version = System.getProperty("java.version")
  print("Java: ",java_version)
  # if it is or above java 17, load the OTF font
  major = java_version.split(".")[0]
  print("Major: ",major)
  if (int(major) >= 17):
    print("Loading OTF")
    font = createFont("assets/mine-sweeper.otf", 30, True)
  else:
    print("Loading TTF")
    font = createFont("assets/mine-sweeper.ttf", 30)
  textFont(font)

# COMPILER_END: util.font.py

# COMPILER_BEGIN: util.board.py


import random #!compiler_ignore
from collections import deque #!compiler_ignore

def getBoard():
  if "board" not in globals():
    globals()["board"] = [[]]
  global board
  return board

def setBoard(newBoard):
  global board
  board = newBoard
  return

def checkWon():
  board = getBoard()
  for row in board:
    for cell in row:
      if not cell["mine"] and not cell["revealed"]:
        return False
  return True

def getNumMines(width, height):
  return int(width * height * 0.12)

def generateMines(ignorePos, nM=None):
  board = getBoard()
  boardHeight = len(board) - 1 # Number of rows (height)
  boardWidth = len(board[0])  # Number of columns (width)
  
  # Debug: Verify the board dimensions
  print("Board size: ", boardWidth, " (width) x ", boardHeight, " (height)")

  if nM is None:
    numMines = getNumMines(boardWidth, boardHeight)
  else:
      numMines = nM
  
  print("Generating", numMines, "mines for a board of", boardWidth, "x", boardHeight)
  
  for _ in range(numMines):
      print("Generating mine #", _)
      x = random.randint(0, boardWidth - 1)  # Random column within valid range
      y = random.randint(0, boardHeight - 1)  # Random row within valid range
      
      print("Generated mine at", x, y)
      
      if x >= boardWidth:
        print(" !!!!! (x) Mine out of bounds at", x, y)
      if y >= boardHeight:
        print(" !!!!! (y) Mine out of bounds at", x, y)

      # Keep regenerating if we land on a mine
      while board[y][x]["mine"] or (x, y) == ignorePos:
          x = random.randint(0, boardWidth - 1)
          y = random.randint(0, boardHeight - 1)
          print(" -> Regenerated mine at", x, y)
      # check out of bounds
      if x >= boardWidth:
        print(" !!!!! (x) Mine out of bounds at", x, y)
      if y >= boardHeight:
        print(" !!!!! (y) Mine out of bounds at", x, y)
      print("  -> Final mine placed at", x, y)
      board[y][x]["mine"] = True  # Place mine
  print("Mines generated")
  return board

def generateBoard(width, height):
  global board
  board = [[]] # array of rows, each cell being { mine: false, revealed: false, flagged: false }
  for i in range(width):
    board.append([])
    for _ in range(height):
      board[i].append({
        "mine": False,
        "revealed": False,
        "flagged": False,
        "number": 0
      })
  return board

def getCell(x, y):
  return getBoard()[x][y]

def getCellWidth():
  return width // len(getBoard()[0])

def inBounds(x,y):
  board = getBoard()
  boardWidth = len(board)
  boardHeight = len(board[0])
  return x >= 0 and x < boardWidth-1 and y >= 0 and y < boardHeight

def countMines(x,y):
  board = getBoard()
  count = 0
  for i in range(-1,2):
    for j in range(-1,2):
      if inBounds(x + i, y + j):
        count += board[x + i][y + j]["mine"]
  return count

def hasAdjacentMines(x,y):
  return countMines(x,y) > 0

def revealCell(x,y):
  global board_setup
  if (not board_setup):
    board_setup = True
    generateMines(ignorePos=(x, y))
  cell = getCell(x,y)
  if cell["revealed"]:
    return "ok"
  # expand out
  queue = deque([(x,y)])
  while len(queue) > 0:
    x, y = queue.popleft()
    cell = getCell(x,y)
    if cell["revealed"]:
      continue
    cell["revealed"] = True # reveal the cell
    if cell["mine"]:
      return "mine"
    # expandOut
    mc = countMines(x,y)
    if mc == 0:
      for i in range(-1,2):
        for j in range(-1,2):
          if inBounds(x + i, y + j):
            queue.append((x + i, y + j))
    else:
      cell["number"] = mc
  
  if (checkWon()):
    global scene
    scene = "end"
  return "ok"

def revealAllMines():
  board = getBoard()
  for row in board:
    for cell in row:
      if cell["mine"]:
        cell["revealed"] = True
  return

# COMPILER_END: util.board.py

# COMPILER_BEGIN: scene.board.py


def setupBoard():
  global board_lost, board_setup
  board_lost = False
  board_setup = False
  return

def cleanupBoard():
  global board_lost, board_setup
  board_lost = False
  board_setup = False
  return

def drawBoard():
  global board_lost
  board = getBoard()
  cellWidth = getCellWidth()
  textSize(16)
  for i in range(len(board)):
    for j in range(len(board[i])):
      cell = board[i][j]
      if cell["revealed"]:
        fill(255)
      else:
        fill(125)
      rect(i * cellWidth, j * cellWidth, cellWidth, cellWidth)
      if board[i][j]["revealed"]:
        fill(0)
        if board[i][j]["mine"]:
          fill(255, 0, 0)
          text("M", i * cellWidth + cellWidth / 2, j * cellWidth + cellWidth / 2)
          fill(0)
        if board[i][j]["number"] != 0:
          text(board[i][j]["number"], i * cellWidth + cellWidth / 2, j * cellWidth + cellWidth / 2)
      if board[i][j]["flagged"]:
        fill(255, 0, 0)
        text("F", i * cellWidth + cellWidth / 2, j * cellWidth + cellWidth / 2)
        fill(0)
  if (board_lost):
    fill(255, 0, 0)
    textSize(32)
    text("Click to continue...", 100, 400)
  return

def boardClick(mouseX, mouseY):
  global board_lost
  if (board_lost):
    global scene
    scene = "end"
    return
  board = getBoard()
  cellWidth = getCellWidth()

  for i in range(len(board)):
    for j in range(len(board[i])):
      if mouseX > i * cellWidth and mouseX < i * cellWidth + cellWidth and mouseY > j * cellWidth and mouseY < j * cellWidth + cellWidth:
        jdfsh = revealCell(i,j)
        if (jdfsh == "mine"):
          revealAllMines()
          board_lost = True
          return

  return

# COMPILER_END: scene.board.py

# COMPILER_BEGIN: scene.end.py


def setupEnd():
  return
def drawEnd():
  global scene
  fill(255, 0, 0)
  textSize(32)
  won = checkWon()
  if won:
    color(0, 255, 0)
    text("You won!", 200, 290)
  else:
    color(255, 0, 0)
    text("You lost!", 200, 290)
  drawTextButton("restart", 250, 300, "Restart")
  if isButtonClicked("restart"):
    scene = "initial"
    return
  return
def cleanupEnd():
  return

# COMPILER_END: scene.end.py

# COMPILER_BEGIN: scene.initial.py



def setupInitial():
  return
def drawInitial():
  textSize(32)
  fill(255, 255, 255)
  text("Minesweeper", 200, 290)

  # [Width]x[Height]
  inputSize = 140
  text("x", 200 + inputSize + 30, 350)
  wStr = drawTextInput("width", 200, 310, "Width", 1, "8", None, inputSize)
  heightX = 200 + inputSize + 100
  hStr = drawTextInput("height", heightX, 310, "Height", 2, "8", None, inputSize + 20)

  if (wStr != "" and hStr != ""):
    if (not wStr.isdigit() or not hStr.isdigit()):
      fill(255, 0, 0)
      textSize(16)
      text("Width and Height must be integers", 150, 400)
      return


  w = int(wStr) if wStr != "" else 0
  h = int(hStr) if hStr != "" else 0
  if (w > 0 and h > 0):
    if (w > 16 or h > 16):
      fill(255, 0, 0)
      textSize(16)
      text("Warning: Board may not render correctly", 100, 400)
    drawTextButton("start", 300, 450, "Start")
    if isButtonClicked("start"):
      setBoard(generateBoard(w, h))
      global scene
      scene = "board"
  return
def cleanupInitial():
  return

# COMPILER_END: scene.initial.py

# COMPILER_BEGIN: scene.scene.py

def drawScene():
  scenes = {
    "initial": {
      "setup": setupInitial,
      "main": drawInitial,
      "cleanup": cleanupInitial
    }, 
    "board": {
      "setup": setupBoard,
      "main": drawBoard,
      "cleanup": cleanupBoard
    },
    "end": {
      "setup": setupEnd,
      "main": drawEnd,
    }
  }
  global scene, lastScene
  if scene != lastScene:
    scenes[scene]["setup"]()
    lastScene = scene
  scenes[scene]["main"]()
  return

# COMPILER_END: scene.scene.py

# COMPILER_BEGIN: main.py


def setup():
  global scene, lastScene
  size(750,750)
  scene = "initial"
  lastScene = None
  initRenderers()

  #loadMineSweeperFont()

  global tick, mspt, last_ticks, mspt_overhead, last_tick_overhead, last_tick_end, mspt_total
  mspt = 0
  tick = 0
  last_ticks = []
  mspt_overhead = 0
  last_tick_overhead = []
  last_tick_end = millis()
  mspt_total = 0

  return

def draw():
  global tick, mspt, last_ticks, mspt_overhead, last_tick_overhead, last_tick_end, total_ms, mspt_total # Overhead mspt is the entire time taken to render the frame, not just the game logic
  start = millis()

  overhead = start - last_tick_end
  last_tick_overhead.append(overhead)
  if len(last_tick_overhead) > 10:
    last_tick_overhead.pop(0)
  mspt_overhead = sum(last_tick_overhead) / len(last_tick_overhead)
  clear()
  update()
  drawScene()
  updateButtons()


  ms = millis() - start
  last_ticks.append(ms)
  if len(last_ticks) > 10:
    last_ticks.pop(0)
  mspt = sum(last_ticks) / len(last_ticks)

  mspt_total = mspt + mspt_overhead

  last_tick_end = millis()


def mouseReleased():
  print("mouse down")
  print(mouseX, mouseY)
  buttonsHandleClick()
  global scene
  if (scene == "board"):
    boardClick(mouseX, mouseY)

def keyPressed():
  inputKeyPressed()

# COMPILER_END: main.py

