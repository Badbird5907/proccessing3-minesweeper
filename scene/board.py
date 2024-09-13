from Processing3 import *
from util.board import *

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