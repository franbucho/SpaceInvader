import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 600, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Jugador
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - 2 * player_size
player_speed = 5
player_bullet_speed = 7
player_fire_power = 1

# Nuevos cañones
player_cannons = [
    {'x': player_x, 'y': player_y, 'offset': -15},
    {'x': player_x, 'y': player_y, 'offset': 15}
]

# Enemigos
enemy_size = 30
enemy_speed = 2
enemy_spawn_rate = 30
enemies = []

# Disparos
bullet_size = 5
bullet_speed = 7
bullets = []

# Vidas
lives = 3

# Puntuación
score = 0
top_score = 0
font = pygame.font.Font(None, 36)

# Fondo espacial
stars = [(random.randint(0, width), random.randint(0, height)) for _ in range(50)]

def create_enemies():
    for _ in range(10 + score // 5):
        enemy_x = random.randint(0, width - enemy_size)
        enemy_y = random.randint(50, 150)
        enemies.append([enemy_x, enemy_y])

def draw_player():
    for cannon in player_cannons:
        pygame.draw.rect(screen, white, [cannon['x'] + cannon['offset'], cannon['y'], player_size, player_size])

def draw_enemy(x, y):
    pygame.draw.rect(screen, red, [x, y, enemy_size, enemy_size])

def draw_bullet(x, y):
    pygame.draw.rect(screen, white, [x, y, bullet_size, bullet_size])

def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, white, star, 1)

def draw_score():
    score_text = font.render(f"Score: {score}   Lives: {lives}   Top Score: {top_score}", True, white)
    screen.blit(score_text, (10, 10))

def draw_restart_button():
    pygame.draw.rect(screen, white, [width // 2 - 75, height // 2 - 25, 150, 50])
    restart_text = font.render("Restart", True, black)
    screen.blit(restart_text, (width // 2 - 40, height // 2 - 15))

def restart_game():
    global player_x, player_y, player_cannons, enemies, bullets, lives, score
    player_x = width // 2 - player_size // 2
    player_y = height - 2 * player_size
    player_cannons = [
        {'x': player_x, 'y': player_y, 'offset': -15},
        {'x': player_x, 'y': player_y, 'offset': 15}
    ]
    enemies.clear()
    bullets.clear()
    lives = 3
    score = 0
    create_enemies()

# Bucle principal del juego
running = True
create_enemies()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if width // 2 - 75 <= mouse_x <= width // 2 + 75 and height // 2 - 25 <= mouse_y <= height // 2 + 25:
                restart_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_cannons[0]['x'] > 0:
        for cannon in player_cannons:
            cannon['x'] -= player_speed
    if keys[pygame.K_RIGHT] and player_cannons[1]['x'] < width - player_size:
        for cannon in player_cannons:
            cannon['x'] += player_speed
    if keys[pygame.K_SPACE]:
        for cannon in player_cannons:
            bullets.append([cannon['x'] + cannon['offset'] + player_size // 2 - bullet_size // 2, cannon['y']])

    # Mover enemigos
    new_enemies = []
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > height:
            lives -= 1
            if lives <= 0:
                running = False
            enemy[0] = random.randint(0, width - enemy_size)
            enemy[1] = random.randint(50, 150)
        else:
            new_enemies.append(enemy)
    
    enemies = new_enemies

    # Generar nuevos enemigos
    if random.randint(0, enemy_spawn_rate) == 0:
        create_enemies()

    # Mover balas
    new_bullets = []
    for bullet in bullets:
        bullet[1] -= bullet_speed
        if bullet[1] >= 0:
            new_bullets.append(bullet)

    bullets = new_bullets

    # Colisiones
    new_enemies = []
    for enemy in enemies:
        hit = False
        new_bullets = []
        for bullet in bullets:
            if enemy[0] < bullet[0] < enemy[0] + enemy_size and enemy[1] < bullet[1] < enemy[1] + enemy_size:
                score += 1
                if score > top_score:
                    top_score = score
                hit = True
            else:
                new_bullets.append(bullet)
        
        if not hit:
            new_enemies.append(enemy)

    enemies = new_enemies
    bullets = new_bullets

    # Dibujar elementos en la pantalla
    screen.fill(black)
    draw_stars()
    draw_player()
    for enemy in enemies:
        draw_enemy(enemy[0], enemy[1])
    for bullet in bullets:
        draw_bullet(bullet[0], bullet[1])
    draw_score()

    if lives <= 0:
        draw_restart_button()

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
