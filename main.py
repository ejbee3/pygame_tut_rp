import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_a,
    K_d,
    K_s,
    K_w,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

LIGHT_BROWN = (234, 221, 202)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.dir = {'right' : pygame.image.load("img/roach_right.png").convert(), 'left' : pygame.image.load("img/roach_left.png").convert(),
                    'up' : pygame.image.load("img/roach_up.png").convert(), 'down' : pygame.image.load("img/roach_down.png").convert()}
        self.rect = self._animate(self.dir['right'], (100, 100))
        self.current_dir = 'right'
    
    # change image based on direction of movement
    def _animate(self, dir, old_center):
        self.surf = dir
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        return self.surf.get_rect(center=old_center)


    def update(self, pressed_keys):
        # UP
        up = pressed_keys[K_w]
        if up and self.current_dir != 'up':
            self.rect = self._animate(self.dir['up'], self.rect.center)
            self.current_dir = 'up'
            self.rect.move_ip(0, -15)
        elif up:
            self.rect.move_ip(0, -15)
        # DOWN
        down = pressed_keys[K_s]
        if down and self.current_dir != 'down':
            self.rect = self._animate(self.dir['down'], self.rect.center)
            self.current_dir = 'down'
            self.rect.move_ip(0, 15)
        elif down:
            self.rect.move_ip(0, 15)
        # LEFT
        left = pressed_keys[K_a]
        if left and self.current_dir != 'left':
            self.rect = self._animate(self.dir['left'], self.rect.center)
            self.current_dir = 'left'
            self.rect.move_ip(-15, 0)
        elif left:
            self.rect.move_ip(-15, 0)
        # RIGHT
        right = pressed_keys[K_d]
        if right and self.current_dir != 'right':
            self.rect = self._animate(self.dir['right'], self.rect.center)
            self.current_dir = 'right'
            self.rect.move_ip(15, 0)
        elif right:
            self.rect.move_ip(15, 0)

         # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = {'up': pygame.image.load("img/hammer_up.png").convert(), 'down' : pygame.image.load("img/hammer_down.png").convert()}
        self.surf = self.image['up']
        self.toggle = False
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(7, 15)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
    
    def animate(self, new_img, old_center):
        self.surf = new_img
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        return self.surf.get_rect(center=old_center)

pygame.mixer.init()

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

crunch_sound = pygame.mixer.Sound("sounds/crunch.ogg")

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

ANIMATEENEMY = pygame.USEREVENT + 2
pygame.time.set_timer(ANIMATEENEMY, 500)

player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
    # look at every event in the queue
    for event in pygame.event.get():
        # did the user hit a key?
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ANIMATEENEMY:
            for entity in enemies:
                if not entity.toggle:
                    entity.rect = entity.animate(entity.image['down'], entity.rect.center)
                else:
                    entity.rect = entity.animate(entity.image['up'], entity.rect.center)
                entity.toggle = not entity.toggle

                    
    
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update enemy position
    enemies.update()
    
    screen.fill(LIGHT_BROWN)

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        crunch_sound.play()
        pygame.time.wait(2000)
        player.kill()
        running = False

    pygame.display.flip()
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)
