import pygame
import sys
import random
import math
import base64

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ENEMY_SPAWN_INTERVAL = 60  # Spawn a new enemy every 60 frames (1 second)
POWERUP_SPAWN_INTERVAL = 1200  # Spawn a power-up every 1200 frames (1 minute)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The game ever")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.health = 100
        self.level = 1  # Player starts at level 1
        self.bullet_radius = 10
        self.bullet_cooldown = 20  # Cooldown between bullet firing (frames)
        self.bullet_timer = 0
        self.enemies_killed = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Fire bullets when pressing 'F' and the cooldown is over
        if keys[pygame.K_f] and self.bullet_timer <= 0:
            self.shoot_bullets()
            self.bullet_timer = self.bullet_cooldown
        elif self.bullet_timer > 0:
            self.bullet_timer -= 1

        # Keep player within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

    def shoot_bullets(self):
        for angle in range(0, 360, 30):
            radians = math.radians(angle)
            bullet = Bullet(self.rect.centerx, self.rect.centery, radians, self.level)
            bullets.add(bullet)
            all_sprites.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, radians, level):
        super().__init__()
        self.level = level
        damage_multiplier = [1, 2, 3, 4, 5]
        colors = [RED, GREEN, BLUE, ORANGE, BLACK]
        self.damage = damage_multiplier[level - 1]
        self.color = colors[level - 1]

        self.image = pygame.Surface((10, 10))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.radians = radians

    def update(self):
        dx = math.cos(self.radians) * self.speed
        dy = math.sin(self.radians) * self.speed
        self.rect.x += dx
        self.rect.y += dy
        if not (0 <= self.rect.x < SCREEN_WIDTH) or not (0 <= self.rect.y < SCREEN_HEIGHT):
            self.kill()  # Remove bullets that go off-screen

# Power-up class
class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

    def update(self):
        # Check for collision with the player
        if pygame.sprite.collide_rect(player, self):
            player.health += 25  # Increase player's health
            self.kill()  # Remove the power-up



# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.level = random.randint(1, 5)
        damage_multiplier = [1, 2, 3, 4, 5]
        colors = [RED, GREEN, BLUE, ORANGE, BLACK]
        self.damage = damage_multiplier[self.level - 1]
        self.color = colors[self.level - 1]

        self.image = pygame.Surface((30, 30))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = 2

    def update(self):
        # Move towards the player
        if player.rect.centerx < self.rect.centerx:
            self.rect.x -= self.speed
        elif player.rect.centerx > self.rect.centerx:
            self.rect.x += self.speed
        if player.rect.centery < self.rect.centery:
            self.rect.y -= self.speed
        elif player.rect.centery > self.rect.centery:
            self.rect.y += self.speed

        # Check for collision with the player
        if pygame.sprite.collide_rect(player, self):
            player.health -= self.damage  # Player takes damage based on enemy's level
            self.kill()  # Enemy dies when it hits the player

# Create a player instance
player = Player()

# Create groups for all sprites, bullets, enemies, and power-ups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
all_sprites.add(player)

# Game variables
enemy_spawn_timer = 0
powerup_spawn_timer = 0

# Inside the game loop

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    # Update

    all_sprites.update()

    # Spawn enemies at regular intervals

    enemy_spawn_timer += 1

    if enemy_spawn_timer >= ENEMY_SPAWN_INTERVAL:

        new_enemy = Enemy()

        enemies.add(new_enemy)

        all_sprites.add(new_enemy)

        enemy_spawn_timer = 0

    # Spawn power-ups at regular intervals

    powerup_spawn_timer += 1

    if powerup_spawn_timer >= POWERUP_SPAWN_INTERVAL:

        new_powerup = Powerup()

        powerups.add(new_powerup)

        all_sprites.add(new_powerup)

        powerup_spawn_timer = 0

    # Handle enemy attacks

    for enemy in enemies:

        if pygame.sprite.collide_rect(player, enemy):

            player.health -= enemy.damage  # Player takes damage based on the enemy's level

            enemy.kill()  # Enemy dies when it hits the player

    # Check for game over

    if player.health <= 0:

        running = False  # Game over if player's health reaches 0

    # Handle player bullet collisions

    for bullet in bullets:

        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)

        if hit_enemies:

            player.enemies_killed += len(hit_enemies)

            bullet.kill()

            # Check for level up based on the number of kills

            if player.enemies_killed >= 250:

                player.level = 5

            elif player.enemies_killed >= 150:

                player.level = 4

            elif player.enemies_killed >= 100:

                player.level = 3

            elif player.enemies_killed >= 50:

                player.level = 2

            elif player.enemies_killed >= 20:

                player.level = 1

    # Draw

    screen.fill(WHITE)

    all_sprites.draw(screen)

    # Display player health, number of enemies, and number of power-ups

    font = pygame.font.Font(None, 36)

    health_text = font.render(f"Health: {player.health}", True, RED)

    enemies_text = font.render(f"Enemies: {player.enemies_killed}", True, RED)

    powerups_text = font.render(f"Power-ups: {len(powerups)}", True, GREEN)

    level_text = font.render(f"Level: {player.level}", True, BLUE)

    screen.blit(health_text, (10, 10))

    screen.blit(enemies_text, (10, 50))

    screen.blit(powerups_text, (10, 90))

    screen.blit(level_text, (10, 130))

    pygame.display.flip()

# Game over screen

game_over_font = pygame.font.Font(None, 72)

game_over_text = game_over_font.render("Game Over", True, RED)

screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

pygame.display.flip()

# Delay before quitting

pygame.time.delay(2000)

# Quit Pygame

pygame.quit()

sys.exit()
