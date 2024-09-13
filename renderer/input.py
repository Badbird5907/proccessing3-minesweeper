from Processing3 import *
from util.bb import *
from util.ticker import *

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