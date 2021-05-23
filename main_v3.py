# pygame is from: https://www.pygame.org/wiki/GettingStarted
import pygame
# from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html 
# big thanks!
from cmu_112_graphics import *
from grudgeGameDatabase import *
import math
import time
import random
from maze_generation_v3 import *
from player_raycaster_v3_untextured import *

# You need Hannya.wav to run this
# Hannya is 40 MB so I have sent it externally, too big for autolab :()

# sound credits: Hannya.wav https://www.youtube.com/watch?v=BZD9ZBQxusw&ab_channel=Kraosando
# for their really nice and atmospheric music, Implemented as general bgm

# also the grudge death rattle sound clip credits is to: https://www.youtube.com/watch?v=-0v24Af1KhU&ab_channel=GhostlyHighway 

# this is the heart of the game where most of the work happens

# mainly initializing audio, sprite textures, background textures, ui, and the 
# modifiable aspects of the game such as the no. of rooms created in the maze etc

class GrudgeGame(App):

    def appStarted(self):
        self.userName = 'Guest'
        pygame.mixer.init()
        self.gameStarted = False
        self.bgmVol = 0.6
        self.grudgeVol = 0

        self.grudgeChannel = pygame.mixer.Channel(1)
        self.bgmChannel = pygame.mixer.Channel(0) 
        self.grudgeChannel.set_volume(self.grudgeVol)
        self.bgmChannel.set_volume(self.bgmVol)
        self.grudgeChannel.play(pygame.mixer.Sound('grudge_sound.wav'),-1)
        self.bgmChannel.play(pygame.mixer.Sound('Hannya.wav'),-1)
        self.isPaused = False


        # general game initializes change for a different experience
        # may be used for varying difficult levels down the line

        self.mapRows = 32
        self.mapCols = 32
        self.gridLength = 100
        self.sparseness = 2
        self.numRooms = 4
       
        self.startRings = 12
        self.totalRings = 7
        self.difficulty = "Medium"
        
        # credits for grudge background image : https://www.google.com/url?sa=i&url=https%3A%2F%2Fhipwallpaper.com%2Fthe-grudge-desktop-backgrounds%2F&psig=AOvVaw3T_cZosjx8vwXled8Av8j3&ust=1607280213351000&source=images&cd=vfe&ved=0CA0QjhxqFwoTCNCU4cO_t-0CFQAAAAAdAAAAABAD
        self.background = self.loadImage('grudgeBackground.jpg')
        # credits for the you died image : https://www.google.com/url?sa=i&url=https%3A%2F%2Fbloody-disgusting.com%2Fmovie%2F3599114%2Fgrudge-sequels-explore-time-periods-exclusive%2F&psig=AOvVaw2p-EevFtHfCaAnrM0u49w6&ust=1607280188211000&source=images&cd=vfe&ved=0CAMQjB1qFwoTCNjPkum_t-0CFQAAAAAdAAAAABAJ
        self.deadImage = self.loadImage('yourDead.jpg')
        self.deadImage = self.scaleImage(self.deadImage, 0.85)
        # credits cute puppy you win image: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.wallpaperflare.com%2Fthree-puppies-basket-dogs-pets-canine-domestic-domestic-animals-wallpaper-smqps&psig=AOvVaw3OHD-aUr66qabqjVohaQau&ust=1607280752429000&source=images&cd=vfe&ved=0CAMQjB1qFwoTCMD8p8rBt-0CFQAAAAAdAAAAABAD
        self.winImage = self.loadImage('youWin.jpg')
        self.grudgeisSpawned = False


        self.gameOver = False
        self.youWin = False
        self.showLeaderBoard = False
        self.helpScreen = False
        


    # some more initializations necessary in case player chooses to restart game
    def grudgeGameStartSettings(self):
        # Different starting settings depending on difficulty
        # Easy requires only 4 rings to win and grudge spawn and move interval decrease
        if self.difficulty == "Medium":
            self.mapRows = 32
            self.mapCols = 32
            self.gridLength = 100
            self.sparseness = 2
            self.numRooms = 4
        
            self.startRings = 12
            self.totalRings = 7
            self.playerRings = 0
            self.health = 100
                
            # grudge starting spawn intervals which will change as game progresses

            self.grudgeSpawnInterval = 70

            # grudge moves on step in this interval which changes as player collects rings
            self.grudgeMoveInterval = 35
        elif self.difficulty == "Easy":
            self.mapRows = 32
            self.mapCols = 32
            self.gridLength = 100
            # Increased sparsenenss 
            self.sparseness = 3
            # More rooms
            self.numRooms = 6

            #Increased number of rings
            #Less rings to win
            self.startRings = 20
            self.totalRings = 4
            self.playerRings = 0
            self.health = 100
                
            # grudge starting spawn intervals which will change as game progresses

            self.grudgeSpawnInterval = 70

            # grudge moves on step in this interval which changes as player collects rings
            self.grudgeMoveInterval = 35
        elif self.difficulty == "Hard":
            self.mapRows = 32
            self.mapCols = 32
            self.gridLength = 100
            # Decreased sparseness
            self.sparseness = 1
            # slightly less rooms
            self.numRooms = 3
        
            self.startRings = 12
            # need to collect more rings to win
            self.totalRings = 10
            self.playerRings = 0
            self.health = 100
                
            # grudge starting spawn intervals which will change as game progresses

            self.grudgeSpawnInterval = 30

            # grudge moves on step in this interval which changes as player collects rings
            self.grudgeMoveInterval = 20

        self.helpScreen = False
        self.youWin = False
        self.showLeaderBoard = False

        self.playerAngle = math.pi/4
        self.playerdx =  math.cos(self.playerAngle) * 5
        self.playerdy = math.sin(self.playerAngle) * 5

        # Grudge sprite Image creds: 
        # https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vippng.com%2Fmaxp%2FhiRRomb%2F&psig=AOvVaw0pBS2Eh_4m-69bEIM96QN2&ust=1607280931144000&source=images&cd=vfe&ved=0CAMQjB1qFwoTCOjk-prCt-0CFQAAAAAdAAAAABAD
        self.grudgeTexture = self.loadImage('grudgechara.png')
        # ring Image creds:
        # http://pixelartmaker.com/art/5bbab14010c0068
        self.ringTexture = self.loadImage('ring.png')
        # roach Image creds:
        # https://www.clipartmax.com/middle/m2H7N4A0Z5b1m2G6_this-high-quality-free-png-image-without-any-background-cockroach-png/
        self.cockroachTexture = self.loadImage('roach.png')

        # initializing and generating game map
        self.gameMap = GameMap(self.mapRows, self.mapCols, self.gridLength, self.sparseness, self.numRooms, self.startRings, self.grudgeTexture, self.ringTexture, self.cockroachTexture)
        map_generatorStartRow = random.randint(1, self.mapRows-2)
        map_generatorStartCol = random.randint(1, self.mapCols-2)
        self.gameMap.generate_map(map_generatorStartRow,map_generatorStartCol)

        self.playerX = map_generatorStartCol*self.gridLength+ 50
        self.playerY = map_generatorStartRow*self.gridLength+ 50


        # grudge is spawned on map and  rest of stuff initialized
        self.gameMap.spawnGrudge((map_generatorStartRow ,map_generatorStartCol))
        self.grudgeisMoving = False
        self.gameOver = False
        self.grudgeisSpawned = True

        # audio set to og state w no grudge music
        self.bgmVol = 0.6
        self.grudgeVol = 0
        
        
        # game start Time
        self.startTime = time.time()
        
        self.grudgeChannel.set_volume(self.grudgeVol)
        self.bgmChannel.set_volume(self.bgmVol)
        

        self.grudgeChannel.play(pygame.mixer.Sound('grudge_sound.wav'),-1)
        self.bgmChannel.play(pygame.mixer.Sound('Hannya.wav'),-1)
        self.isPaused = False


    # this is the logic part where the game checks whether the player is inside
    # either a ring block a grudge block or a cockroach block
    # ring block increases your ring count
    # grudge block results in instant death
    # cockroach block results in -10 health
    # gameOver state is reached when grudge catches the player or when their
    # health is depleted to below 0

    # as the ring count increases the grudge respawn rate as well as movement rate
    # increases giving the impression of a speed up

    # if you collect 7 rings congratsss you win!!!


    # also there is the fun bit which computes if the block distance between 
    # grudge and the player is less than 7 blocks, if true the background sound 
    # is set to 0 and the grudge death rattle is progressively increased as
    # grudge reaches the player

    # the original sound settings are reset if player is at a block distance of
    # more than 7 blocks or grudge despawns

    def gameStateCheck(self):
        playerCol = int((self.playerX )/  self.gridLength)
        playerRow = int((self.playerY ) / self.gridLength)
        if self.grudgeisMoving:
            self.gameMap.grudgeMove((playerRow,playerCol))
            grudgeRow = self.gameMap.grudgeRow
            grudgeCol = self.gameMap.grudgeCol
            grudgeDistance = ((grudgeRow-playerRow)**2 + (grudgeCol-playerCol)**2)**0.5
            if 0<grudgeDistance < 7 and self.grudgeisMoving:
                self.grudgeVol = 1/grudgeDistance
                self.bgmVol = 0
            else:
                self.grudgeVol = 0
                self.bgmVol = 0.6

            self.grudgeChannel.set_volume(self.grudgeVol)
            self.bgmChannel.set_volume(self.bgmVol)


        if self.gameMap.map[playerRow][playerCol] == 3:
            self.playerRings += 1
            self.gameMap.map[playerRow][playerCol] = 0
            # Differing game state adjustments depending on difficulty
            if self.difficulty == "Medium":
                if self.grudgeSpawnInterval < 20:
                    self.grudgeSpawnInterval = 15
                else:
                    self.grudgeSpawnInterval -= 10
                if self.grudgeMoveInterval < 5:
                    self.grudgeMoveInterval -= 4
                else:
                    self.grudgeMoveInterval -= 5
            elif self.difficulty == "Easy":
                if self.grudgeSpawnInterval < 20:
                    self.grudgeSpawnInterval = 15
                else:
                    self.grudgeSpawnInterval -= 7
                self.grudgeMoveInterval -= 5
            elif self.difficulty == "Hard":
                if self.grudgeSpawnInterval < 20:
                    self.grudgeSpawnInterval = 15
                else:
                    self.grudgeSpawnInterval -= 7
                if self.grudgeMoveInterval < 5:
                    self.grudgeMoveInterval = 1
                else:
                    self.grudgeMoveInterval -= 6


        if self.gameMap.map[playerRow][playerCol] == 4:
            self.health -= 20
        if self.playerRings == self.totalRings:
            self.youWin = True

        if self.gameMap.map[playerRow][playerCol] == 5 or self.health == 0:
            self.gameOver = True

 
 # when game over the audio is either set to ominous grudge noises
 # victory is just silence (for now.... maybe)
 # cockroaches move around their perimeter continuously every timerFired interval
 
    def timerFired(self):
        if self.gameOver:
            self.grudgeChannel.set_volume(7)
            self.bgmChannel.set_volume(0)
            updateTable(self.userName, self.playerRings)
        
        if self.youWin:
            self.grudgeChannel.set_volume(0)
            self.bgmChannel.set_volume(0)
            updateTable(self.userName, self.playerRings)
        
        # cockroaches move around their perimeter continuously every timerFired interval
        # also here is the code causing the despawn and spawning as well as motion or pausing
        # of grudge :
 
        if not self.isPaused and self.gameStarted and not self.gameOver and not self.youWin:
            currentTime = time.time()
            self.gameMap.cockroachesMove()
            if round(currentTime - self.startTime)%self.grudgeSpawnInterval == 0 and round(currentTime - self.startTime)>0:
                self.grudgeChannel.set_volume(0)
                self.bgmChannel.set_volume(0.6)
                if self.grudgeisSpawned:
                    self.grudgeisMoving = False
                    self.gameMap.grudgeDespawn()
                    self.grudgeisSpawned = False
                else:       
                    playerCol = int((self.playerX )/  self.gridLength)
                    playerRow = int((self.playerY ) / self.gridLength)
                    self.gameMap.spawnGrudge((playerRow ,playerCol))
                    self.grudgeisSpawned = True
            if self.grudgeisSpawned:
                if round(currentTime - self.startTime)%self.grudgeMoveInterval == 0  and round(currentTime - self.startTime)>0:
                    self.grudgeisMoving = not self.grudgeisMoving
            else:
                self.grudgeisMoving = False
            # the regular gameStateCheck
            self.gameStateCheck()
            
    # as of rn basically to click the button to start the game or click the
    # button to restart the game

    def mousePressed(self, event):
        # For the play/ replay buttons
        # When clicking the play button it gets user input about username
        if (event.x >= 1024//2 - 150 and event.x <= 1024//2+ 100 
            and event.y >= 768//2 + 80 and event.y <= 768//2+ 180) and not self.showLeaderBoard and (self.youWin or self.gameOver or not self.gameStarted):
            if not self.gameStarted:
                self.userName = self.getUserInput("What is your username?")
            if self.grudgeisSpawned:
                self.gameMap.grudgeDespawn()
            self.grudgeGameStartSettings()
            self.grudgeisMoving = False
            self.startTime = time.time()
            self.gameStarted = True

        # Button for showing leaderboard
        if (event.x >= 1024//2 - 195 and event.x <= 1024//2+ 153 
            and event.y >= 768//2- 80 and event.y <= 768//2+ 20) and (self.gameOver or not self.gameStarted or self.youWin):
            self.showLeaderBoard = True

        # Button for exiting leaderboard screen
        if (event.x >= 900 and event.x <= 1000
            and event.y >= 25 and event.y <= 85) and self.showLeaderBoard:
            self.showLeaderBoard = False
        
        # Difficulty selection at start 
        if (event.x >= 1024//2- 195 and event.y >=768//2 + 240  
            and event.x <=1024//2+ 153 and event.y <= 768//2+ 340 and not self.gameStarted):
            difficulties = ['Easy', 'Medium', 'Hard']
            self.difficulty = self.getUserInput("Select Difficulty: Easy, Medium, Hard")
            if self.difficulty not in difficulties:
                self.difficulty = 'Medium'


    def keyPressed(self, event):
        # if you press a and d the player rotates giving the impression of turning
        # ones head in 2d; idea from: 3d sage's explanation in C : https://www.youtube.com/watch?v=gYRrGTC7GtA&t=423s
        # if you press w or s you move the player moves forward or backward in that direction
        if not self.isPaused and not self.gameOver and not self.youWin and self.gameStarted:
            if event.key == "a": 
                self.playerAngle -= 0.2
                if  self.playerAngle < 0:
                    self.playerAngle += math.pi*2
            elif event.key == "d": 
                self.playerAngle += 0.2
                if  self.playerAngle > 2*math.pi:
                    self.playerAngle -= math.pi*2
            # Using Vector Rotation the position change due to rotation is computed
            # using the change in the player's angle
            self.playerdx = math.cos(self.playerAngle) * 5
            self.playerdy = math.sin(self.playerAngle) * 5
            
            # checks in place to prevent player from passing through walls
            # can still pass through game objects like cockroaches, rings, grudge
            # etc
            if event.key == "w":  
                self.playerY += self.playerdy
                self.playerX += self.playerdx
                playerCol = int((self.playerX )/  self.gridLength)
                playerRow = int((self.playerY ) / self.gridLength)
                

                if self.gameMap.map[playerRow][playerCol] == 1:
                    self.playerY -= self.playerdy 
                    self.playerX -= self.playerdx 
                    
            elif event.key == "s": 
                self.playerY -= self.playerdy
                self.playerX -= self.playerdx
             
            playerCol = int((self.playerX )/  self.gridLength) 
            playerRow = int((self.playerY ) / self.gridLength) 


            if self.gameMap.map[playerRow][playerCol] == 1:
                self.playerY += self.playerdy
                self.playerX += self.playerdx
        
           
        # To pause the game
        if event.key == 'p':
            if self.isPaused:
                pygame.mixer.unpause()
                self.isPaused = not self.isPaused 
            else:
                pygame.mixer.pause()
                self.isPaused = not self.isPaused 

        # Hack/ cheat to go to the you Win page
        if event.key == 'o':
            self.youWin = True
        
        if event.key == 'h':
            self.helpScreen = not self.helpScreen

   
    def redrawAll(self, canvas):
        # draws user help screen with rules and guidance on how to play
        if self.helpScreen:
            canvas.create_rectangle(0,0, self.width, self.height, fill = "black")
            canvas.create_text(1024//2, 100, font = "fixedsys 70 bold underline", text= f'''Rules:''', fill= "Red")
            canvas.create_text(500, 250, font = "fixedsys 20 bold", text= f'''1. Collect rings to escape! 4 for easy, 7 for medium,\n   9 for hard.''', fill= "Red")
            canvas.create_text(500, 350, font = "fixedsys 20 bold", text= f'''2. Toggle Difficulty at game start screen; \n   Difficulty changes map design and Grudge's behaviour.''', fill= "Red")
            canvas.create_text(500, 450, font = "fixedsys 20 bold", text= f'''3. Getting hit by a cockroach makes you lose 10 hp.''', fill= "Red")
            canvas.create_text(500, 550, font = "fixedsys 20 bold", text= f'''4. If Sadako catches you or your health drops below 10,\n   You die!''', fill= "Red")
            canvas.create_text(500, 650, font = "fixedsys 20 bold", text= f'''5. Use green curtain hiding spots to hide from Sadako. \n   She can't catch you there!''', fill= "Red")
        # draws Leaderboard screen
        # Consisting of leaderboard as well as exit button
        # Leaderboard shows names of top 5 scorers 
        # Each name can only be used once and the leaderboard stores only each player's highest
        # score and only updates if a new player got a high enough score or a present player on the leaderboard
        # beat their old score.
        elif self.showLeaderBoard:
            canvas.create_rectangle(0,0, self.width, self.height, fill = "black")
            canvas.create_text(1024//2, 100, font = "fixedsys 70 bold underline", text= f'''Leaderboard:''', fill= "Red")
            leaderBoardList = getLeaderboard()
            canvas.create_rectangle(900,25,1000, 85, fill = "IndianRed4")
            canvas.create_rectangle(905,30,995, 80, fill= "red", outline="IndianRed4")
            
            canvas.create_text(950, 55, font = "fixedsys 15 bold", text = "Back", fill= "indigo")
            if len(leaderBoardList) == 1:
                canvas.create_text(500, 250, font = "fixedsys 40 bold", text= f'''1. {leaderBoardList[0][0]}    Score: {leaderBoardList[0][1]}''', fill= "Yellow")
            elif len(leaderBoardList) == 2:
                canvas.create_text(500, 250, font = "fixedsys 40 bold", text= f'''1. {leaderBoardList[0][0]}    Score: {leaderBoardList[0][1]}''', fill= "Yellow")
                canvas.create_text(500, 350, font = "fixedsys 40 bold", text= f'''2. {leaderBoardList[1][0]}    Score: {leaderBoardList[1][1]}''', fill= "Blue")
            elif len(leaderBoardList) == 3:
                canvas.create_text(500, 250, font = "fixedsys 40 bold", text= f'''1. {leaderBoardList[0][0]}    Score: {leaderBoardList[0][1]}''', fill= "Yellow")
                canvas.create_text(500, 350, font = "fixedsys 40 bold", text= f'''2. {leaderBoardList[1][0]}    Score: {leaderBoardList[1][1]}''', fill= "Blue")
                canvas.create_text(500, 450, font = "fixedsys 40 bold", text= f'''3. {leaderBoardList[2][0]}    Score: {leaderBoardList[2][1]}''', fill= "Orange")
            elif len(leaderBoardList) == 4:
                canvas.create_text(500, 250, font = "fixedsys 40 bold", text= f'''1. {leaderBoardList[0][0]}    Score: {leaderBoardList[0][1]}''', fill= "Yellow")
                canvas.create_text(500, 350, font = "fixedsys 40 bold", text= f'''2. {leaderBoardList[1][0]}    Score: {leaderBoardList[1][1]}''', fill= "Blue")
                canvas.create_text(500, 450, font = "fixedsys 40 bold", text= f'''3. {leaderBoardList[2][0]}    Score: {leaderBoardList[2][1]}''', fill= "Orange")
                canvas.create_text(500, 550, font = "fixedsys 40 bold", text= f'''4. {leaderBoardList[3][0]}    Score: {leaderBoardList[3][1]}''', fill= "Green")
            else:
                canvas.create_text(500, 250, font = "fixedsys 40 bold", text= f'''1. {leaderBoardList[0][0]}    Score: {leaderBoardList[0][1]}''', fill= "Yellow")
                canvas.create_text(500, 350, font = "fixedsys 40 bold", text= f'''2. {leaderBoardList[1][0]}    Score: {leaderBoardList[1][1]}''', fill= "Blue")
                canvas.create_text(500, 450, font = "fixedsys 40 bold", text= f'''3. {leaderBoardList[2][0]}    Score: {leaderBoardList[2][1]}''', fill= "Orange")
                canvas.create_text(500, 550, font = "fixedsys 40 bold", text= f'''4. {leaderBoardList[3][0]}    Score: {leaderBoardList[3][1]}''', fill= "Green")
                canvas.create_text(500, 650, font = "fixedsys 40 bold", text= f'''5. {leaderBoardList[4][0]}    Score: {leaderBoardList[4][1]}''', fill= "White")


        # draws game Over UI splash screen
        # lots of magic number :(
        # replay and leaderboard button pressent
        elif self.gameOver:
            canvas.create_rectangle(0,0, self.width, self.height, fill = "black")
            canvas.create_image(1024//2+300, 768//2, image=ImageTk.PhotoImage(self.deadImage))
            canvas.create_text(1024//2, 768//2-200, font = "fixedsys 50 bold", text= f'''You Died!\nScore: {self.playerRings}''', fill= "Red")

            canvas.create_rectangle(1024//2- 195, 768//2- 80, 1024//2+ 153, 768//2+ 20, fill= "IndianRed4" )
            canvas.create_rectangle(1024//2- 190, 768//2- 75, 1024//2+ 148, 768//2+ 15, fill= "red", outline="IndianRed4" )
            canvas.create_text(1024//2-20, 768//2-40, font = "fixedsys 40 bold", text= '''Leaderboard''', fill= "indigo")
        
            canvas.create_rectangle(1024//2- 150, 768//2+ 80, 1024//2+ 100, 768//2+ 180, fill= "IndianRed4" )
            canvas.create_rectangle(1024//2- 145, 768//2+ 85, 1024//2+ 95, 768//2+ 175, fill= "red", outline="IndianRed4" )
            canvas.create_text(1024//2-20, 768//2+120, font = "fixedsys 40 bold", text= '''replay?''', fill= "indigo")

            
        # draws game opening UI splash screen
        # play button, leaderboard button, and difficulty toggle button present
        elif not self.gameStarted:
            canvas.create_image(1024//2, 768//2, image=ImageTk.PhotoImage(self.background))
            canvas.create_text(1024//2-10, 768//2-250, font = "fixedsys 50 bold", text= '''112 Grudge\n Game 3D''', fill= "Red")
            canvas.create_rectangle(1024//2- 195, 768//2- 80, 1024//2+ 153, 768//2+ 20, fill= "IndianRed4" )
            canvas.create_rectangle(1024//2- 190, 768//2- 75, 1024//2+ 148, 768//2+ 15, fill= "red", outline="IndianRed4" )
            canvas.create_text(1024//2-20, 768//2-40, font = "fixedsys 40 bold", text= '''Leaderboard''', fill= "indigo")
        
            canvas.create_rectangle(1024//2- 150, 768//2+ 80, 1024//2+ 100, 768//2+ 180, fill= "IndianRed4" )
            canvas.create_rectangle(1024//2- 145, 768//2+ 85, 1024//2+ 95, 768//2+ 175, fill= "red", outline="IndianRed4" )
            canvas.create_text(1024//2-20, 768//2+120, font = "fixedsys 40 bold", text= '''Play?''', fill= "indigo")

            canvas.create_rectangle(1024//2- 195, 768//2 + 240, 1024//2+ 153, 768//2+ 340, fill= "IndianRed4" )
            canvas.create_rectangle(1024//2- 190, 768//2+ 245, 1024//2+ 148, 768//2+ 335, fill= "red", outline="IndianRed4" )
            canvas.create_text(1024//2-20, 768//2+280, font = "fixedsys 40 bold", text= '''Difficulty''', fill= "indigo")
        
        
        # draws the you Win splash screen
        # replay and leaderboard button present
        elif self.youWin:
            canvas.create_rectangle(0,0, self.width, self.height, fill = "pink")
            canvas.create_image(1024//2, 768//2, image=ImageTk.PhotoImage(self.winImage))
            canvas.create_text(1024//2+100, 768//2, font = "fixedsys 40 bold", text= f''' You escaped!!! Score: {self.playerRings}\n\n\n\n\n\n\n\n Look at some puppies!!!!   ''', fill= "blue")

            canvas.create_rectangle(1024//2- 195, 768//2- 80, 1024//2+ 153, 768//2+ 20, fill= "Green2" )
            canvas.create_rectangle(1024//2- 190, 768//2- 75, 1024//2+ 148, 768//2+ 15, fill= "Green4", outline="Green2" )
            canvas.create_text(1024//2-20, 768//2-40, font = "fixedsys 40 bold", text= '''Leaderboard''', fill= "blue")
        
            canvas.create_rectangle(1024//2- 150, 768//2+ 80, 1024//2+ 100, 768//2+ 180, fill= "Green2" )
            canvas.create_rectangle(1024//2- 145, 768//2+ 85, 1024//2+ 95, 768//2+ 175, fill= "Green4", outline="Green2" )
            canvas.create_text(1024//2-20, 768//2+120, font = "fixedsys 40 bold", text= '''replay?''', fill= "blue")

        
        # draws the actual game stuff 
        else:
            # creating the scene backdrops
            canvas.create_rectangle(0,20+self.height/3, self.width, self.height, fill = 'IndianRed4')
            # when grudge is moving the sky is black
            if self.grudgeisMoving:
                canvas.create_rectangle(0,0, self.width,20+ self.height/3, fill = "black")
            else:
                canvas.create_rectangle(0,0, self.width,20+ self.height/3, fill = "plum2")
        
            # creates a player object
            victim = Camera(self.playerX, self.playerY, self.playerdx, self.playerdy, \
                                                    self.playerAngle)

            startTime = time.time()
            
            # the magic!!!!
            victim.rayCast(self.gameMap, canvas)
            
            
            endTime = time.time()
            
            # creates the ring counter as well as health bar 
            # health bar color changes depending on health level
            canvas.create_rectangle(0,0,120,110,fill="saddle brown")
            canvas.create_text(60, 50, font = "arial 30 bold", text= str(self.playerRings), fill= "blue")
            canvas.create_rectangle(850,0,1024,75,fill="saddle brown")

            if self.health > 65:
                color = "green"
            elif 35< self.health <65:
                color = "yellow"
            else:
                color = "red"
                
            canvas.create_rectangle(865,22,875,52, fill= color, outline = color)
            canvas.create_rectangle(855,32,885,42, fill= color, outline= color)

            canvas.create_rectangle(900,25,1000,50, outline= "green")
            canvas.create_rectangle(900,25,900 + int(self.health),50, fill = color)

GrudgeGame(width = 1024, height = 768)

pygame.mixer.stop()

# Voila the end!