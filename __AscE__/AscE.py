import os, time, sys, math
sys.path.insert(0, './__AscE__/Libs')

import keyboard
from termcolor import colored

from Components import *
from AscE_Components import *

objects = []#Holds every active game object
scenes = []#Holds every scene
lastFrameTime = 0
currentSceneIndex = 0

def GetKey(key):
    return keyboard.is_pressed(key)

def DestroyObject(obj):
    global objects
    objects.remove(obj)
    return obj

def CreateObject(obj):
    global objects
    objects.append(obj)
    return obj
    
def FindObject(name):#Find an object by it's name
    for x in range(len(objects)):
        if (objects[x].name == name):
            return objects[x]
    return "null"

def FindObjectsWithComponent(componentType):#Find all objects with a component
    objs = []
    for x in range(len(objects)):
        if (objects[x].GetComponent(componentType) != "null"):
            objs.append(objects[x])
    return objs

def FindObjectWithComponent(componentType):#Find object with a component
    for x in range(len(objects)):
        if (objects[x].GetComponent(componentType) != "null"):
            return objects[x]
    return "null"

def FindClosestObjectWithComponent(pos, componentType):
    closestPos = "null"
    for x in range(len(objects)):
        if (objects[x].GetComponent(componentType) != "null"):
            objPos = objects[x].GetComponent(Transform).position
            if (closestPos == "null"):
                closestPos = DistanceBetween(objPos, pos)
                closest = objects[x]
            elif (DistanceBetween(objPos, pos) < closestPos):
                closestPos = DistanceBetween(objPos, pos)
                closest = objects[x]
    return closest

def DistanceBetween(pos1, pos2):
    return (((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2)) ** 0.5

def DeltaTime(): #Time since last frame
    return time.time() - lastFrameTime

def UpdateFrameTime(t):
    global lastFrameTime
    lastFrameTime = t

def ClearFrame():#Clear Frame
    os.system("cls")

def UpdateFrame():#Update the frame to currentFrame
    Cam = FindObjectWithComponent(Camera).GetComponent(Camera)
    if (Cam != "null"):
        rs = FindObjectsWithComponent(Renderer)
        pixels = Cam.RenderView(rs)
        ClearFrame()
        for y in range(Cam.size[1]):
            temp = ""
            for x in range(Cam.size[0]):
                temp += colored(pixels[x][y].GetCharacter(), pixels[x][y].GetColour())
            print(temp)

def LoadScene(sceneIndex):
    global objects
    for x in range(len(scenes)):
        s = scenes[x]()
        if (s.sceneIndex == sceneIndex):
            objects = s.sceneObjects
            global currentSceneIndex
            currentSceneIndex = sceneIndex
            return

def CurrentScene():
    return currentSceneIndex

class Scene():#Game Object class
    def __init__(self, index=0):
        self.sceneIndex = index
        self.sceneObjects = []

class obj():#Game Object class
    def __init__(self,name="New Object",components=[]):
        self.name = name
        self.components = components
        global objects
        objects.append(self)
    def AddComponent(self, component):
        for x in range(len(component.dependancies)):
            if (self.GetComponent(component.dependancies[x]) == "null"):
                self.AddComponent(component.dependancies[x])
        self.components.append(component)
    def RemoveComponent(self, component):
        self.components.remove(component)
    def GetComponent(self, component):
        for x in range(len(self.components)):
            if (self.components[x].type == component):
                    return self.components[x]
        return "null"
