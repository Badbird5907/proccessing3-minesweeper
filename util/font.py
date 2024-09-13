from Processing3 import *
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