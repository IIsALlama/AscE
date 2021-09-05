import sys
sys.path.insert(0, './__AscE__')
from AscE import *
from Scenes import *

debug = False

def Initialise():#Initialise Game
    keyboard.on_press_key("f2", ChangeDebug)
    s = Scene.__subclasses__()
    global scenes
    for x in range(len(s)):
        scenes.append(s[x])
    LoadScene(0)
    time.sleep(0.01)
    UpdateCode()

def ChangeDebug(arg):
    global debug
    debug = not debug

def UpdateCode():#Update function runs every 0.01 seconds + time to run code for that frame.
    while True:
        colliders = FindObjectsWithComponent(BoxCollider)
        for x in range(len(colliders)):
            colliders[x].GetComponent(BoxCollider).OnUpdate()
        for x in range(len(objects)):
            for i in range(len(objects[x].components)):
                if (not(objects[x].components in colliders)):
                    try:
                        objects[x].components[i].OnUpdate()
                    except Exception:
                        pass
                try:
                    objects[x].components[i].AfterUpdate()
                except Exception:
                    pass
        UpdateFrame()
        if (debug):
            print("Scene : " + scenes[CurrentScene()].__name__)
            print("Delta Time : " + str(DeltaTime()))
            print("==Active Objects==")
            print(len(objects), "active objects")
            for x in range(len(objects)):
                print(objects[x].name)
        UpdateFrameTime(time.time())
        time.sleep(0.01)
Initialise()
