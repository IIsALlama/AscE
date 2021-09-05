import AscE

class Vect2():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Component():
    def __init__(self, dependancies=[]):
        self.gameObject = None
        self.dependancies = dependancies
        self.OnAwake()

class Camera(Component):
    def __init__(self, size=Vect2(25, 25)):
        self.type = Camera
        self.size = size
        Component.__init__(self, [Transform()])
    def OnUpdate(self):
        pass
    def OnAwake(self):
        pass
    def RenderView(self, Renderers):
        position = self.gameObject.GetComponent(Transform).position
        pixels = []
        for x in range(position.x - AscE.math.floor(self.size.x/2), position.x + AscE.math.ceil(self.size.x/2)):
            temp = []
            for y in range(position.y - AscE.math.floor(self.size.y/2), position.y + AscE.math.ceil(self.size.y/2)):
                temp.append(pixel(Vect2(x,y), []))
            pixels.append(temp)
        for x in range(len(Renderers)):
            subpixels = Renderers[x].GetComponent(Renderer).GetPixels(Renderers[x].GetComponent(Transform).roundedPosition)
            for i in range(len(subpixels)):
                pos = subpixels[i].position
                for x in pixels:
                    for y in x:
                        if (y.position.x == subpixels[i].position.x and y.position.y == subpixels[i].position.y):
                            y.subpixels.append(subpixels[i])
        return pixels

class pixel():
    def __init__(self, position=Vect2(0,0), subpixels=[]):
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
    def __init__(self, position=Vect2(0,0), character="  ", priority=0, colour="white"):
        self.character = character[:2]
        self.position = position
        self.priority = priority
        self.colour = colour

class Transform(Component):
    def __init__(self, position=Vect2(0,0)):
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
        return Vect2(round(position.x), round(position.y))
    def ReturnToStartPos(self):
        self.position = self.startPosition
    def MoveToPosition(self, position):
        x, y = self.position.x, self.position.y
        if (self.position.x < position.x and self.positionLock[0] == False):
            x = position.x
        if (self.position.x > position.x and self.positionLock[1] == False):
            x = position.x
        if (self.position.y < position.y and self.positionLock[2] == False):
            y = position.y
        if (self.position.y > position.y and self.positionLock[3] == False):
            y = position.y
        self.position = Vect2(x, y)

class Light(Component):
    def __init__(self, lightRadius=1, isDynamic=False):
        self.radius = lightRadius
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
            for x in range(camSize.x):
                temp = []
                for y in range(camSize.y):
                    temp.append(self.CalculateLightingForPixel(Vect2(x, y), True))
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
            thisPosition = self.gameObject.GetComponent(Transform).position
            distFromLight = (((thisPosition.x - pixelPos.x) ** 2) + ((thisPosition.y - pixelPos.y) ** 2)) ** 0.5
            val = distFromLight / self.radius
            return val
        else:
            return self.lightingPixels[pixelPos.x][pixelPos.y]

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
    def __init__(self, renderingPriority=0, colour="white", size=Vect2(1,1), usesLight=False):
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
        for x in range(position.x, position.x + self.size.x):
            for y in range(position.y, position.y + self.size.y):
                char = "██"
                if (self.usesLight):
                    light = AscE.FindClosestObjectWithComponent(Vect2(x,y), Light).GetComponent(Light)
                    value = light.CalculateLightingForPixel(Vect2(x, y), False)
                    char = light.ReturnCharacterFromValue(value)
                    if (char == ""):
                        char = "  "
                filledPoses.append(subpixel(Vect2(x, y), char, self.renderingPriority, self.colour))
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
                filledPoses.append(subpixel(Vect2(position.x + x, position.y + y), self.sprite[y][x*2:], self.renderingPriority, self.colour))
        return filledPoses

class BoxCollider(Component):
    def __init__(self, isTrigger=False, size=Vect2(1, 1)):
        self.type = BoxCollider
        self.size = size
        self.isTrigger = isTrigger
        Component.__init__(self, [Transform()])
    def OnUpdate(self):
        thisTransform = self.gameObject.GetComponent(Transform)
        thisTransform.positionLock = (False, False, False, False)
        cs = AscE.FindObjectsWithComponent(BoxCollider)
        for x in range(len(cs)):
            if (cs[x].GetComponent(BoxCollider) != self):
                otherBC = cs[x].GetComponent(BoxCollider)
                otherT = cs[x].GetComponent(Transform)
                otherT = otherT.RoundPosition(otherT.position)
                thisPos = thisTransform.RoundPosition(thisTransform.position)
                if (self.IsCollidingWithOther(thisPos, otherBC, otherT)):
                    newLock = (False, False, False, False)
                    if (thisPos.x + self.size.x == otherT.x):
                        newLock = (True, False, False, False)
                    if (thisPos.x == otherT.x + otherBC.size.x):
                        newLock  = (False, True, False, False)
                    if (thisPos.y + self.size.y == otherT.y):
                        newLock  = (False, False, True, False)
                    if (thisPos.y == otherT.y + otherBC.size.y):
                        newLock  = (False, False, False, True)

                    if (thisTransform.positionLock[0] == True):
                        newLock = (True, newLock[1], newLock[2], newLock[3])
                    if (thisTransform.positionLock[1] == True):
                        newLock = (newLock[0], True, newLock[2], newLock[3])
                    if (thisTransform.positionLock[2] == True):
                        newLock = (newLock[0], newLock[1], True, newLock[3])
                    if (thisTransform.positionLock[3] == True):
                        newLock = (newLock[0], newLock[1], newLock[2], True)
                    thisTransform.positionLock = newLock
                
    def OnAwake(self):
        pass
    def IsCollidingWithOther(self, thisPosition, otherCollider, otherColliderPosition):
        val = False
        if thisPosition.x <= otherColliderPosition.x + otherCollider.size.x and thisPosition.x + self.size.x >= otherColliderPosition.x:
            if thisPosition.y <= otherColliderPosition.y + otherCollider.size.y and thisPosition.y + self.size.y >= otherColliderPosition.y:
                val = True
        return val
        
class TopDownMovement(Component):
    def __init__(self, speed=1):
        self.type = TopDownMovement
        self.speed = speed
        Component.__init__(self, [Transform()])
    def OnUpdate(self):
        if (AscE.GetKey("up")):
            t = self.gameObject.GetComponent(Transform)
            pos = Vect2(t.position.x, t.position.y - (self.speed * AscE.DeltaTime()))
            t.MoveToPosition(pos)
        if (AscE.GetKey("down")):
            t = self.gameObject.GetComponent(Transform)
            pos = Vect2(t.position.x, t.position.y + (self.speed * AscE.DeltaTime()))
            t.MoveToPosition(pos)
        if (AscE.GetKey("left")):
            t = self.gameObject.GetComponent(Transform)
            pos = Vect2(t.position.x - (self.speed * AscE.DeltaTime()), t.position.y)
            t.MoveToPosition(pos)
        if (AscE.GetKey("right")):
            t = self.gameObject.GetComponent(Transform)
            pos = Vect2(t.position.x + (self.speed * AscE.DeltaTime()), t.position.y)
            t.MoveToPosition(pos)
    def OnAwake(self):
        pass
