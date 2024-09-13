from scene.initial import *
from scene.board import *
from scene.end import *

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