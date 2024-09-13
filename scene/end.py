from Processing3 import *
from renderer.button import *
from util.board import *

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