import sys
sys.path.insert(0, './__AscE__')
from AscE import *

class MainScene(Scene):
    def __init__(thisScene):
        Scene.__init__(thisScene, index=0)

        thisScene.sceneObjects.append(obj("Camera",
                     [Transform((0, 0)),
                      Camera((25, 25))]))

        thisScene.sceneObjects.append(obj("Text",
                     [Transform(),
                     SpriteRenderer(2, "white", ["AscE Test "])]))

        thisScene.sceneObjects.append(obj("Ground",
                     [Transform((0, 0)),
                     QuadRenderer(1, "white", (25, 25), False)]))

        thisScene.sceneObjects.append(obj("Player",
                     [Transform((10, 10)),
                     QuadRenderer(2, "green", (2, 2), False),
                     TopDownMovement("Player", 50),
                    BoxCollider("Player", False, (2, 2))]))

        #thisScene.sceneObjects.append(obj("Light",
                     #[Transform((12, 12)),
                     #Light("Light", 5, False)]))

        thisScene.sceneObjects.append(obj("Object",
                     [Transform((15, 10)),
                     QuadRenderer(2, "red", (5, 2), False),
                    BoxCollider("Object", False, (5, 2))]))    

class Scene2(Scene):
    def __init__(thisScene):
        Scene.__init__(thisScene, index=1)

        thisScene.sceneObjects.append(obj("Camera2",
                     [Transform((0, 0)),
                      Camera((25, 25))]))
        
        thisScene.sceneObjects.append(obj("Player2",
                     [Transform((5, 10)),
                     QuadRenderer(2, "blue", (2, 2)),
                     TopDownMovement("Player2", 75)]))

        thisScene.sceneObjects.append(obj("Text2",
                     [Transform(),
                     SpriteRenderer(2, "white", ["Scene 2 "])]))
        
        
        
        

    
    
