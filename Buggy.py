
import pygame, random


#################################
# Functions


# This function will return the RGB code for the colors
def getColor(color):
    D = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "orange": (250, 250, 0),
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "gold": (255, 215, 0),
        "pink": (255, 192, 203)
    }
    return D[color]



# This function will create a Button
def myButton(screen,msg,x,y,w,h,ic,ac,textsize,textcolor,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, getColor(ac),(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, getColor(ic),(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",textsize)
    textSurf, textRect = renderText(msg, smallText, textcolor)
    textRect.center = (x + w/2, y + h/2)
    screen.blit(textSurf, textRect)


# This function will create a Label
def myLabel(screen, msg,x,y,w,h,color,textsize):

    smallText = pygame.font.SysFont("comicsansms", textsize)
    textSurf, textRect = renderText(msg, smallText, color)
    textRect.center = (x + w/2, y + h/2)
    screen.blit(textSurf, textRect)


# This function returns the surface & rect of the textbox
def renderText(msg, font, color):
    surface = font.render(msg, True, getColor(color))
    rect = surface.get_rect()
    return [surface, rect]


#################################
# GUI

def quitGame():
    pygame.quit()


def drawQuitButton(screen):
    msg = "Quit"
    x, y = 10, 70
    w, h = 100, 25
    ic, ac = "black", "gold"
    textsize = 20
    textcolor = "white"
    quitBtn = myButton(screen,msg,x,y,w,h,ic,ac,textsize,textcolor,action=quitGame)


def drawClockLabel(screen, numSeconds):
    msg = str("Time = %d" % (numSeconds))
    x, y = 10, 10
    w, h = 100, 25
    color = "white"
    textsize = 20
    timeLbl = myLabel(screen,msg,x,y,w,h,color,textsize)


def drawInsectLabel(screen, numInsects):
    msg = str("Enemies Left = %d" % (numInsects))
    x, y = 10, 40
    w, h = 100, 25
    color = "white"
    textsize = 20
    timeLbl = myLabel(screen,msg,x,y,w,h,color,textsize)


def drawScoreboard(screen, hero_score, hero_stats):

    msg = str("Score = %d pts" % hero_score)
    x, y = 450, 10
    w, h = 150, 25
    color = "gold"
    textsize = 20
    scoreLbl = myLabel(screen,msg,x,y,w,h,color,textsize)

    x, y = 450, 50
    for item in hero_stats:
        msg = str("Level %d = %d" % (item[0], item[1]))
        w, h = 150, 25
        color = "red"
        textsize = 20
        scoreLbl = myLabel(screen,msg,x,y,w,h,color,textsize)
        y += 30


#################################
# Classes

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self)

        # Position
        self.x = x
        self.y = y

        # Size
        self.w = w
        self.h = h

        # Appearance
        self.color = color

        # Surface ***
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(getColor(self.color))

        # Rect ***
        self.rect = self.image.get_rect()

        # Position of the Sprite
        self.rect.x = self.x
        self.rect.y = self.y

        # Velocity of the Sprite
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        pass
        
    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def loadImage(self, imageName):
        self.imageName = imageName

        # Load an image onto the surface
        self.image = pygame.image.load(self.imageName)
        self.image = pygame.transform.scale(self.image, (75, 75))
        pygame.draw.rect(self.image, getColor(self.color), [self.x, self.y, self.w, self.h])



class Insect(Entity):
    def __init__(self, x, y, w, h, color):
        Entity.__init__(self, x, y, w, h, color)

        # Parameters
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

        # Set Position
        self.rect.x = self.x
        self.rect.y - self.y

        # Set Velocity
        self.velocity_x = random.choice([-9, -7, -5,-3, 3, 5, 7, 9])
        self.velocity_y = random.choice([-6, -4, -2, 2, 4, 6])

    def update(self):
        self.move()
        self.bounceOffWalls(0, 600, 0, 600)
    
    def bounceOffWalls(self, left, right, top, bottom):

        # Left Edge
        if self.rect.left < left:
            self.velocity_x *= -1
        # Right Edge
        if self.rect.right > right:
            self.velocity_x *= -1
        # Top Edge
        if self.rect.top < top:
            self.velocity_y *= -1
        # Bottom Edge
        if self.rect.bottom > bottom:
            self.velocity_y *= -1

        

class Hero(Entity):
    def __init__(self, x, y, w, h, color):
        Entity.__init__(self, x, y, w, h, color)

        # Parameters
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

        # Set Position
        self.rect.x = self.x
        self.rect.y - self.y

        # Set Velocity
        self.speed = 10
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        self.keystrokes()
        self.move()
        self.stopOnWalls(0, 600, 0, 600)

    def stopOnWalls(self, left, right, top, bottom):
        # Left Edge
        if self.rect.left < left:
            self.velocity_x = 0
        # Right Edge
        if self.rect.right > right:
            self.velocity_x = 0
        # Top Edge
        if self.rect.top < top:
            self.velocity_y = 0
        # Bottom Edge
        if self.rect.bottom > bottom:
            self.velocity_y = 0

    def keystrokes(self):
        # Create a dictionary of booleans for each key on the keyboard
        key=pygame.key.get_pressed()

        # Press the left arrow key
        if key[pygame.K_LEFT]:
                self.velocity_x = -self.speed
                self.velocity_y = 0
        # Press the right arrow key
        if key[pygame.K_RIGHT]:
                self.velocity_x = 1.5 * self.speed
                self.velocity_y = 0
        # Press the up arrow key
        if key[pygame.K_UP]:
                self.velocity_x = 0
                self.velocity_y = -self.speed
        # Press the down arrow key
        if key[pygame.K_DOWN]:
                self.velocity_x = 0
                self.velocity_y = self.speed


############################
# Globals

# initialize
pygame.init()

# screen
screen_width = 600
screen_height = 600
screen_size = [screen_width, screen_height]
bg_color = (0,0,0)
screen = pygame.display.set_mode(screen_size)

# title
title = "Buggy"
pygame.display.set_caption(title)

# clock
fps = 30
clock = pygame.time.Clock()

# groups
allSprites = pygame.sprite.Group()
insectGroup = pygame.sprite.Group()
heroGroup = pygame.sprite.Group()

# sprite instance --- hero
x, y = screen_width/2, screen_height/2
w, h = 50, 50
color = "yellow"
hero = Hero(x, y, w, h, color)
allSprites.add(hero)
heroGroup.add(hero)

# Insect Swarm
def createSwarm(numInsects):
    for i in range(numInsects):
        x, y = random.randint(20, screen_width-20), random.randint(20, screen_height-20)
        w, h = 25, 25
        color = "cyan"
        insect = Insect(x, y, w, h, color)
        insectGroup.add(insect)


############################
# Game Loop

def gameloop():
    numSeconds = 0
    numInsects = 10
    hero_score = 0
    hero_stats = []
    
    gameover = False

    # sprite instance --- swarm of insects
    createSwarm(numInsects)
    
    while not gameover:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
                pygame.quit()

        # Game Logic (collision detection, scoring)
        trapped = pygame.sprite.spritecollide(hero, insectGroup, True)

        if trapped:
            hero_score += 25

        if len(insectGroup) == 0:
            hero_stats.append([numInsects/10, numSeconds])
            numInsects += 10
            createSwarm(numInsects)

        # Clear the Screen
        screen.fill(bg_color)

        # Drawing
        drawClockLabel(screen, numSeconds)
        drawInsectLabel(screen, len(insectGroup))
        drawScoreboard(screen, hero_score, hero_stats)
        drawQuitButton(screen)

        # Group --- draw
        allSprites.draw(screen)
        insectGroup.draw(screen)

        # Updates
        allSprites.update()
        insectGroup.update()

        # Next Frame
        pygame.display.update()
        clock.tick(fps)
        numSeconds += (1/fps)

gameloop()
