import sys
sys.path.insert(0, './__AscE__')
from AscE import *

class MainScene(Scene):
    def __init__(thisScene):
        Scene.__init__(thisScene, index=0)

        thisScene.sceneObjects.append(obj("Camera",
                     [Transform(Vect2(0, 0)),
                      Camera(Vect2(25, 25))]))

        thisScene.sceneObjects.append(obj("Text",
                     [Transform(Vect2(0, 0)),
                     SpriteRenderer(2, "white", ["AscE Test "])]))

        thisScene.sceneObjects.append(obj("Ground",
                     [Transform(Vect2(-12, -12)),
                     QuadRenderer(1, "white", Vect2(25, 25), False)]))

        thisScene.sceneObjects.append(obj("Player",
                     [Transform(Vect2(10, 10)),
                     QuadRenderer(2, "green", Vect2(2, 2), False),
                     BoxCollider(False, Vect2(2, 2)),
                     TopDownMovement(50)]))

        thisScene.sceneObjects.append(obj("Wall",
                     [Transform(Vect2(5, 5)),
                     QuadRenderer(2, "red", Vect2(2, 6), False),
                     BoxCollider(False, Vect2(2, 6))]))

class Scene2(Scene):
    def __init__(thisScene):
        pass
        
        
        
        

    
    
