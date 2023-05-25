import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Shooter")

# Set up the time variables
clock = pygame.time.Clock()
bullet_timer = 0
bullet_delay = 1000  # Delay in milliseconds (1 second)

# Set up the colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (128, 128, 255)
PINK = (255, 128, 128)

# Set up the player
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - 2 * player_size
player_speed = 1
move_left = False
move_right = False

# Set up the bullets
bullet_size = 10
bullet_speed = 2
bullets = []

# Set up the enemy bullets
bullet_size_enemy = 11
bullet_speed_enemy = 1.6
bullets_enemy = []

# Set up the enemy
enemy_size = 50
enemy_x = random.randint(0, width - enemy_size)
enemy_y = 0
enemy_speed = 0.5

# Set up the lives
Hit_points = 10

# Set up the score
score = 0

def player(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, player_size, player_size))

def enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, enemy_size, enemy_size))

def fire_bullet(x, y):
    bullets.append([x, y])
    
def fire_bullet_enemy(x, y):
    bullets_enemy.append([x, y])
    

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    if (enemy_x <= bullet_x < enemy_x + enemy_size) and (enemy_y <= bullet_y < enemy_y + enemy_size):
        return True
    return False

def is_player_collision(player_x, player_y, enemy_x, enemy_y):
    if (player_x < enemy_x + enemy_size) and (player_x + player_size > enemy_x) and (player_y < enemy_y + enemy_size) and (player_y + player_size > enemy_y):
        return True
    return False

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_SPACE:
                bullet_x = player_x + player_size // 2 - bullet_size // 2
                bullet_y = player_y
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
    
    # Enemy bullet firing        
    current_time = pygame.time.get_ticks()
    if current_time - bullet_timer > bullet_delay:
        bullet_enemy_x = enemy_x + enemy_size // 2 - bullet_size_enemy // 2
        bullet_enemy_y = enemy_y + enemy_size
        fire_bullet_enemy(bullet_enemy_x, bullet_enemy_y)
        bullet_timer = current_time
    
    # Enemy bullet movement
    for bullet_enemy in bullets_enemy:
        bullet_enemy[1] += bullet_speed_enemy
        if bullet_enemy[1] > height:
            bullets_enemy.remove(bullet_enemy)
            
    # Collision detection with player and enemy bullets
    for bullet_enemy in bullets_enemy:
        if is_collision(player_x, player_y, bullet_enemy[0], bullet_enemy[1]):
            bullets_enemy.remove(bullet_enemy)
            Hit_points -= 1

    # Update player position based on movement flags
    if move_left:
        player_x -= player_speed
    if move_right:
        player_x += player_speed

    # Player boundary check
    if player_x < 0:
        player_x = 0
    elif player_x > width - player_size:
        player_x = width - player_size

    # Bullet movement
    for bullet in bullets:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Enemy movement
    enemy_y += enemy_speed
    if enemy_y > height:
        enemy_x = random.randint(0, width - enemy_size)
        enemy_y = 0

    # Collision detection with enemy
    for bullet in bullets:
        if is_collision(enemy_x, enemy_y, bullet[0], bullet[1]):
            bullets.remove(bullet)
            enemy_x = random.randint(0, width - enemy_size)
            enemy_y = 0
            score += 3
            Hit_points += 1

    # Collision detection with player
    if is_player_collision(player_x, player_y, enemy_x, enemy_y):
        enemy_x = random.randint(0, width - enemy_size)
        enemy_y = 0
        Hit_points -= 3

    player(player_x, player_y)
    enemy(enemy_x, enemy_y)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_size, bullet_size))
        
    # Draw enemy bullets
    for bullet_enemy in bullets_enemy:
        pygame.draw.rect(screen, PINK, (bullet_enemy[0], bullet_enemy[1], bullet_size_enemy, bullet_size_enemy))

    # Draw lives
    font = pygame.font.Font(None, 36)
    text = font.render("HP : " + str(Hit_points), True, WHITE)
    screen.blit(text, (10, 10))
    
    # Draw score
    if score == 69 or score == 420:
        font = pygame.font.Font(None, 30)
        text = font.render("Score: " + str(score) + "Nice!", True, RED)
        screen.blit(text, (10, 50))
    else:
        font = pygame.font.Font(None, 30)
        text = font.render("Score: " + str(score), True, BLUE)
        screen.blit(text, (10, 50))

    pygame.display.update()

    # Game over if lives reach 0
    if Hit_points < 0:
        running = False

# Quit the game
pygame.quit()
