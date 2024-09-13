from Processing3 import *

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