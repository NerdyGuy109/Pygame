

import pygame
import random
import math


# Colors
def myColors(color):
    D = {
        "white": (255, 255, 255),   # max = 255, min = 0
        "black": (0,0,0),
        "red": (255,0,0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
    }

    if color in D.keys():
        return D[color]
    else:
        return (0, 0, 0)   # black is default


# Widget Classes
class MyButton(pygame.sprite.Sprite):
    def __init__(self, screen, text, x, y, w, h, action=None):
        super().__init__()
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.spot = (self.x, self.y, self.w, self.h)
        self.action = action
        self.ic = myColors("white")  # inactive color
        self.ac = myColors("red")    # active color
        self.textColor = myColors("black")
        self.fontType = "comicsansms"
        self.smallText = pygame.font.SysFont(self.fontType, 20)
        self.largeText = pygame.font.SysFont(self.fontType, 40)

        self.image = self.smallText.render(self.text, True, self.textColor)
        self.rect = self.image.get_rect()
        self.rect.center = ((self.x + (self.w / 2)), (self.y + (self.h / 2)))

    def update(self):
        # self.checkForMouse()
        self.screen.blit(self.image, self.rect)

    def changeText(self, text):
        self.text = text
        self.image = self.smallText.render(self.text, True, self.textColor)
        self.rect = self.image.get_rect()
        self.rect.center = ((self.x + (self.w / 2)), (self.y + (self.h / 2)))

    def checkForMouse(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x + self.w > mouse[0] > self.x:
            if self.y + self.h > mouse[1] > self.y:
                pygame.draw.rect(self.screen, self.ac, self.spot)

                if click[0] == 1 and self.action != None:
                    self.action()
        else:
            pygame.draw.rect(self.screen, self.ic, self.spot)


# Sprite
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        super().__init__()
        # Position
        self.x = x
        self.y = y
        # Size
        self.w = w
        self.h = h
        # Color
        self.color = color   # "red"
        self.colorCode = myColors(color)  # (255, 0 ,0)
        # Image
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(self.colorCode)
        # Rect
        pygame.draw.rect(self.image, self.colorCode, [self.x, self.y, self.w, self.h])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        # Picture
##        self.fileName = str("oxygen_molecule.png")
##        self.image = pygame.image.load(self.fileName)
##        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        # Motion
        self.velocity_x = random.choice([-10, -8, -6, 6, 8, 10])   
        self.velocity_y = random.choice([-10, -8, -6, 6, 8, 10])
        self.speed = 3                              # used for keyboard events
        if self.velocity_x != 0:
            self.angle = math.degrees(math.atan(float(self.velocity_y/self.velocity_x)))

    def update(self):
        # Based on the speed, change the position   Xf = Xi + V * T ---- (m/s) * (s/1) = m
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def bounce(self, leftEdge, rightEdge, topEdge, bottomEdge):
        hit = False
        
        # If it hits the left edge or right edge, reverse velocity_x
        if ((self.rect.left < leftEdge) or (self.rect.right > rightEdge)):
            self.velocity_x = -self.velocity_x
            hit = True

        # If it hits the top edge or bottom edge, reverse velocity_y
        if ((self.rect.top < topEdge) or (self.rect.bottom > bottomEdge)):
            self.velocity_y = -self.velocity_y
            hit = True

        return hit

    def stick(self, leftEdge, rightEdge, topEdge, bottomEdge):
        # If it hits the left edge or right edge, stop movement
        if ((self.rect.left < leftEdge) or (self.rect.right > rightEdge)):
            self.velocity_x = 0
            self.velocity_y = 0
        # If it hits the top edge or bottom edge, stop movement
        if ((self.rect.top < topEdge) or (self.rect.bottom > bottomEdge)):
            self.velocity_x = 0
            self.velocity_y = 0



# Keystrokes
def keystrokes(sprite):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        sprite.velocity_x = sprite.speed
        sprite.velocity_y = 0
    elif keys[pygame.K_LEFT]:
        sprite.velocity_x = -sprite.speed
        sprite.velocity_y = 0
    elif keys[pygame.K_UP]:
        sprite.velocity_x = 0
        sprite.velocity_y = -sprite.speed
    elif keys[pygame.K_DOWN]:
        sprite.velocity_x = 0
        sprite.velocity_y = sprite.speed
    elif keys[pygame.K_SPACE]:
        sprite.speed += 1

    if sprite.speed > 5:
        sprite.speed = 1



def main():
    pygame.init()

    # Screen --- the Main Window where sprites are drawn
    screen_width = 600
    screen_height = 600
    background_color = myColors("white")   # (255, 255, 255)
    screen = pygame.display.set_mode([screen_width, screen_height])

    title = "Kinetic Theory of Matter"
    pygame.display.set_caption(title)

    # Time
    frames_per_second = 30
    clock = pygame.time.Clock()

    # Groups
    allSprites = pygame.sprite.Group()
    widgetGroup = pygame.sprite.Group()
    
    # Temperature
    # --- the speed of the particles
    temperature = 10

    # Pressure
    # --- the number of collisions with walls
    pressure = 0
    
    # Moles
    # --- the number of particles
    moles = 25
    
    # Volume
    # --- the amount of space for the particles
    tank_width = 500
    tank_height = 300

##############
    # SPRITES
    
    for i in range(moles):
        x = random.randint(((screen_width/2) - (tank_width/4)), ((screen_width/2) + (tank_width/4)))
        y = random.randint(((screen_height/2) - (tank_height/4)), ((screen_height/2) + (tank_height/4)))
        w = 10
        h = 10
        color = random.choice(["red"])
        ball = Ball(x, y, w, h, color)
        ball.velocity_x = random.randint(-temperature, temperature)
        ball.velocity_y = random.randint(-temperature, temperature)
        allSprites.add(ball)

    w, h = 600, 25
    text = "Time"
    x, y = 0, 0
    widg_time = MyButton(screen, text, x, y, w, h)
    widgetGroup.add(widg_time)

    text = "Pressure"
    x, y = 0, h
    widg_pressure = MyButton(screen, text, x, y, w, h)
    widgetGroup.add(widg_pressure)
    
    text = "Temperature = %d K" % (temperature)
    x, y = 0, 2*h
    widg_temperature = MyButton(screen, text, x, y, w, h)
    widgetGroup.add(widg_temperature)

    text = "Moles = %d" % (moles)
    x, y = 0, 3*h
    widg_moles = MyButton(screen, text, x, y, w, h)
    widgetGroup.add(widg_moles)

    
    

##############
    # Game Loop

    running_time = 0
    
    gameOver = False
    while not gameOver:

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
                pygame.quit()

        # Bouncing off the Wall
        for ball in allSprites:
            leftEdge = screen_width/2 - tank_width/2
            rightEdge = screen_width/2 + tank_width/2
            topEdge = screen_height/2 - tank_height/2
            bottomEdge = screen_height/2 + tank_height/2
            hit = ball.bounce(leftEdge, rightEdge, topEdge, bottomEdge)

            if hit:
                pressure += 1


        text = "Pressure = %d" % (pressure)
        widg_pressure.changeText(text)

        text = "Time = %d" % (running_time/frames_per_second)
        widg_time.changeText(text)
        
        # Clear the Screen
        screen.fill(background_color)

        pygame.draw.rect(screen, (0,0,0), (leftEdge, topEdge, tank_width, tank_height), 9)

        # Drawing
        allSprites.draw(screen)       ### SPRITE DRAWINGS

        # Update
        allSprites.update()           ### SPRITE UPDATE
        widgetGroup.update()

        # Next Frame
        pygame.display.update()
        clock.tick(frames_per_second)
        running_time += 1

    pygame.quit()

main()





