
import pygame, random


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
        self.velocity_x = random.randrange(-8, 8, 1)
        self.velocity_y = random.randrange(-6, 6, 1)
        

    def update(self):
        self.move()
        self.bounceOffWalls(0, 600, 0, 600)
    
    def bounceOffWalls(self, left, right, top, bottom):

        if self.rect.left < left:
            self.velocity_x *= -1
        elif self.rect.right > right:
            self.velocity_x *= -1

        if self.rect.top < top:
            self.velocity_y *= -1
        elif self.rect.bottom > bottom:
            self.velocity_y *= -1



class Hero(Entity):
    def __init__(self, x, y, w, h, color):
        Entity.__init__(self, x, y, w, h, color)

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
        self.speed = 10
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        self.move()
        self.stopOnWalls(0, 600, 0, 600)

    
    def stopOnWalls(self, left, right, top, bottom):

        if self.rect.left < left:
            self.velocity_x = 0
        elif self.rect.right > right:
            self.velocity_x = 0

        if self.rect.top < top:
            self.velocity_y = 0
        elif self.rect.bottom > bottom:
            self.velocity_y = 0


class Poison(Entity):
    def __init__(self, x, y, w, h, color):
        Entity.__init__(self, x, y, w, h, color)

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
        self.speed = 10
        self.velocity_x = random.randint(-5,5)
        self.velocity_y = random.randint(-5,5)

    def update(self):
        self.move()
        self.bounceOffWalls(0, 600, 0, 600)
            
    def bounceOffWalls(self, left, right, top, bottom):

        if self.rect.left < left:
            self.velocity_x *= -1
        elif self.rect.right > right:
            self.velocity_x *= -1

        if self.rect.top < top:
            self.velocity_y *= -1
        elif self.rect.bottom > bottom:
            self.velocity_y *= -1




class BugBomb(Entity):
    def __init__(self, x, y, w, h, color):
        Entity.__init__(self, x, y, w, h, color)

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
        self.speed = 10
        self.velocity_x = random.randint(-3,3)
        self.velocity_y = random.randint(-3,3)

    def update(self):
        self.move()
        self.bounceOffWalls(0, 600, 0, 600)


    def explode(self, poisonGroup):
        for i in range(3):
            x, y = self.rect.centerx, self.rect.centery
            w, h = 5, 5
            color = "white"
            poison = Poison(x, y, w, h, color)
            poisonGroup.add(poison)
            
    def bounceOffWalls(self, left, right, top, bottom):

        if self.rect.left < left:
            self.velocity_x *= -1
        elif self.rect.right > right:
            self.velocity_x *= -1

        if self.rect.top < top:
            self.velocity_y *= -1
        elif self.rect.bottom > bottom:
            self.velocity_y *= -1





def keystrokes(sprite):
    # Create a dictionary of booleans for each key on the keyboard
    key=pygame.key.get_pressed()
    
    if key[pygame.K_LEFT]:
            sprite.velocity_x = -sprite.speed
            sprite.velocity_y = 0
    if key[pygame.K_RIGHT]:
            sprite.velocity_x = 1.5 * sprite.speed
            sprite.velocity_y = 0
    if key[pygame.K_UP]:
            sprite.velocity_x = 0
            sprite.velocity_y = -sprite.speed
    if key[pygame.K_DOWN]:
            sprite.velocity_x = 0
            sprite.velocity_y = sprite.speed


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


def drawScoreboard(screen, scoreboard):
    x, y = 450, 10
    
    for item in scoreboard:
        msg = str("Level %d = %d" % (item[0], item[1]))
        w, h = 150, 25
        color = "red"
        textsize = 20
        scoreLbl = myLabel(screen,msg,x,y,w,h,color,textsize)
        y += 30


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


def createInsectSwarm(numInsects, insectGroup, bombGroup, screen_width, screen_height):
    for i in range(numInsects):
        x, y = random.randint(20, screen_width-20), random.randint(20, screen_height-20)
        w, h = 25, 25
        color = "cyan"
        insect = Insect(x, y, w, h, color)
        insectGroup.add(insect)

    for i in range(int(numInsects/20)):
        x, y = random.randint(20, screen_width-20), random.randint(20, screen_height-20)
        w, h = 50, 50
        color = "blue"
        bomb = BugBomb(x, y, w, h, color)
        bombGroup.add(bomb)
        
        




def main():
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
    numSeconds = 0

    # groups
    allSprites = pygame.sprite.Group()
    insectGroup = pygame.sprite.Group()
    heroGroup = pygame.sprite.Group()
    poisonGroup = pygame.sprite.Group()
    bombGroup = pygame.sprite.Group()

    # Sprite --- Hero
    x, y = screen_width/2, screen_height/2
    w, h = 50, 50
    color = "yellow"
    hero = Hero(x, y, w, h, color)
    allSprites.add(hero)
    heroGroup.add(hero)


    # Sprite --- Enemy Insect
    numInsects = 10
    createInsectSwarm(numInsects, insectGroup, bombGroup, screen_width, screen_height)

    # Scoreboard
    scoreboard = []

    # Game Loop
    gameover = False

    while not gameover:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
                pygame.quit()

        # Keystrokes
        keystrokes(hero)

        # Game Logic (collision detection, scoring)
        pygame.sprite.spritecollide(hero, insectGroup, True)
        pygame.sprite.groupcollide(insectGroup, poisonGroup, True, True)

        if pygame.sprite.spritecollide(hero, bombGroup, True):
            for bomb in bombGroup:
                bomb.explode(poisonGroup)
            

        if len(insectGroup) == 0:
            scoreboard.append([numInsects/10, numSeconds])
            numInsects += 10
            createInsectSwarm(numInsects, insectGroup, bombGroup, screen_width, screen_height)

        # Clear the Screen
        screen.fill(bg_color)

        # Drawing
        drawClockLabel(screen, numSeconds)
        drawInsectLabel(screen, len(insectGroup))
        drawScoreboard(screen, scoreboard)
        drawQuitButton(screen)

        allSprites.draw(screen)
        insectGroup.draw(screen)
        bombGroup.draw(screen)
        poisonGroup.draw(screen)

        # Updates
        allSprites.update()
        insectGroup.update()
        bombGroup.update()
        poisonGroup.update()

        # Next Frame
        pygame.display.update()
        clock.tick(fps)
        numSeconds += (1/fps)

main()



