from Processing3 import *

from renderer.button import *
from util.board import *
from renderer.input import *

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