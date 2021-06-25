import AscE

class Component():
    def __init__(self, dependancies=[]):
        self.dependancies = dependancies
        self.OnAwake()

class Camera(Component):
    def __init__(self, size=(25,25)):
        self.type = Camera
        self.size = size
        Component.__init__(self, [Transform()])
    def OnUpdate(self):
        pass
    def OnAwake(self):
        pass
    def RenderView(self, Renderers):
        pixels = []
        for x in range(self.size[0]):
            temp = []
            for y in range(self.size[1]):
                temp.append(pixel((x,y), []))
            pixels.append(temp)
        for x in range(len(Renderers)):
            subpixels = Renderers[x].GetComponent(Renderer).GetPixels(Renderers[x].GetComponent(Transform).roundedPosition)
            for i in range(len(subpixels)):
                pos = subpixels[i].position
                try:
                    pixels[pos[0]][pos[1]].subpixels.append(subpixels[i])
                except:
                    pass
        return pixels

class pixel():#Not a component
    def __init__(self, position=(0,0), subpixels=[]):
        self.position = position
        self.subpixels = subpixels
    def GetCharacter(self):
        current = subpixel()
        for x in range(len(self.subpixels)):
            if (current.priority <= self.subpixels[x].priority):
                current = self.subpixels[x]
        return current.character
    def GetColour(self):
        current = subpixel()
        for x in range(len(self.subpixels)):
            if (current.priority <= self.subpixels[x].priority):
                current = self.subpixels[x]
        return current.colour

class subpixel():#Not a component
    def __init__(self, position=(0,0), character="  ", priority=0, colour="white"):
        self.character = character[:2]
        self.position = position
        self.priority = priority
        self.colour = colour

class Transform(Component):
    def __init__(self, position=(0,0)):
        self.type = Transform
        self.position = position
        self.roundedPosition = self.RoundPosition(position)
        self.startPosition = position
        self.positionLock = (False, False, False, False)
        Component.__init__(self)
    def OnUpdate(self):
        self.roundedPosition = self.RoundPosition(self.position)
    def OnAwake(self):
        pass
    def RoundPosition(self, position):
        return (round(position[0]), round(position[1]))
    def ReturnToStartPos(self):
        self.position = self.startPosition
    def MoveToPosition(self, position):
        x, y = self.position[0], self.position[1]
        if (self.position[0] < position[0] and self.positionLock[0] == False):
            x = position[0]
        if (self.position[0] > position[0] and self.positionLock[1] == False):
            x = position[0]
        if (self.position[1] < position[1] and self.positionLock[2] == False):
            y = position[1]
        if (self.position[1] > position[1] and self.positionLock[3] == False):
            y = position[1]
        self.position = (x, y)

class Light(Component):
    def __init__(self, thisObjectName, lightRadius=1, isDynamic=False):
        self.radius = lightRadius
        self.thisObjectName = thisObjectName
        self.type = Light
        self.isDynamic = isDynamic
        self.lightingPixels = []
        self.baked = False
        Component.__init__(self, [Transform()])
    def OnUpdate(self):
        if (self.baked == False):
            self.BakeLights(AscE.FindObjectWithComponent(Camera).GetComponent(Camera).size)
            self.baked = True
    def OnAwake(self):
        pass
    def BakeLights(self, camSize):
        if (not self.isDynamic):
            for x in range(camSize[0]):
                temp = []
                for y in range(camSize[1]):
                    temp.append(self.CalculateLightingForPixel((x, y), True))
                self.lightingPixels.append(temp)
    def ReturnCharacterFromValue(self, value):
        if (value < 0.25):
            return "██"
        elif (value < 0.4):
            return "▓▓"
        elif (value < 0.6):
            return "▒▒"
        elif (value < 1):
            return "░░"
        else:
            return "  "
    def CalculateLightingForPixel(self, pixelPos, forceDynamic=False):
        if (self.isDynamic or forceDynamic):
            thisPosition = AscE.FindObject(self.thisObjectName).GetComponent(Transform).position
            distFromLight = (((thisPosition[0] - pixelPos[0]) ** 2) + ((thisPosition[1] - pixelPos[1]) ** 2)) ** 0.5
            val = distFromLight / self.radius
            return val
        else:
            return self.lightingPixels[pixelPos[0]][pixelPos[1]]

class Renderer(Component):
    def __init__(self, renderingPriority=0, colour="white"):
        self.type = Renderer
        self.renderingPriority = renderingPriority
        self.colour = colour
        Component.__init__(self, [Transform()])
    def OnUpdate(self):
        pass
    def OnAwake(self):
        pass
    def GetPixels(self, position):
        return []

class QuadRenderer(Renderer):
    def __init__(self, renderingPriority=0, colour="white", size=(1,1), usesLight=False):
        self.type = Renderer
        self.size = size
        self.usesLight = usesLight
        Renderer.__init__(self, renderingPriority, colour)
    def OnUpdate(self):
        pass
    def OnAwake(self):
        pass
    def GetPixels(self, position):
        filledPoses = []
        for x in range(position[0], position[0] + self.size[0]):
            for y in range(position[1], position[1] + self.size[1]):
                char = "██"
                if (self.usesLight):
                    light = AscE.FindClosestObjectWithComponent((x,y), Light).GetComponent(Light)
                    value = light.CalculateLightingForPixel((x, y), False)
                    char = light.ReturnCharacterFromValue(value)
                    if (char == ""):
                        char = "  "
                filledPoses.append(subpixel((x, y), char, self.renderingPriority, self.colour))
        return filledPoses

class SpriteRenderer(Renderer):
    def __init__(self, renderingPriority=0, colour="white", sprite=["╔═╗",
                                                                    "╚═╝"]):
        self.type = Renderer
        self.sprite = sprite
        Renderer.__init__(self, renderingPriority, colour)
    def OnUpdate(self):
        pass
    def OnAwake(self):
        pass
    def GetPixels(self, position):
        filledPoses = []
        for y in range(len(self.sprite)):
            for x in range(0, round(len(self.sprite[y])/2)):
                filledPoses.append(subpixel((position[0] + x, position[1] + y), self.sprite[y][x*2:], self.renderingPriority, self.colour))
        return filledPoses

class BoxCollider(Component):
    def __init__(self, thisObjectName, isTrigger=False, size=(1, 1)):
        self.type = BoxCollider
        self.size = size
        self.isTrigger = isTrigger
        self.thisObjectName = thisObjectName
        self.thisTransform = "null"
        Component.__init__(self, [Transform()])
    def OnUpdate(self):
        if (self.thisTransform == "null"):
            self.thisTransform = AscE.FindObject(self.thisObjectName)
            if (self.thisTransform != "null"):
                self.thisTransform = self.thisTransform.GetComponent(Transform)
        else:
            self.thisTransform.positionLock = (False, False, False, False)
            cs = AscE.FindObjectsWithComponent(BoxCollider)
            for x in range(len(cs)):
                if (cs[x].GetComponent(BoxCollider) != self):
                    otherBC = cs[x].GetComponent(BoxCollider)
                    otherT = cs[x].GetComponent(Transform)
                    otherT = otherT.RoundPosition(otherT.position)
                    thisPos = self.thisTransform.RoundPosition(self.thisTransform.position)
                    if (self.IsCollidingWithOther(thisPos, otherBC, otherT)):
                        newLock = (False, False, False, False)
                        if (thisPos[0] + self.size[0] == otherT[0]):
                            newLock = (True, False, False, False)
                        if (thisPos[0] == otherT[0] + otherBC.size[0]):
                            newLock  = (False, True, False, False)
                        if (thisPos[1] + self.size[1] == otherT[1]):
                            newLock  = (False, False, True, False)
                        if (thisPos[1] == otherT[1] + otherBC.size[1]):
                            newLock  = (False, False, False, True)

                        if (self.thisTransform.positionLock[0] == True):
                            newLock = (True, newLock[1], newLock[2], newLock[3])
                        if (self.thisTransform.positionLock[1] == True):
                            newLock = (newLock[0], True, newLock[2], newLock[3])
                        if (self.thisTransform.positionLock[2] == True):
                            newLock = (newLock[0], newLock[1], True, newLock[3])
                        if (self.thisTransform.positionLock[3] == True):
                            newLock = (newLock[0], newLock[1], newLock[2], True)
                        self.thisTransform.positionLock = newLock
                
    def OnAwake(self):
        pass   
    def IsCollidingWithOther(self, thisPosition, otherCollider, otherColliderPosition):
        val = False
        if thisPosition[0] <= otherColliderPosition[0] + otherCollider.size[0] and thisPosition[0] + self.size[0] >= otherColliderPosition[0]:
            if thisPosition[1] <= otherColliderPosition[1] + otherCollider.size[1] and thisPosition[1] + self.size[1] >= otherColliderPosition[1]:
                val = True
        return val
        
class TopDownMovement(Component):
    def __init__(self, thisObjectName, speed=1):
        self.type = TopDownMovement
        self.thisObjectName = thisObjectName
        self.thisObject = "null"
        self.speed = speed
        Component.__init__(self, [Transform()])
    def OnUpdate(self):
        didMove = False
        if (self.thisObject == "null"):
            self.thisObject = AscE.FindObject(self.thisObjectName)
        if (AscE.GetKey("up")):
            t = self.thisObject.GetComponent(Transform)
            pos = (t.position[0], t.position[1] - (self.speed * AscE.DeltaTime()))
            t.MoveToPosition(pos)
        if (AscE.GetKey("down")):
            t = self.thisObject.GetComponent(Transform)
            pos = (t.position[0], t.position[1] + (self.speed * AscE.DeltaTime()))
            t.MoveToPosition(pos)
        if (AscE.GetKey("left")):
            t = self.thisObject.GetComponent(Transform)
            pos = (t.position[0] - (self.speed * AscE.DeltaTime()), t.position[1])
            t.MoveToPosition(pos)
        if (AscE.GetKey("right")):
            t = self.thisObject.GetComponent(Transform)
            pos = (t.position[0] + (self.speed * AscE.DeltaTime()), t.position[1])
            t.MoveToPosition(pos)
    def OnAwake(self):
        pass
