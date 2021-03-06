import math, time, random, pygame, copy #Import some modules
from pygame.locals import *
clock = pygame.time.Clock()
class Barrel(pygame.sprite.Sprite):
    def __init__(self, difficulty):
        self.difficulty = difficulty
        super().__init__()
        self.correct, self.passed = False, None #Make sure this variable is false to start. Will become true when the question has been answered correctly and when the barrel has been passed.
        #Passed will be true if jumped over, false if the player hits it and none while neither has happene.d
        self.barrels = [] #Variable define: A variable to hold the multiple instances of barrels
        for self.a in range(0, 90, 10): #Loop around opening stuff
            self.barreltext = "Barrel" + str(self.a) + ".png" #Get the name of the next barrel.
            self.barrel = pygame.image.load("Barrels/"+ self.barreltext)
            self.barrel.convert() #Convert it
            self.barrel.set_colorkey((0, 0, 0)) #Set the background stuff
            self.barrel = pygame.transform.scale(self.barrel, (120, 120))#Scale it properly
            self.barrels.append(self.barrel)
        self.image = self.barrels[0].copy()
        self.rect = self.image.get_rect() #Get the rectangle.
        self.rect.bottomright = (0, round(800 * resolution)) #Move the rectangle to the proper locations.
        self.instance = 36
        #Text now
        self.font = pygame.font.SysFont("timesnewroman", 17) #Get the font ready
    def onScreen(self): #This will prepare the barrel for going onto the screen.
        self.text, self.answer, self.type = questionAnalyzer(self.difficulty) #Get the question to display on the barrel.
        if self.type == None or self.type == 'circle':
            self.displayText = self.font.render(self.text, 1, (255, 255, 255)) #Render text
            self.textPos = self.displayText.get_rect() #Set up for placing the text in the centre.
            self.textPos.center = self.image.get_rect().center #Place the font in the centre.
        elif self.type == 'rectangle': 
            self.displayText = pygame.Surface((120, 120), pygame.SRCALPHA, 32) #Make a surface with the same dimensions as the barrel
            self.displayText = self.displayText.convert_alpha()
            self.textPos = self.displayText.get_rect()
            self.textPos.center = self.image.get_rect().center
            self.rectangle = pygame.draw.rect(self.displayText, (0, 153, 255), (self.textPos.centerx - 30, self.textPos.centery - 30, 60, 60))
            #Do the length
            self.h = self.font.render(str(self.text[0]), 1, (255, 255, 255))
            self.hPos = self.h.get_rect()
            self.hPos.midright = self.rectangle.midleft
            self.displayText.blit(self.h, self.hPos)
            #Do the width
            self.b = self.font.render(str(self.text[1]), 1, (255, 255, 255))
            self.bPos = self.b.get_rect()
            self.bPos.midtop = self.rectangle.midbottom
            self.displayText.blit(self.b, self.bPos)
            #Do the area or perimeter
            self.temp = self.text[2] #Temporary variable to hold either the area or perimeter
            if self.temp == None: self.temp = "A = " #SOlving for area
            elif self.temp == False: self.temp = self.text[3]
            if self.temp == None: self.temp = "P = " #Solving for perimeter
            self.b = self.font.render(str(self.temp), 1, (255, 255, 255))
            self.bPos = self.b.get_rect()
            self.bPos.center = self.rectangle.center
            self.displayText.blit(self.b, self.bPos)
        elif self.type == 'triangle':
            self.displayText = pygame.Surface((120, 120), pygame.SRCALPHA, 32) #Make a surface with the same dimensions as the barrel
            self.displayText = self.displayText.convert_alpha()
            self.textPos = self.displayText.get_rect()
            self.textPos.center = self.image.get_rect().center
            self.triangle = pygame.draw.polygon(self.displayText, (0, 153, 255), [(self.textPos.w//4, self.textPos.h//4), (self.textPos.w//4, self.textPos.h//4 * 3), (self.textPos.w//4 * 3, self.textPos.h//4 * 3)]) #Draw a right triangle
            if len(self.text) < 3: #If we are asking a simple area question
                #Do the height
                self.h = self.font.render(str(self.text[1]), 1, (255, 255, 255))
                self.hPos = self.h.get_rect()
                self.hPos.midright = self.triangle.midleft
                self.displayText.blit(self.h, self.hPos)
                #Do the base
                self.b = self.font.render(str(self.text[0]), 1, (255, 255, 255))
                self.bPos = self.b.get_rect()
                self.bPos.midtop = self.triangle.midbottom
                self.displayText.blit(self.b, self.bPos)
                #Do the "A" 
                self.A = self.font.render("A = ", 1, (255, 255, 255))
                self.APos = self.A.get_rect()
                self.APos.center = self.triangle.center #Put it at the centre of the triangle rect, meaning where the hypotenuse is
                self.displayText.blit(self.A, self.Apos)
            else:
                #Do the b-value
                if self.text[1] == None: self.text[1] = "b"
                self.h = self.font.render(str(self.text[1]), 1, (255, 255, 255))
                self.hPos = self.h.get_rect()
                self.hPos.midtop = self.triangle.midbottom
                self.displayText.blit(self.h, self.hPos)
                #Do the a-value
                if self.text[0] == None: self.text[0] = "a"
                self.b = self.font.render(str(self.text[0]), 1, (255, 255, 255))
                self.bPos = self.b.get_rect()
                self.bPos.midright = self.triangle.midleft
                self.displayText.blit(self.b, self.bPos)
                #Do the c-value
                if self.text[2] == None: self.text[2] = "c"
                self.c = self.font.render(str(self.text[2]), 1, (255, 255, 255))
                self.cPos = self.c.get_rect()
                self.cPos.center = self.triangle.center
                self.displayText.blit(self.c, self.cPos)

    def roll(self, movement):
        self.instance += 1
        if 9 <= self.instance % 36 <= 17:
            self.image = self.barrels[self.instance %36 - 9].copy()
            self.image = pygame.transform.rotozoom(self.image, -90, 1)
        elif 18 <= self.instance % 36 <= 26:
            self.image = self.barrels[self.instance % 36 - 18].copy()
            self.image = pygame.transform.rotozoom(self.image, -180, 1)
        elif 27 <= self.instance % 36:
            self.image = self.barrels[self.instance %36 - 27].copy()
            self.image = pygame.transform.rotozoom(self.image, -270, 1)
        else: self.image = self.barrels[self.instance % 36].copy()
        self.rect = self.rect.move(movement, 0)#Move the barrel to the right
        self.textPos.center = self.image.get_rect().center
        self.image.blit(self.displayText, self.textPos)
    def reset(self, difficulty): #This function will be used to make a new question for the barrel and put it back in the original position.
        self.image = self.barrels[0].copy()
        self.correct, self.passed = False, None
        self.instance = 36
        self.rect.bottomright = (0, round(800 * resolution))

class Player(pygame.sprite.Sprite): #Make a class for the player
    def __init__(self, version):
        super().__init__()
        self.lives = 2 #2 lives before the game ends.
        self.done = False #Used for jumping the character
        #self.image = pygame.Surface((100, 300), pygame.SRCALPHA, 32)
        #self.image = self.image.convert_alpha()
        self.image = pygame.image.load("Elves versions/" + version)
        self.image.convert()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        #self.bottom = pygame.draw.rect(self.image, (255, 255, 255), (self.rect.centerx -50, self.rect.h//2 -50, 100, 100))
        #self.body = pygame.draw.circle(self.image, (255, 255, 255), (self.rect.centerx, self.rect.h//6 * 5), 50)
        #self.head = pygame.draw.polygon(self.image, (255, 255, 255), [(self.rect.w//4, 0), (self.rect.w//4 *3, 0), (self.rect.w ,self.rect.h//6), (self.rect.w//4 *3, self.rect.h//3), (self.rect.w//4, self.rect.h//3), (0, self.rect.h//6)])
        self.rect.bottomright = (round(1200 * resolution), round(800 * resolution)) #Reposition at 1200, 800
        self.originalRect = self.rect.copy() #Make this for referencing original position.
        self.timeReg, self.initVel = 0, (9.81 * math.sqrt(120/49))/1000 #Used for the jumping later.
    def jump(self):
        self.timePassed = int(round(time.time() *1000)) - self.timeReg
        #self.intendHeight = int(round(-243/250000 * (self.timePassed - 500)**2 + 243))
        self.intendHeight = int(round(-1/3125 * (self.timePassed - 750)**2 + 180)) #Quadratic equation vertex form: -1/3125(time - 750)^2 + 180
        #if self.timePassed <= 750: self.intendHeight = int(round(2/5*self.timePassed))
        #elif 750 < self.timePassed < 1750: self.intendHeight = int(round(-2/5625*(self.timePassed - 1125)**2 + 350))
        #elif self.timePassed >= 1750: self.intendHeight = int(round(-2/5 * self.timePassed + 900))
        #self.intendHeight = -27/25000 * (self.timePassed -1000/3)**2 + 120
        self.newY = self.originalRect.y - self.intendHeight
        #print("New Y :", self.newY, "Intend Height:", self.intendHeight, "TimeREG:", self.timeReg, "Time:", int(round(time.time()*1000)), "Time Difference:", int(round(time.time()*1000)) - self.timeReg)
        self.rect.move_ip(0,  self.newY - self.rect.y) #Guaranteed goodness.
        if self.timePassed >= 1500: #Stop after enough seconds.
            self.rect.move_ip(0, self.originalRect.y - self.rect.y) #Reset to original location
            return False #Stop Jumping!
        return True
    def hit(self):
        self.rect.right = round(1200 * resolution) #Move to edge of the right of the screen.
    def move(self, direction, minimumPos):
        if direction == "r": 
            if self.rect.right + 7 > 1200: self.rect.move_ip(1200 - self.rect.right, 0)
            else: self.rect.move_ip(7, 0)
        elif direction == "l":
            if self.rect.left -7 < minimumPos: self.rect.move_ip(minimumPos - self.rect.left, 0)
            else: self.rect.move_ip(-7, 0)
    def deathAnimation(self, timeSinceDeath):
        self.deathTime = int(round(time.time()*1000)) - timeSinceDeath #Time in miliseconds to be more precise.
        self.rect.y = self.originalRect.y - (int(round(-1/2500*(self.deathTime - 1000)**2 + 400)))
        if 50 < (self.deathTime % 200) <= 199: self.image = pygame.transform.rotozoom(self.image, 90, 1) #Rotate the character.
        if self.deathTime >= 2500: return True #Stop eventually
        return False

class AnswerBoard(pygame.sprite.Sprite): #Make a class for the answering board
    def __init__(self, screen):
        super().__init__()
        self.green, self.red, self.white = (0, 255, 0), (255, 0, 0), (255, 255, 255)
        self.font = pygame.font.SysFont("microsofthimalaya", 45)
        self.correct = None
        self.displayText = self.font.render("Answer : ", 1, self.white)
        self.rect = self.displayText.get_rect()
        self.rect.centery = screen.get_height()/5
        self.rect.centerx = screen.get_rect().centerx
        self.image = self.displayText
    def change(self, screen, correct, inputted):
        if correct == None: self.displayText = self.font.render("Answer : " + inputted, 1, self.white)
        elif not correct: self.displayText = self.font.render("Answer : " + inputted, 1, self.red)
        elif correct: self.displayText = self.font.render("Answer : " + inputted, 1, self.green)
        self.rect.centerx = screen.get_rect().centerx
        self.image = self.displayText
class scoreDisplay(pygame.sprite.Sprite): #Make a class for the display of the scoreboard
    def __init__(self):
        super().__init__()
        self.imageSafe = pygame.Surface((200, 75))
        self.imageSafe.fill((222, 184, 135))
        self.box = pygame.draw.rect(self.imageSafe, (245, 222, 179), (self.imageSafe.get_rect().centerx - 40, self.imageSafe.get_rect().centery - 25, 80, 50))
        self.rect = self.imageSafe.get_rect()
        self.rect.move_ip(round(50 * resolution), round(100 * resolution)) #Move
        self.image = self.imageSafe.copy() #So that we can blit the text onto the new image without affecting the old one.
        #Text now
        self.font = pygame.font.SysFont("freestylescript", 45)
        self.text = self.font.render("0", 1, (255, 255, 255))
        self.textPos = self.text.get_rect()
        self.textPos.center = self.image.get_rect().center
        self.image.blit(self.text, self.textPos)
    def Update(self, score): #Make an update function
        self.image = self.imageSafe.copy()
        self.text = self.font.render(str(score), 1, (255, 255, 255))
        self.textPos = self.text.get_rect()
        self.textPos.center = self.image.get_rect().center
        self.image.blit(self.text, self.textPos)
class Menu(pygame.sprite.Sprite): #Make a menubutton class
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((400, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (round(600 * resolution), round(400 * resolution)) #Position it at the centre of the screen.
        self.image.fill((102, 51, 0))

        self.font = pygame.font.SysFont("timesnewroman", 45)
        self.text = self.font.render("Return to Main Menu", 1, (204, 102, 0))
        self.textPos = self.text.get_rect()
        self.textPos.center = (self.image.get_rect().centerx, self.image.get_rect().h/3)
        self.image.blit(self.text, self.textPos)
        
        #self.font = pygame.font.SysFont("timesnewroman", 25)
        #self.text = self.font.render("All progress will be lost", 1, (204, 103, 0))
        #self.textPos = self.text.get_rect()
        #self.textPos.center = (self.image.get_rect().centerx, self.image.get_rect().h/3 *2)
        #self.image.blit(self.text, self.textPos)
class timeDisplay(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.startTime = round(time.time()) #Set the start time of the game.
        self.font = pygame.font.SysFont("timesnewroman", 35)
        self.image = self.font.render("00:00", 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topright = screen.get_rect().topright
    def Update(self): #Make something to update the time display
        self.newTime = round(time.time())
        self.mins, self.secs = (self.newTime - self.startTime)//60, (self.newTime - self.startTime) % 60
        self.mins, self.secs = str(self.mins), str(self.secs)
        if len(self.mins) < 2: self.mins = "0" + self.mins
        if len(self.secs) < 2: self.secs = "0" + self.secs
        self.image = self.font.render(self.mins + ":" + self.secs, 1, (255, 255, 255))

def box(screen, text, correct, oldTextPos): #Make this function to draw the box for the input.
    if oldTextPos != None: screen.fill((0 ,0 ,0), oldTextPos) #Get rid of what is there
    font = pygame.font.SysFont("microsofthimalaya", 25) #Get font variable
    green, red, white = (0, 255, 0), (255, 0, 0), (255, 255, 255) #Make some colours.
    if correct == False: displayText = font.render(text, 1, red)
    elif correct == True: displayText = font.render(text, 1, green)
    elif correct == None: displayText = font.render(text, 1, white)
    textpos = displayText.get_rect()
    textpos.centerx = screen.get_rect().centerx
    textpos.centery = screen.get_height()/5
    screen.blit(displayText, textpos)
    pygame.display.flip()
    return textpos
def keyer(): #Make a function to get the key that was pressed down.
    event = pygame.event.poll()
    if event.type == KEYDOWN:
        return event.key
def questionAnalyzer(difficulty): #Make a function that will generate the barrel questions Difficulty affects both the speed of the barrels and the question difficulty.
    #Below is to deal with how to display the questions generated
    question = questionCreator(difficulty)    
    if 1 <= difficulty <= 2:
        if difficulty == 1:interval = 10 #Variable define: This will regulate how fast the barrels move later on.
        else: interval = 7
        answer = question['answer']
        text = str(question['values'][0]) + str(question['operation']) + str(question['values'][1]) #Format this properly.
    elif difficulty == 3:
        interval = 10 #Variable define: This will regulate how fast the barrels move later on.
        questionType = question['questionType']
        if questionType == 1:
            text = str(question['a']) + " = " + str(question['b']) + " " + question['operation 1'] + " " + str(question['c']) + " " + question['operation 2'] + " " + str(question['d']) #Make the text variable
            answer = question['answer']
        elif 2<= questionType <=  3: 
            text = str(question['values'][0]) + str(question['values'][2]) + question['values'][1] + " " + question['values'][3] + " " + str(question['values'][4]) #Big mouthful for one line.
            answer = question['answer']
        elif 4<= questionType <= 5: 
            text = question['equation']
            answer = question['answer']
    elif difficulty == 4:
        type = question['type']
        answer = question['answer']
        if type == 'rectangle' or type == 'triangle': 
            text = question['values']
        elif type == 'circle':
            text = str(question['A']) +  "=" + chr(960) + str(question['r']) + "^2"
        return (text, answer, question['type'])
    return (text, answer, None)
def main(difficulty, user): #User is the user's information
    global resolution
    try:
        resolution = user["resolution"]
        resolution = resolution / 100
    except Exception:
        resolution = 1.0

    pygame.init()
    screen = pygame.display.set_mode((round(1200 * resolution), round(800 * resolution)))
    pygame.display.set_caption("Ape Over Math - In Game")
    pygame.mixer.init()
    musicList = user['gameMusic']
    musicSelection = pygame.mixer.Sound("Music/In Game/" + musicList[random.randint(0, len(musicList) - 1)]) #Get a random music file to play
    musicSelection.play(-1)
    pygame.key.set_repeat(150, 5) #If the user holds the key down, keep doing the action
    if user['background'] != "": backgroundJungle = pygame.image.load("Player Background/" + user['background']) #Import the image selected by the player.
    else: backgroundJungle = pygame.image.load("jungleHD.png")
    backgroundJungle = pygame.transform.scale(backgroundJungle, (round(1200 * resolution), round(800 * resolution)))
    backgroundJungle = backgroundJungle.convert()
    screen.blit(backgroundJungle, (0,0))
    succession, score = 20.0, 0  #Variable define: This variable will control the rate at which barrels hurtle at the player. Score is the player's score.
    barrel, answerBoard, scoreboard, character, menubutton, timedisplay =  Barrel(difficulty), AnswerBoard(screen), scoreDisplay(), Player(user['character']), Menu(), timeDisplay(screen)
    barrels = pygame.sprite.Group(barrel) #Add the text and the barrel to the barrels group
    for barrelMaker in range(0, 5): #Make 5 more barrels so we do not need to make them during the game. Also restricts the game to allow only 6 barrels at a time.
        #newbarrel = copy.deepcopy(barrel) #Copy the last barrel.
        newbarrel = Barrel(difficulty)
        #newbarrel.reset(difficulty)
        barrels.add(newbarrel)
    barrel.onScreen()
    objects = pygame.sprite.Group(barrel, answerBoard, scoreboard, character, timedisplay)
    jump, movement, jumpStat, reg, furthestRight, menu, timepaused, answerChances = False, 3, False, False, 0, False, 0, 2 #Variable define: reg determines if the jumping of the player has been registered already.
    inputted = "" #Make a variable for what the user inputs.
    turn = 0 #Variable define: Will be used to determine if we should turn the barrel or not.
    correct = None #Define some variables to be used later.
    timeReg = time.time() #Variable define: This will be where we register times.
    barrelOptions, posList, answerList = [], [], []
    while character.lives > 0:
        keyPressed = keyer() #See if key has been pressed
        if keyPressed == K_ESCAPE and not menu:
            startPause = time.time() #Get the time we start the pausing.
            menu = True
            objects.add(menubutton)
            objects.draw(screen)
            pygame.display.flip()
            continue
        elif keyPressed == K_ESCAPE and menu:
            timePaused = time.time() - startPause #Get the total time we paused for.
            timeReg += timePaused
            timedisplay.startTime += round(timePaused) #This will assure that the time display doesn't count while the player is in the pause menu.
            menu = False
            objects.remove(menubutton)
        elif keyPressed != K_ESCAPE and menu:
            if menubutton.rect.topleft < pygame.mouse.get_pos() < menubutton.rect.bottomright and pygame.mouse.get_pressed() == (True, False, False):
                pygame.mixer.quit()
                pygame.quit()
                return None
            objects.draw(screen)
            pygame.display.flip()
            continue
        if keyPressed == K_RIGHT or keyPressed == K_d: character.move("r", furthestRight)
        elif keyPressed == K_LEFT or keyPressed == K_a: character.move("l", furthestRight)
        if jump and keyPressed == K_SPACE or jumpStat == True: 
            if not reg:
                inputted = ""
                correct = None
                character.timeReg = int(round(time.time() * 1000))
                reg = True
            jumpStat = character.jump() #If we're allowed to jump, let's jump.
            jump = jumpStat
            if not jumpStat: 
                reg = False
        turn += 1
        furthestRight = 0 #Reset this variable
        clock.tick(60) #Limit to 60 fps
        screen.fill((0, 0, 0))
        screen.blit(backgroundJungle, (0,0))
        #if turn % 5400 == 0: movement += 1
        if turn % 4 == 0: #Limit how many times the barrels move.
            posList, answerList, barrelOptions = [], [], []
            collisionList = pygame.sprite.spritecollide(character, barrels, False, None) #Get a list of the barrels that are colliding with the player.
            for collisionGo in range(0, len(collisionList)):
                if collisionList[collisionGo] in objects: #Only do this for barrels that are actually in the game.
                    answerChances = 2 #Reset this variable so the user gets more chances to answer the question.
                    character.lives -= 1 #Subtract from the lives of the player
                    inputted = ""
                    correct = None
                    if character.lives > 0: character.hit() #Only do this while no death animation will go
                    objects.remove(collisionList[collisionGo])
                    collisionList[collisionGo].reset(difficulty)
                    #collisionList[collisionGo].passed = False
            barrelList = barrels.sprites()
            for barrelRoller in range(0, len(barrelList)): #Loop around the barrels group to make them all roll
                object = barrelList[barrelRoller]
                if objects.has(object): #Roll only the barrels that need to be on screen.
                    object.roll(movement)
                    if character.rect.right < object.rect.left and object.correct and object.passed == None: #This will decide if the player has passed the object.
                        object.passed = True
                        answerChances = 2 #Reset this variable so the player can answer the questions again in the future.
                        score += 5
                    if object.rect.left >= round(1200 * resolution): 
                        objects.remove(object) #If the barrel runs off screen, remove it from the group of onscreen stuff.
                        object.reset(difficulty)
                        barrels.update(object)
                    else:
                        if object.correct == False and object.passed == None: #Only do this if the question has not been answered and jumped over.
                            barrelOptions.append(object)
                            posList.append(object.rect.x) #Append the x coordinate.
                            answerList.append(object.answer) #Also append the answer to the question
                        barrels.update(object)
                        objects.update(object) #Update the objects class
                elif time.time() - timeReg >= succession: #If this is true, make another barrel.
                    timeReg = time.time()
                    succession -= 0.3 #Subtract so that next time the barrel comes a little earlier each time, making it harder every time.
                    object.onScreen()
                    barrelOptions.append(object)
                    objects.add(object) #Add it to the group of stuff that goes on screen.
                    posList.append(object.rect.x) #Append the x coordinate.
                    answerList.append(object.answer) #Also append the answer to the question
            if len(barrelOptions) > 0:
                if len(posList) > 1: furthestRight = max(posList) + round(120 * resolution) #Prevent the player from going too close to the next barrel.
                answerPos = posList.index(max(posList))
                answer = answerList[answerPos]
                barrelToAnswer = barrelOptions[answerPos] #Need this in case the user get the answer right.
            else: furhtestRight = 0
        if len(barrelOptions) > 0 and type(keyPressed)== int and (48 <= keyPressed <= 57 or keyPressed == 45) and answerChances > 0: #We make sure that they are only inputting numbers or negative sign "-"
            if correct == False:
                correct = None
                inputted = ""
            inputted += str(chr(keyPressed))
            print(inputted, answer)
            if inputted[-1] == str(answer)[len(inputted)-1]: 
                if inputted != str(answer): correct = None
                elif inputted == str(answer): 
                    barrelToAnswer.correct, correct = True, True #True to be green and to tell the barrel it has been answered.
                    score += 10 #Increase score per question answered correctly
                    jump = True
            else: 
                correct = False
                answerChances -= 1 #Subtract from the amount of chances the user gets
        answerBoard.change(screen, correct, inputted) #Update the answering board.
        scoreboard.Update(score)
        timedisplay.Update()
        objects.update(answerBoard, scoreboard, character, timedisplay)
        objects.draw(screen)
        pygame.display.flip()
    deathSound = pygame.mixer.Sound("deathSound.wav")
    deathSound.set_volume(1.0)
    musicSelection.stop()
    deathSound.play(0)
    timetoDeath = int(round(time.time()*1000)) #Get the time in miliseconds since beginning of the death
    done = False
    while not done:
        clock.tick(60)
        done = character.deathAnimation(timetoDeath)
        objects.update(character)
        screen.fill((0, 0, 0))
        screen.blit(backgroundJungle, (0,0))
        objects.draw(screen)
        pygame.display.flip()
    objects.add(menubutton)
    while True:
        event = pygame.event.poll()
        objects.draw(screen)
        pygame.display.flip()
        if event.type == MOUSEBUTTONDOWN: break
    pygame.mixer.quit()
    pygame.quit()
    return score

def questionCreator(difficulty): #Make a function that will make the question for the barrel
    #Operation legend: 1 = addition, 2 = subtraction, 3 = multiplication, 4 = division, 5 = powers, 6 = square roots.
    if difficulty == 1:
        acceptable = False
        while not acceptable:
            num1, num2 = random.randint(0, 100), random.randint(0, 100)
            operation = random.randint(1, 2) #Make a random number between 1 and 2 to decide the operation that will be used
            if operation == 1: 
                answer = num1 + num2
                if answer %5 == 0 or answer %2 == True: acceptable = True
                else: continue
                operation = "+"
            elif operation == 2: 
                oldNum1, oldNum2 = num1, num2
                num1, num2 = max(oldNum1, oldNum2), min(oldNum1, oldNum2)
                answer = num1 - num2
                if answer %5 == 0 or answer %2 == 0: acceptable = True
                else: continue
                operation = "-"
        equation = {'operation': operation, 'answer': answer, 'values':[num1, num2]} #Variable define: Making a list for all of the numbers and the operation.

    elif difficulty == 2: #Get questions for difficulty 2
        operation = random.randint(1, 4) #Make a random number between 1 and 4 to get the operation that will be used.
        if operation <= 2: #1: addition, 2: subtraction
            num1, num2, = random.randint(0, 100), random.randint(0, 30), 
            oldnum1, oldnum2 = num1, num2 #Variable define: The numbers for addition or subtraction.
            if operation == 1: 
                operation = "+"
                answer = num1 + num2 #Get the answer
            elif operation == 2: 
                operation = "-"
                num1, num2 = max(oldnum1, oldnum2), min(oldnum1, oldnum2) #Variable define: The numbers for subtraction
                answer = num1 - num2 #Get the answer.
        elif operation == 3: #3: Multiplication
            operation = chr(215) #Multiplication symbol
            num1, num2 = random.randint(0, 12), random.randint(0, 12)
            answer = num1 * num2
        elif operation == 4: #4: Division
            operation = chr(247) #Division symbol FTW
            num2 = random.randint(0, 12) #num2 is the divisor
            num1 = num2 * random.randint(0, 12) #num1 is then number to be divided.
            answer = num1 // num2
        equation = {'operation' : operation, 'answer': answer, 'values': [num1, num2]} #Variable define: Making a dictionary for all of the numbers and the operation.

    elif difficulty == 3:
        questionType = random.randint(1, 5) #Variable define: We wil decide if we're doing a reverse-operations question (1), a powers or square root question (2 and 3) or an order of operations question (4 and 5).
        if questionType == 1: #These question types (reverse operations) will be binomials with one variable of the form a = bc + d or a = b/c - d or other variations. The unknown will be either b, c or d.
            unknown = random.randint(0, 2) #Decide who will be the unknown. 1 = b, 2 = c, 3 = d
            op1, op2 = random.randint(1, 2), random.randint(1, 2) #Decide which operations to perform.
            b, c, d = random.randint(1, 15), random.randint(1, 15), random.randint(0, 100) #Variable define: Come up with all of the numbers in the equation.
            bc = b *c #We want this to run no matter what so that we can either use it for multiplication or for a nice integer division.
            if op1 == 1: op1 = chr(215)
            elif op1 == 2: #2 is division
                op1 = chr(247)
                b = bc #Make b bc so that it will be an integer division.
                bc = bc//c #Get the results of that part.
            if op2 == 1: 
                a = bc + d #+
                op2 = "+"
            elif op2 == 2: 
                a = bc - d #-
                op2 = "-"
            funList = [b, c, d]
            answer = funList[unknown]
            funList[unknown] = "x"
            b= funList[0]
            c = funList[1]
            d = funList[2]
            equation = {'questionType':questionType,'answer': answer,  'a':a, 'b':b, 'c':c, 'd':d, 'operation 1':op1, 'operation 2':op2, 'unknownValue':unknown} #Get ready to return the equation for the pygame to display during the game and to be displayed on the barrels.
        elif 2 <= questionType <= 3: #Equation of the form [math.sqrt]x[^2] [+][-] y
            psqrt = random.randint(0, 2) #Decide whether or not we're doing a power or a square root. 0 and 1 are power so that it is twice as likely.
            plusminus = random.randint(1, 2) #Decide if we will add or subtract y. 1 = add, 2 = subtract
            if psqrt != 2:
                psqrt = ""
                #Make the power.
                power = random.randint(1, 10) 
                if 9<= power : power = 2 #We want the power of 2 primarily.
                elif 7 <= power <= 8: power = 3 #We also want it to be more likely to have a power of 3. 
                base = random.randint(1, 12) #Make the base that will be put to an exponent.
                pAns = base ** power
                power = "^" + str(power) #Convert to string for later usage
                #This all means that powers of 1, 2, 3, 4, 5 and 6 are all possible but 2 is three times more likely and 3 is twice as likely.
            else:
                psqrt = chr(8730)
                pAns = random.randint(1, 12)
                base = pAns ** 2
                power = ""
            addsubtractNum = random.randint(1, 9) #Generate the random number that we will be adding to the power's product.
            if plusminus == 1: 
                answer = pAns + addsubtractNum
                plusminus = "+"
            else: 
                answer = pAns - addsubtractNum
                plusminus = "-"
            equation = {'questionType': questionType, 'answer':answer, 'values':[psqrt, power, base, plusminus, addsubtractNum]}
        elif 4 <= questionType <= 5: #Order of operations
            opNum = random.randint(3, 5) #Determine how many operators there will be, between 3 and 5.
            soFar = [] #Make a list that will eventually contain everything necessary for the equation.
            opList = ["+", "-", "*", "/"]
            for operators in range(0, opNum): #Loop around generating operators and numbers.
                if soFar.count("*") == 2 and "*" in opList: opList.remove("*") #We do not want more than two multiplication operators in any one equation.
                if soFar.count("/") == 1 and "/" in opList: opList.remove("/") #No more than 1 division operator per equation.
                if soFar.count("+") == 2 and "+" in opList: opList.remove("+") #No more than 2 addition operators.
                if soFar.count("-") == 2 and "-" in opList: opList.remove("-") #No more than 2 subtraction operator.
                number, operator = random.randint(1, 8), opList[random.randint(0, len(opList) -1)]
                try: 
                    if soFar[-1] == "/": 
                        soFar[-2] = number * soFar[-2]
                except IndexError: pass
                if operators != opNum -1: 
                    soFar.append(number)
                    soFar.append(operator)
                else: soFar.append(number)
            totalEquation = soFar.copy() #Duplicate the list of everything so far to be held for the end.
            while soFar.count("/") > 0 or soFar.count("*") > 0:
                if soFar.count("/") > 0: divisionPos = soFar.index("/")
                else: divisionPos = len(soFar)
                if soFar.count("*") > 0: multiplyPos = soFar.index("*")
                else: multiplyPos = len(soFar)
                num1, num2 = soFar[min(divisionPos, multiplyPos) -1], soFar[min(divisionPos, multiplyPos) + 1]
                if divisionPos < multiplyPos: 
                    replacement = num1//num2
                    for divisionB in range(0, 3): del soFar[divisionPos -1]
                    soFar.insert(divisionPos -1, replacement)
                else: 
                    replacement = num1 * num2
                    for multiplyB in range(0, 3): del soFar[multiplyPos -1]
                    soFar.insert(multiplyPos -1, replacement)
            while soFar.count("-") > 0:
                subtractionPos = soFar.index("-")
                num1, num2 = soFar[subtractionPos -1], soFar[subtractionPos + 1]
                replacement = num1-num2
                for subtractionB in range(0, 3): del soFar[subtractionPos -1]
                soFar.insert(subtractionPos -1, replacement)
            while soFar.count("+") > 0:
                additionPos = soFar.index("+")
                num1, num2 = soFar[additionPos -1], soFar[additionPos + 1]
                replacement = num1+num2
                for additionB in range(0, 3): del soFar[additionPos -1]
                soFar.insert(additionPos -1, replacement)
            answer = soFar[0]
            totalEquationStr = "" #Variable for the totalequation's string version
            for equationMaker in range(0, len(totalEquation)): #Make the totalequation into a string
                totalEquationStr += str(totalEquation[equationMaker])
            equation = {'questionType':questionType, 'answer': answer, 'equation':totalEquationStr} #Get ready to return this all.

    elif difficulty == 4: #Questions of the application type, where the person must apply their knowledge.
            shape = random.randint(0, 2) #0: Rectangle, 1: Right Triangle, 2: Circle
            unknown = random.randint(2, 2) #0: Perimeter, 1: Area, 2: Side
            if shape == 0: #Rectangle
                l = random.randint(5, 100)
                w = random.randint(5, 100)
                unknowner = False
                if unknown == 2: 
                    unknowner = True #Variable to tell the two other if statements if we will have an unknown side length
                    unknown = random.randint(0, 1) #Chose between area or perimeter.
                if unknown == 0:
                    unknown = "Perimeter"
                    A = False
                    answer = 2*(l + w) #Perimeter
                    P = None
                    if unknowner:
                        P = "P=" + str(answer)
                        answer = l
                        l = "L"
                elif unknown == 1: 
                    unknown = "Area"
                    P = False
                    answer = l*w #Area
                    A = None
                    if unknowner: 
                        A = "A=" + str(answer)
                        answer = l
                        l = "L"
                equation =  {'type': 'rectangle', 'values': [l, w, A, P], 'answer': answer} #Return a proper dictionary
            elif shape == 1: #Triangle
                b = random.randint(1, 10)
                h = random.randint(1, 10)
                if 0 <= unknown <= 1: 
                    answer = b*h//2 #Get the area
                    values = [b, h]
                elif unknown == 2:
                    unknown2 = random.randint(0, 2) #Chose which side, between the 3 triangle sides are unknown.
                    right = False #We need for num1 and num2 to not both be odd, so loop around until they're right
                    while not right:
                        num1, num2 = random.randint(1, 10), random.randint(1, 10)
                        if num1 %2 != 0 and num2 %2 != 0: continue
                        else: right = True
                    m, n = max(num1, num2), min(num1, num2)
                    k = random.randint(2, 7)
                    values = [k*(m**2 - n**2), k* 2*m*n, k*(m**2 + n**2)]
                    answer = values[unknown2] #Get the answer
                    values[unknown2] = None
                equation =  {'type': 'triangle', 'answer': answer, 'values': values}
            elif shape == 2: #Circle
                r = random.randint(1, 5)
                A = round(math.pi * (r**2))
                decision = random.randint(1, 2) #Decide if we will give them the radius or the area
                if decision == 1: answer, r = r, "r" #Give them the area
                else: answer, A = A, "A" #Give them the radius
                equation = {'type': 'circle', 'A': A, 'r': r, 'answer': answer}

    return equation
