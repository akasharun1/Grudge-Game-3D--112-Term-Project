from astar_v3 import *


# this is the code for the GameMap:
# It contains aspects of drawing the map in a 2d form as well as creating the map

# The map is dungeon styled and is created using the following steps:

# First a perfect maze is generated with no exits, this is via Prim's algorithm

# Prim's algorithm inspired from
# https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjJlMzAyNWYyNmI1OTVmOTZlYWM5MDdjYzJiOTQ3MTQyMmJjYWViOTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2MDY2NTg4ODEsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMDc2NzkxODg2OTU3Nzc5ODI4NCIsImVtYWlsIjoiYWthc2guYXJ1bjIxMDFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF6cCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsIm5hbWUiOiJBa2FzaCBBcnVuIiwicGljdHVyZSI6Imh0dHBzOi8vbGg1Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tNlFZNTNsQkVLWjQvQUFBQUFBQUFBQUkvQUFBQUFBQUFBQUEvQU1adXVjbXVkSlh3dEc1c193dkRyNlNJdUVTczM2WjFqQS9zOTYtYy9waG90by5qcGciLCJnaXZlbl9uYW1lIjoiQWthc2giLCJmYW1pbHlfbmFtZSI6IkFydW4iLCJpYXQiOjE2MDY2NTkxODEsImV4cCI6MTYwNjY2Mjc4MSwianRpIjoiMWNiMTNlNDBmZGI5NmY2OTlmYmVjNmFiMDQxYTI1ZGVlMmU3OTQzNyJ9.l2HWvJBR3ewDeUKydefLwnsItvObc98vgHBwLJJc7Os8-58yceYpP1vcYMMWalXm3607bqgch2CSsK4mfN69W5yoFQhdkoqBXA4dHJXFESVT8WLqHJLmFmjyzyZgDJaOuR5geJWZCS3pvUKEgzip6NhiGWO59nNNZZe7Vy-72gW0GMjKfzYArV7eIGsd5TSskfDPznkUoWl7bYnM-q2_S2DPvI1SlVAxTqPAPfsL7brlHDbWVB9WwCC3ORnaFsxjC5Elye-B-VnbvuTcZzztb2VmCN_qMaffPoEzfGBgY2_rotRJWz9eftqUf7-J3oSvQ59eu4E6Zi3uA9K-WAk2XA

# Then I increase the sparseness of the maze by a certain defined amount, which 
# dissolves some dead ends. After this I make the remaining dissolve the walls of 
# remaining dead ends to create loops. The maze is now imperfect

# Finally I add rooms of 4x4 after certain cell intervals to create a dungeon effect
# In these rooms I make the centre's into a celly type I like to call the curtain/ hiding spot type
# I personally like calling it a curtain as because of
# how raycasting works once in the curtain cell you can still see outside the curtain cell 
# and you can pass through it 

# the general idea of how to create the dungeonified maze comes from 
# http://www.brainycode.com/downloads/RandomDungeonGenerator.pdf

# I haven't followed it to a T, espescially regarding the random generation 
# of rooms cause I realised it wasn't necessary for my purposes to follow the 
# randomize room generation to that extent

# okie so now the good parts
# I made the grudge pathfinding AI and the algo is in astar_v2.py as well as the inspiration
# it works very well, almost too well which is why I needed to handicap it with the spawn intervals
# and move intervals in main

# I also spawn a set number of rings(not paintings now though a change is literally one png image away!)
# they are spawned randomly and spread out
# also i spawn a cockroach around the room w the hiding spot
# and made this cockroach move function which makes it move across its perimeter 
# every timerFired in the main game
# this actually ups the game difficulty to a good level cause the cockroaches slice your health 
# bar 10 hp at a time :()


import random

class GameMap():

    def __init__(self, rows, cols, gridLength, sparseness, numRooms, rings, grudgeTexture , ringTexture, cockroachTexture):
        self.rows = rows
        self.cols = cols
        self.gridLength = gridLength
        self.map = []
        self.sparseness = sparseness
        self.numRooms = numRooms
        self.startRings = rings
        self.grudgeRow = 0
        self.grudgeCol = 0
        self.cockroachPosList = []
        # these are already cited in the main code 
        self.grudgeTexture = grudgeTexture  
        self.ringTexture = ringTexture
        self.roachTexture = cockroachTexture


    def generate_map(self, generatorStartRow, generatorStartCol):

        # Prims algorithm: inspired from https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjJlMzAyNWYyNmI1OTVmOTZlYWM5MDdjYzJiOTQ3MTQyMmJjYWViOTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2MDY2NTg4ODEsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMDc2NzkxODg2OTU3Nzc5ODI4NCIsImVtYWlsIjoiYWthc2guYXJ1bjIxMDFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF6cCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsIm5hbWUiOiJBa2FzaCBBcnVuIiwicGljdHVyZSI6Imh0dHBzOi8vbGg1Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tNlFZNTNsQkVLWjQvQUFBQUFBQUFBQUkvQUFBQUFBQUFBQUEvQU1adXVjbXVkSlh3dEc1c193dkRyNlNJdUVTczM2WjFqQS9zOTYtYy9waG90by5qcGciLCJnaXZlbl9uYW1lIjoiQWthc2giLCJmYW1pbHlfbmFtZSI6IkFydW4iLCJpYXQiOjE2MDY2NTkxODEsImV4cCI6MTYwNjY2Mjc4MSwianRpIjoiMWNiMTNlNDBmZGI5NmY2OTlmYmVjNmFiMDQxYTI1ZGVlMmU3OTQzNyJ9.l2HWvJBR3ewDeUKydefLwnsItvObc98vgHBwLJJc7Os8-58yceYpP1vcYMMWalXm3607bqgch2CSsK4mfN69W5yoFQhdkoqBXA4dHJXFESVT8WLqHJLmFmjyzyZgDJaOuR5geJWZCS3pvUKEgzip6NhiGWO59nNNZZe7Vy-72gW0GMjKfzYArV7eIGsd5TSskfDPznkUoWl7bYnM-q2_S2DPvI1SlVAxTqPAPfsL7brlHDbWVB9WwCC3ORnaFsxjC5Elye-B-VnbvuTcZzztb2VmCN_qMaffPoEzfGBgY2_rotRJWz9eftqUf7-J3oSvQ59eu4E6Zi3uA9K-WAk2XA

        maze_numRows = self.rows
        maze_numCols = self.cols

        maze_seed = [[1]*maze_numRows for i in range(maze_numCols)]
        maze_generatorStartRow = generatorStartRow
        maze_generatorStartCol = generatorStartCol

        maze_seed[maze_generatorStartRow][maze_generatorStartCol] = 0

        toSearchList = []

        for dRow in [-1,0,1]:
            for dCol in [-1,0,1]:
                if abs(dRow) != abs(dCol):
                    toSearchList.append([maze_generatorStartRow+dRow,maze_generatorStartCol+dCol])

        while len(toSearchList) != 0:
            
            searchPoint = toSearchList[random.randint(0,len(toSearchList)-1)]
            for dRow in [-1,0,1]:
                for dCol in [-1,0,1]:
                    if abs(dRow) != abs(dCol):

                        if (searchPoint[0] != 0 and searchPoint[0] != maze_numRows-1 
                            and searchPoint[1] != 0 and searchPoint[1] != maze_numCols-1):
                        

                            if (maze_seed[searchPoint[0]+dRow][searchPoint[1]+dCol] == 1 
                                and maze_seed[searchPoint[0]-dRow][searchPoint[1]-dCol] == 0):

                                surroundingPassageCount = 0

                                for dRow in [-1,0,1]:
                                    for dCol in [-1,0,1]:
                                        if abs(dRow) != abs(dCol):
                                            if maze_seed[searchPoint[0]+dRow][searchPoint[1]+dCol] == 0:
                                                surroundingPassageCount += 1
                                
                                if surroundingPassageCount < 2:
                                    maze_seed[searchPoint[0]][searchPoint[1]] = 0

                                    for dRow in [-1,0,1]:
                                        for dCol in [-1,0,1]:
                                            if abs(dRow) != abs(dCol):
                                                if [searchPoint[0]+dRow, searchPoint[1]+dCol] not in toSearchList:
                                                    toSearchList.append([searchPoint[0]+dRow, searchPoint[1]+dCol])
            toSearchList.remove(searchPoint)
        

                
        
        # Sparsifying the maze 
        while self.sparseness > 1:

            for row in range(len(maze_seed)):
                for col in range(len(maze_seed[0])):
                    if row > 0 and col > 0 and row < len(maze_seed)-1 and col < len(maze_seed[0])-1 and maze_seed[row][col]==0:
                        surroundingPassageCount = 0

                        for dRow in [-1,0,1]:
                            for dCol in [-1,0,1]:
                                if abs(dRow) != abs(dCol):
                                    if maze_seed[row+dRow][col+dCol] == 0:
                                        surroundingPassageCount += 1

                        if surroundingPassageCount == 1:
                            maze_seed[row][col] = 1

            self.sparseness -= 1

        # Making loops and removing some dead ends

        for row in range(len(maze_seed)):
            for col in range(len(maze_seed[0])):
                if row > 0 and col > 0 and row < len(maze_seed)-1 and col < len(maze_seed[0])-1 and maze_seed[row][col]==0:
                    surroundingPassageCount = 0

                    for dRow in [-1,0,1]:
                        for dCol in [-1,0,1]:
                            if abs(dRow) != abs(dCol):
                                if maze_seed[row+dRow][col+dCol] == 0:
                                    surroundingPassageCount += 1

                    if surroundingPassageCount == 1:
                                        
                        toSearchList = []

                        for dRow in [-1,0,1]:
                            for dCol in [-1,0,1]:
                                if abs(dRow) != abs(dCol):
                                    toSearchList.append([row+dRow,col+dCol])

                        while surroundingPassageCount <1:
                                            
                            searchPoint = toSearchList[random.randint(0,len(toSearchList)-1)]
                            for dRow in [-1,0,1]:
                                for dCol in [-1,0,1]:
                                    if abs(dRow) != abs(dCol):

                                        if (searchPoint[0] != 0 and searchPoint[0] != maze_numRows-1 
                                            and searchPoint[1] != 0 and searchPoint[1] != maze_numCols-1):
                                        

                                            if (maze_seed[searchPoint[0]+dRow][searchPoint[1]+dCol] == 1 
                                                and maze_seed[searchPoint[0]-dRow][searchPoint[1]-dCol] == 0):

                                                surroundingPassageCount = 0

                                                for dRow in [-1,0,1]:
                                                    for dCol in [-1,0,1]:
                                                        if abs(dRow) != abs(dCol):
                                                            if maze_seed[searchPoint[0]+dRow][searchPoint[1]+dCol] == 0:
                                                                surroundingPassageCount += 1
                                                
                                                if surroundingPassageCount < 2:
                                                    maze_seed[searchPoint[0]][searchPoint[1]] = 0

                                                    for dRow in [-1,0,1]:
                                                        for dCol in [-1,0,1]:
                                                            if abs(dRow) != abs(dCol):
                                                                if [searchPoint[0]+dRow, searchPoint[1]+dCol] not in toSearchList:
                                                                    toSearchList.append([searchPoint[0]+dRow, searchPoint[1]+dCol])

        # making large rooms 
        # hiding spaces/ curtains are added into the centre of the room and 
        # represented with a different color
        # additionally spawning cockroaches at their start points
        while self.numRooms > 1:

            count = 0
            for row in range(len(maze_seed)):
                for col in range(len(maze_seed[0])):
                    if row > 0 and col > 0 and row < len(maze_seed)-1 and col < len(maze_seed[0])-1 and maze_seed[row][col]==0:
                        count += 1
                        if count > 64:
                            if row + 4 < len(maze_seed)-1 and col + 4 < len(maze_seed[0])-1:
                                startRow = row
                                startCol = col
                                self.cockroachPosList.append((startRow,startCol))
                                
                                for row1 in range(startRow, startRow+4):
                                    for col1 in range(startCol, startCol + 4):
                                        row_differential = startRow+4 - row1
                                        col_differential = startCol+4 - col1
                                        
                                        if 1<row_differential<4 and 1<col_differential<4:
                                            maze_seed[row1][col1] = 2
                                        elif row1 == startRow and col1 == startCol:
                                            # spawning cockroach
                                            maze_seed[row1][col1] = 4
                                        else:
                                            maze_seed[row1][col1] = 0
                                        count = 0
                                        self.numRooms -= 1
       

        # spawning rings
        while self.startRings > 1:
            count = 0
            for row in range(len(maze_seed)):
                for col in range(len(maze_seed[0])):
                    if row > 0 and col > 0 and row < len(maze_seed)-1 and col < len(maze_seed[0])-1 and maze_seed[row][col]==0:
                        count += 1
                        if count > 50:
                            maze_seed[row][col] = 3
                            self.startRings -= 1
                            count = 0

        self.map = maze_seed

    # potentially draw map in case I want to create a birds eye view
    def drawMap(self, canvas):
        
        for row in range(self.rows):
            for col in range(self.cols):
                if self.map[row][col] > 0: color = 'white'
                else: color = "black"
                x0 = col*self.gridLength
                y0 = row*self.gridLength
                
                # the magic no. 1 is basically for the width of grid lines
                canvas.create_polygon(x0+1, y0+1,x0+1, self.gridLength + y0 -1 \
                ,self.gridLength+x0-1, self.gridLength+y0-1, \
                self.gridLength+x0-1, y0+1, fill = color)

    # this function spawns grudge at a point in the map
    # if and only if grudge has a path to the player
    # and grudge is being spawned atleast 17 blocks away from the player
    # this is to ensure grudge doesnt insta kill the player and also 
    # that somehow an anamolous dead end doesn't permanantly trap grudge
    def spawnGrudge(self, playerStartPos):
        maze_numRows = self.rows
        maze_numCols = self.cols
        grudgeStartRow = random.randint(1, maze_numRows-2)
        grudgeStartCol = random.randint(1, maze_numCols-2)


        path = aStarList(self.map, (grudgeStartRow,grudgeStartCol), playerStartPos)

        
        while ((grudgeStartRow-playerStartPos[0])**2 + (grudgeStartCol-playerStartPos[1])**2)**0.5 <=17 or path == None:
            grudgeStartRow = random.randint(1, maze_numRows-2)
            grudgeStartCol = random.randint(1, maze_numCols-2)
            path = aStarList(self.map, (grudgeStartRow,grudgeStartCol), playerStartPos)
           
        self.grudgeRow = grudgeStartRow
        self.grudgeCol = grudgeStartCol

        self.map[grudgeStartRow][grudgeStartCol] = 5
        
    # Both this and spawn use a star pathfinding the work
    # it finds the list of movements from the algorithim
    # and performs the first one
    def grudgeMove(self, playerPos):
        playerRow, playerCol = playerPos
        if self.grudgeRow != playerRow and self.grudgeCol != playerCol:
            path = aStarList(self.map, (self.grudgeRow, self.grudgeCol), playerPos)
            if path != None:
                grudgeRow, grudgeCol = path[0]
                if self.map[grudgeRow][grudgeCol] != 2:
                    self.map[self.grudgeRow][self.grudgeCol] = 0
                    
                    self.map[grudgeRow][grudgeCol] = 5
                    self.grudgeRow, self.grudgeCol = grudgeRow, grudgeCol
        
    # despawns the grudge an essential mechanic
    def grudgeDespawn(self):
        self.map[self.grudgeRow][self.grudgeCol] = 0

    # cockroach moves on part of its cycle around the curtains
    def cockroachesMove(self):
        for row, col in self.cockroachPosList:
            self.map[row][col] = 0
            if self.map[row +1][col + 1] == 2 or self.map[row][col+1] == 2:
                newRow = row+1
                newCol = col
            elif self.map[row -1][col + 1] == 2 or self.map[row-1][col] ==2:
                newRow = row
                newCol = col+1
            elif self.map[row -1][col - 1] == 2 or self.map[row][col-1] ==2:
                newRow = row-1
                newCol = col
            else:
                newRow = row
                newCol = col-1
            self.map[newRow][newCol] = 4
            self.cockroachPosList.remove((row, col))
            self.cockroachPosList.append((newRow, newCol))

            







        
        








        



        

