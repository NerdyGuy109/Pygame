
import pygame



class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__()

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
        self.imageName = "toaster.jpg"

        # Load an image onto the surface
        self.image = pygame.image.load(self.imageName)
        self.image = pygame.transform.scale(self.image, (20, 20))
        pygame.draw.rect(self.image, self.color, [self.x, self.y, self.w, self.h])

        # Rect ***
        self.rect = self.image.get_rect()

        # Position of the Sprite
        self.rect.x = self.x
        self.rect.y = self.y

        # Velocity of the Sprite
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        self.move()
        
    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        
    
    


def main():
    pygame.init()

    # screen
    screen_width = 600
    screen_height = 600
    screen_size = [screen_width, screen_height]
    bg_color = (0,0,0)
    screen = pygame.display.set_mode(screen_size)

    # title
    title = "Avoid the Toaster"
    pygame.display.set_caption(title)

    # clock
    fps = 30
    clock = pygame.time.Clock()

    # groups
    allSprites = pygame.sprite.Group()

    # sprites
    x, y = screen_width/2, screen_height/2
    w, h = 50, 50
    color = (255,255,0)
    hero = Entity(x, y, w, h, color)
    
    # Game Loop
    gameover = False

    while not gameover:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
                pygame.quit()

        # Keystrokes

        # Game Logic (collision detection, scoring)

        # Clear the Screen
        screen.fill(bg_color)

        # Drawing
        allSprites.draw(screen)

        # Updates
        allSprites.update()

        # Next Frame
        pygame.display.update()
        clock.tick(fps)

main()
        
               

        

    
    
