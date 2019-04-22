

import pygame, random, math

# Colors
def myColors(color):
    D = {
        "white": (255, 255, 255),
        "black": (0,0,0),
        "red": (255,0,0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255)
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
        self.checkForMouse()
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


# Keystrokes
def keystrokes(sprite):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        sprite.velocity_x = 5
    elif keys[pygame.K_LEFT]:
        sprite.velocity_x = -5
    else:
        pass

    if keys[pygame.K_UP]:
        sprite.velocity_y = -20
    if keys[pygame.K_DOWN]:
        sprite.velocity_y = 1
    if keys[pygame.K_SPACE]:
        pass
    if keys[pygame.K_TAB]:
        pass
    if keys[pygame.K_q]:
        pass
    if keys[pygame.K_w]:
        pass


# Class
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        super().__init__()

        sprite_width = w
        sprite_height = h

        self.sprite_color = color  # text ("black")
        self.colorCode = myColors(self.sprite_color)

        self.image = pygame.Surface([sprite_width, sprite_height])
        self.image.fill(self.colorCode)

##      self.imageName = str(self.sprite_color + "_snowball.jpg")
##      self.image = pygame.image.load(self.imageName)
##      self.image = pygame.transform.scale(self.image, (20, 20))
##      pygame.draw.rect(self.image, self.colorCode, [x, y, sprite_width, sprite_height])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        self.move()

    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def stop(self):
        self.velocity_x = 0
        self.velocity_y = 0

    def collisions(self):
        if self.rect.x < 0:
            self.stop()
        elif self.rect.x > screen_width:
            self.stop()
            
        if self.rect.y < 0:
            self.stop()
        elif self.rect.y > screen_height:
            self.stop()




class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        super().__init__()

        self.w = w
        self.h = h

        self.sprite_color = color  # text ("black")
        self.colorCode = myColors(self.sprite_color)

        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(self.colorCode)

##        self.imageName = str(self.sprite_color + "_snowball.jpg")
##        self.image = pygame.image.load(self.imageName)
##        self.image = pygame.transform.scale(self.image, (20, 20))

##        pygame.draw.rect(self.image, self.colorCode, [x, y, sprite_width, sprite_height])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vertex = 0

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.updateVelocity()
        self.updatePosition()
#        self.collisions()
        self.numSeconds += float(1/600)

    def collisions(self):
        if self.rect.x < 0 or self.rect.x > screen_width:
            self.kill()
        if self.rect.y > screen_height:
            self.kill()

    def throwSettings(self, x0, y0, vx0, vy0):
        self.rect.x = x0
        self.rect.y = y0
        self.velocity_x = vx0
        self.velocity_y = vy0
        self.acceleration_x = 0
        self.acceleration_y = 10
        self.numSeconds = 0
        self.startVelocityX = vx0
        self.startVelocityY = vy0


    def updateVelocity(self):
        self.velocity_x = self.velocity_x + self.acceleration_x * self.numSeconds
        self.velocity_y = self.velocity_y + self.acceleration_y * self.numSeconds

    def updatePosition(self):
        self.rect.x = self.rect.x + self.velocity_x * self.numSeconds + (0.5) * self.acceleration_x * (self.numSeconds) * (self.numSeconds)
        self.rect.y = self.rect.y + self.velocity_y * self.numSeconds + (0.5) * self.acceleration_y * (self.numSeconds) * (self.numSeconds)

    def findVertex(self):
        self.vertex = (-self.startVelocityY / (self.acceleration_y))

    def getInfo(self):
        self.findVertex()
        return (self.rect.x, self.rect.y, self.velocity_x, self.velocity_y, self.vertex)





def printMouse():
    mouse = pygame.mouse.get_pos()
    print(mouse)


def quitGame():
    pygame.quit()


# Main
def main():
    pygame.init()

    # Screen --- the Main Window where sprites are drawn
    screen_width = 600
    screen_height = 600
    background_color = myColors("white")
    screen = pygame.display.set_mode([screen_width, screen_height])

    # Title
    title = "Name of Game"
    pygame.display.set_caption(title)

    # Clock Settings
    frames_per_second = 30
    clock = pygame.time.Clock()

    # Sprite Groups
    all_sprites = pygame.sprite.Group()

    # Main Character --- Hero
    x, y = 200, 200
    w, h = 50, 50
    color = "blue"
    hero = Projectile(x, y, w, h, color)
    hero.throwSettings(x, y, 0, 0)
    all_sprites.add(hero)

    # Widgets
    x, y = 0, 0
    w, h = 100, 50
    text = "Quit"
    quit_button = MyButton(screen, text, x, y, w, h, action=quitGame)
    all_sprites.add(quit_button)

    x, y = 0, 50
    w, h = 100, 50
    text = "Print"
    quit_button = MyButton(screen, text, x, y, w, h, action=printMouse)
    all_sprites.add(quit_button)
    
    # Game Loop
    gameOver = False
    while not gameOver:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
                pygame.quit()

        # Game Logic
        keystrokes(hero)

        if hero.rect.y > screen_height - hero.h:
            hero.rect.y = screen_height - hero.h

        # Clear the Screen
        screen.fill(background_color)

        # Drawing
        all_sprites.draw(screen)
        
        # Next Frame
        all_sprites.update()
        pygame.display.update()
        clock.tick(frames_per_second)


main()


