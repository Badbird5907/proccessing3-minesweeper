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

  # scale the text down to fit the cell
  ts = min(cellWidth * 0.50, 16)
  textSize(ts)

  flag = loadImage("assets/flag.png")
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
        centerX = i * cellWidth + cellWidth / 2
        centerY = j * cellWidth + cellWidth / 2
        textHeight = textAscent() + textDescent()
        if board[i][j]["mine"]:
          fill(255, 0, 0)
          # text("M", i * cellWidth + cellWidth / 2, j * cellWidth + cellWidth / 2)
          lSize = textWidth("M")
          text("M", centerX - lSize / 2, centerY + textHeight / 2)
          fill(0)
        if board[i][j]["number"] != 0:
          # text(board[i][j]["number"], i * cellWidth + cellWidth / 2, j * cellWidth + cellWidth / 2)
          st = str(board[i][j]["number"])
          lSize = textWidth(st)
          text(st, centerX - lSize / 2, centerY + textHeight / 2)
      if board[i][j]["flagged"]:
        #fill(255, 0, 0)
        #text("F", i * cellWidth + cellWidth / 2, j * cellWidth + cellWidth / 2)
        #fill(0)
        # Flag is 8x8 pixels, scale it down to fill 75% of the cell
        image(flag, i * cellWidth + cellWidth * 0.125, j * cellWidth + cellWidth * 0.125, cellWidth * 0.75, cellWidth * 0.75)
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
        # check right click
        if mouseButton == RIGHT:
          flagCell(i,j)
          return
        jdfsh = revealCell(i,j)
        if (jdfsh == "mine"):
          revealAllMines()
          board_lost = True
          return

  return