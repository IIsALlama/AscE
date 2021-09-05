import os, time, sys, math
sys.path.insert(0, './__AscE__/Libs')

import keyboard
from keyboard import mouse
from termcolor import colored

from Components import *
from AscE_Components import *

objects = []#Holds every active game object
scenes = []#Holds every scene
Cam = None
lastFrameTime = 0
currentSceneIndex = 0

def GetKey(key):
    return keyboard.is_pressed(key)

def MousePos():
    pos = mouse.get_position
    return Vect2(pos[0], pos[1])

def GetClickLeft():
    return mouse.is_pressed(mouse.LEFT)

def GetClickRight():
    return mouse.is_pressed(mouse.RIGHT)

def DestroyObject(obj):
    global objects
    objects.remove(obj)
    return obj

def FindObject(name):#Find an object by it's name
    for x in range(len(objects)):
        if (objects[x].name == name):
            return objects[x]
    return None

def FindObjectsWithComponent(componentType):#Find all objects with a component
    objs = []
    for x in range(len(objects)):
        if (objects[x].GetComponent(componentType) != None):
            objs.append(objects[x])
    return objs

def FindObjectWithComponent(componentType):#Find object with a component
    for x in range(len(objects)):
        if (objects[x].GetComponent(componentType) != None):
            return objects[x]
    return None

def FindClosestObjectWithComponent(pos, componentType):
    closestPos = None
    for x in range(len(objects)):
        if (objects[x].GetComponent(componentType) != None):
            objPos = objects[x].GetComponent(Transform).position
            if (closestPos == None):
                closestPos = DistanceBetween(objPos, pos)
                closest = objects[x]
            elif (DistanceBetween(objPos, pos) < closestPos):
                closestPos = DistanceBetween(objPos, pos)
                closest = objects[x]
    return closest

def DistanceBetween(pos1, pos2):
    return (((pos1.x - pos2.x) ** 2) + ((pos1.y - pos2.y) ** 2)) ** 0.5

def DeltaTime(): #Time since last frame
    return time.time() - lastFrameTime

def UpdateFrameTime(t):
    global lastFrameTime
    lastFrameTime = t

def ClearFrame():#Clear Frame
    os.system("cls")

def UpdateFrame():#Update the frame to currentFrame
    if (Cam != None):
        rs = FindObjectsWithComponent(Renderer)
        pixels = Cam.RenderView(rs)
        ClearFrame()
        for y in range(Cam.size.y):
            temp = ""
            for x in range(Cam.size.x):
                temp += colored(pixels[x][y].GetCharacter(), pixels[x][y].GetColour())
            print(temp)

def LoadScene(sceneIndex):
    global objects
    for x in range(len(scenes)):
        s = scenes[x]()
        if (s.sceneIndex == sceneIndex):
            objects = s.sceneObjects
            global Cam
            Cam = FindObjectWithComponent(Camera).GetComponent(Camera)
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
        for x in range(len(self.components)):
            self.components[x].gameObject = self
        global objects
        objects.append(self)
    def AddComponent(self, component):
        for x in range(len(component.dependancies)):
            if (self.GetComponent(component.dependancies[x]) == None):
                self.AddComponent(component.dependancies[x])
        self.components.append(component)
    def RemoveComponent(self, component):
        self.components.remove(component)
    def GetComponent(self, component):
        for x in range(len(self.components)):
            if (self.components[x].type == component):
                    return self.components[x]
        return None
