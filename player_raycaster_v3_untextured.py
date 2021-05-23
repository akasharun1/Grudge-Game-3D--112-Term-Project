# this is the camera class which can do the rayCasting and is moved throughout the maze

# inspiration for raycasting from 3d sage's explanation in C : https://www.youtube.com/watch?v=gYRrGTC7GtA&t=423s
# and also inspired from https://lodev.org/cgtutor/raycasting.html 

# cmu_112_graphics is from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html 
from cmu_112_graphics import *
# from main_v1 import *

# new changes 
# ive pretty much given up on texture mapping walls as its too slow for python
# unless i port the entire game over to pygame which would be painful

# i have however done stuff with sprite creation sans texture mapping
# I credit the inspiration for my sprite creation technique to current TA Terry Feng's
# implementation in his raycaster: https://www.youtube.com/watch?v=PM4WyIsWJ_8&ab_channel=TerryFeng
# github: https://github.com/feng-terry/pacman3d/blob/master/rayCast.py

# I was inspired by his technique of storing sprites that were seen in sets
# so that they wouldn't be created multiple times
# and using dictionaries and a distance List for drawing images 


# unlike his version though because I was casting sprites from images
# its harder in a way to centre them I guess 
# So I basically also draw them as a wall as well to better visualize their position
# and I down scale the image from its original size using cmu_112_graphics.py from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# depending on how far away the sprite is from the player.

# for the grudge you can visualize it as evil aura XD
# for cockroach maybe a swarm
# for the ring I guess its shiny gleam 
# pls visualize!

import math
class Camera():
    def __init__(self, x, y, dx, dy, angle):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.angle = angle

    # code for a possible birds eye view 
    def drawPlayer(self, canvas):
        cx , cy = self.x, self.y
        canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill = "yellow")
        # this is basically just a line a draw for me to to be able to visualize
        # the turning of the player
        x1 = self.dx*5 + cx
        y1 = self.dy*5 + cy
        canvas.create_line(self.x, self.y, x1, y1, fill= "yellow",  width = 5)


    # This is what makes the rayCasting magic happen
    def rayCast(self, map, canvas):

        # point of these is to ensure that image is only drawn once
        # and not as many times as there are rays hitting the block
        cockroachSet = set()
        grudgeSet = set()
        ringSet = set()

        objectsDict = {}
        distanceList = []

        rayExtension = map.rows

        # The basis of all the calculation I use come from the usage of trigonometry
        # and in particular using tangent, and the way I calculate differs depending
        # on the quadrant where the ray is cast

        # simple pythagorean theorem for distance
        def distance(x1,y1,x2,y2):
            return ((x1-x2)**2 +(y1-y2)**2)**0.5

        # 60 degree field of view
        # start ray casting angle shifted 30 degress left of player centrer FOV
        angle = self.angle - math.radians(30)
        fov = 60

        # Basically 60 degree FOV so 60 rays each shifted by 1 degree
        for ray in range(60):
            # variables predefined to prevent crashing
            isGrudge = False
            vDistObject = None
            hDistObject = None
           
            rayDist = 100000000

            # limiting angle between 0 and 2pi
            if angle < 0:
                angle += 2*math.pi
            elif angle > 2*math.pi:
                angle -= 2*math.pi

            # calculations for rays hitting horizontal walls

            # again initializing some variables
            hDist = 1000000000
            hX, hY = self.x, self.y
            rayDepth = 0

            if 0< angle < math.pi/2:

                rayAngle = math.pi/2 - angle
                rayY = (self.y // map.gridLength) * map.gridLength + map.gridLength
                rayX = math.tan(rayAngle)*(rayY-self.y) + self.x
                yOffset = map.gridLength
                xOffset = math.tan(rayAngle)*yOffset

            elif math.pi/2< angle < math.pi:
                rayAngle = angle - math.pi/2
                rayY = (self.y // map.gridLength) * map.gridLength + map.gridLength
                rayX = self.x - math.tan(rayAngle)* (rayY-self.y)
                yOffset = map.gridLength
                xOffset = -1* math.tan(rayAngle)*yOffset

            elif math.pi < angle < 3*math.pi/2:
                rayAngle = 3*math.pi/2 - angle
                rayY = (self.y // map.gridLength) * map.gridLength 
                rayX = self.x - math.tan(rayAngle)*(self.y -rayY) 
                yOffset = -1*map.gridLength
                xOffset = math.tan(rayAngle)*yOffset

            elif 3*math.pi/2 < angle < 2*math.pi:
                rayAngle = angle - 3*math.pi/2
                rayY = (self.y // map.gridLength) * map.gridLength 
                rayX = math.tan(rayAngle)*(self.y - rayY) + self.x 
                yOffset = -1*map.gridLength
                xOffset = -1*math.tan(rayAngle)*yOffset

            elif angle == 0 or angle == math.pi:
                rayX = self.x
                rayY = self.y
                rayDepth = rayExtension

            # rays extended in length each time until collision with wall
            while rayDepth < rayExtension:
                if angle > math.pi :
                    rayHCol = int(rayX /  map.gridLength)
                    rayHRow = int(rayY / map.gridLength) -1
                else: 
                    rayHCol = int(rayX /  map.gridLength)
                    rayHRow = int(rayY / map.gridLength)
                    
                if (0<=rayHRow<map.rows and 0<=rayHCol< map.cols 
                                and 6 >map.map[rayHRow][rayHCol] > 0):
                                hX = rayX
                                hY = rayY
                                hDist = distance(self.x, self.y, rayX,  rayY)
                                rayDepth = rayExtension   
                                
                                     
                else:
                    rayX += xOffset
                    rayY += yOffset
                    rayDepth += 1
            
            # calculations for rays hitting horizontal walls

            # again initializing some variables
            vDist = 1000000000
            vX, vY = self.x, self.y
            
            rayDepth = 0
            if 0< angle < math.pi/2:
                rayAngle = angle
                rayX = (self.x // map.gridLength) * map.gridLength + map.gridLength
                rayY = math.tan(rayAngle)*(rayX-self.x) + self.y
                xOffset = map.gridLength
                yOffset = math.tan(rayAngle)*xOffset

            elif math.pi/2< angle < math.pi:
                rayAngle = math.pi - angle 
                rayX = (self.x // map.gridLength) * map.gridLength 
                rayY =  math.tan(rayAngle)*(self.x-rayX) + self.y
                xOffset = -1*map.gridLength
                yOffset = -1*math.tan(rayAngle)*xOffset 

            elif math.pi < angle < 3*math.pi/2:

                rayAngle = angle - math.pi
                rayX = (self.x // map.gridLength) * map.gridLength 
                rayY = self.y - math.tan(rayAngle)*(self.x-rayX) 
                xOffset = -1*map.gridLength
                yOffset = math.tan(rayAngle)*xOffset

            elif 3*math.pi/2 < angle < 2*math.pi:

                rayAngle = 2*math.pi - angle 
                rayX = (self.x // map.gridLength) * map.gridLength + map.gridLength
                rayY = self.y - math.tan(rayAngle)*(rayX-self.x) 
                xOffset = map.gridLength
                yOffset = -1*math.tan(rayAngle)*xOffset
                
            elif  angle == math.pi/2 or angle == 3*math.pi/2: 
                  rayX = self.x
                  rayY = self.y
                  rayDepth = rayExtension
            
            # rays extended in length each time until collision with wall
            while rayDepth < rayExtension:
                if math.pi/2 <angle < 3*math.pi/2:
                    rayVCol = int(rayX /  map.gridLength)-1
                    rayVRow = int(rayY / map.gridLength) 
                else: 
                    rayVCol = int(rayX /  map.gridLength)
                    rayVRow = int(rayY / map.gridLength)
                    
                if (0<=rayVRow<map.rows and 0<=rayVCol< map.cols 
                                and 6>map.map[rayVRow][rayVCol] > 0):
                                vX = rayX
                                vY = rayY
                                vDist = distance(self.x, self.y, rayX, rayY)
                                rayDepth = rayExtension   
                                
                else:
                    rayX += xOffset
                    rayY += yOffset
                    rayDepth += 1
            
            # This part creates the illusion of shadows and texturing by darkening the
            # vertical walls a darker shade than horizontal walls
            # It also accounts for different cell types walls vs curtains
            # also grudge, cockroaches and the rings
            if vDist < hDist:
                rayDist = vDist
                rayRow = rayVRow
                rayCol = rayVCol
                if map.map[rayVRow][rayVCol] == 1:
                    wallColor = 'grey24'
                    lineColor = 'grey40'
                elif map.map[rayVRow][rayVCol] == 2:
                    wallColor = 'dark olive green'
                    lineColor = 'sky blue'
                elif map.map[rayVRow][rayVCol] == 3:
                    wallColor = 'goldenrod'
                    lineColor = 'light goldenrod'
                elif map.map[rayVRow][rayVCol] == 4:
                    wallColor = 'DarkOrange4'
                    lineColor = 'brown'
                elif map.map[rayVRow][rayVCol] == 5:
                    isGrudge = True
                    wallColor = 'black'
                    lineColor = 'black'

            elif hDist < vDist:
                rayX, rayY = hX, hY
                rayDist = hDist
                rayRow = rayHRow
                rayCol = rayHCol
                if map.map[rayHRow][rayHCol] == 1:
                    wallColor = 'grey33'
                    lineColor = 'grey40'
                elif map.map[rayHRow][rayHCol] == 2:
                    wallColor = 'DarkOliveGreen4'
                    lineColor = 'sky blue'
                elif map.map[rayHRow][rayHCol] == 3:
                    wallColor = 'gold'
                    lineColor = "light goldenrod"
                elif map.map[rayHRow][rayHCol] == 4:
                    wallColor = 'DarkOrange3'
                    lineColor = 'brown'
                   
                elif map.map[rayHRow][rayHCol] == 5:
                    isGrudge = True
                    wallColor = 'black'
                    lineColor = "black"

            # After all the raycasting this is the final code for creating the 3d world

            # correcting the angle for the primary purpose of fixing the fish-eye effect
            fixedAngle = self.angle - angle
            if fixedAngle < 0: fixedAngle += 2*math.pi
            elif fixedAngle > 2*math.pi: fixedAngle -= 2*math.pi

            #fish-eye effect would be caused if the rayDistance was left as is
            # hence perpendicular distance is calculated and hence corrected for 
            # minimum value to prevent crashing 
            rayDist = max(rayDist* math.cos(fixedAngle), 0.0001)

            # the presence of sets is to prevent multiple objects from spawning
            # same mechanic for all if a ray hits the object and its the centre ray
            # it adds its to the objects elements set and prevents further copies 
            # from spawning 
            # Inspired from Terry Feng's method citation: https://github.com/feng-terry/pacman3d/blob/master/rayCast.py
            # additionally they are then added to a dictionary which is important in the next step of spawning mainly cause fastttt
            if map.map[rayRow][rayCol] == 5 and (rayRow, rayCol) not in grudgeSet and ray==30:
                grudgeSet.add((rayRow, rayCol))
                objectsDict[rayDist] = objectsDict.get(rayDist, [])
                objectsDict[rayDist] += [map.grudgeTexture]
                distanceList.append(rayDist)
            
            elif map.map[rayRow][rayCol] == 3 and (rayRow, rayCol) not in ringSet and ray==30:
                ringSet.add((rayRow, rayCol))
                objectsDict[rayDist] = objectsDict.get(rayDist, [])
                objectsDict[rayDist] += [map.ringTexture]
                distanceList.append(rayDist)
            
            elif map.map[rayRow][rayCol] == 4 and (rayRow, rayCol) not in cockroachSet and ray==30:
                cockroachSet.add((rayRow, rayCol))
                objectsDict[rayDist] = objectsDict.get(rayDist, [])
                objectsDict[rayDist] += [map.roachTexture]
                distanceList.append(rayDist)
           

            # good old wall drawing parts
            # way this works is further away the ray is the smaller the wall
            # and vice versa and hence the rectangle and line are drawn with a smaller height
        
            lineHeight = min(1.5*map.gridLength*500 / rayDist, 2*800)

            lineOffset = 312.5 - lineHeight/2
            
            canvas.create_rectangle(ray*18,lineOffset,ray*18,lineHeight + lineOffset, width= 18, outline= wallColor)
            
            canvas.create_line(ray*18,lineOffset,ray*18,lineHeight + lineOffset, width= 1, fill= lineColor)

            # angle shifted for the next ray to be generated
            angle += math.radians(1)

       # drawing the objects
        self.drawObjects(map,canvas,objectsDict, distanceList)


    # draws the sprites basically and scales it in an appropriate way depending on
    # distance away from player
    # Inspired from Terry Feng's method: https://github.com/feng-terry/pacman3d/blob/master/rayCast.py
    def drawObjects(self,map,canvas,objectsDict, distanceList):
        # This is in case multiple objects are on screen to draw objects the correct distance away from the player
        distanceList.sort()
        distanceList.reverse()

        for objectDistance in distanceList:
            for gameObject in objectsDict[objectDistance]:
                texture = gameObject
                height = min(1.5*map.gridLength*500 / objectDistance, 2*800)
                offset = 312.5 - height
                dist = objectDistance
                # image scaling depending on in game distance away of object from player
                if dist > 275:
                    scale = 0.25

                elif dist>200:  
                   scale = 0.5
                elif dist>130:
                    scale = 0.75
                
                else:
                    scale=1

                texture = App.scaleImage(self,texture, 1*scale)
                
                canvas.create_image(1024/2, offset+height , image=ImageTk.PhotoImage(texture))




