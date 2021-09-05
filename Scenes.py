import sys
sys.path.insert(0, './__AscE__')
from AscE import *

class ExampleScene(Scene):
    def __init__(thisScene):
        Scene.__init__(thisScene, index=0)

        thisScene.sceneObjects.append(obj("Camera",
                     [Transform(Vect2(0, 0)),
                      Camera(Vect2(25, 25))]))

        thisScene.sceneObjects.append(obj("Text",
                     [Transform(Vect2(-12, -12)),
                     SpriteRenderer(2, "white", ["AscE Game "])]))

        thisScene.sceneObjects.append(obj("Player",
                     [Transform(Vect2(10, 10)),
                     QuadRenderer(2, "green", Vect2(2, 2), False),
                     BoxCollider(False, Vect2(2, 2)),
                     TopDownMovement(50)]))

        
        
        

    
    
