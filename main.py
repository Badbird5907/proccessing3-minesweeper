from Processing3 import *
from renderer.button import *
from renderer.renderer import *
from renderer.input import *
from scene.scene import *
from scene.board import boardClick
from util.font import *
from util.ticker import *

def setup():
  global scene, lastScene
  size(750,750)
  scene = "initial"
  lastScene = None
  initRenderers()

  loadMineSweeperFont()

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