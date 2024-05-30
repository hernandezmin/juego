import pygame
import sys
import random

pygame.init()

# Definimos algunas constantes
WIDTH, HEIGHT = 640, 480
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego del cuadrado asesino")
BACKGROUND_COLOR = (0, 0, 0)
SQUARE_SIZE = 50
SPEED = 5
BULLET_SPEED = 7
CHARACTER_SIZE = 20

# Variables de estado del juego
def reset_game():
    global x, y, characters_positions, characters_speed, characters_alive, bullets, alive, score
    x = WIDTH // 2 - SQUARE_SIZE // 2
    y = HEIGHT // 2 - SQUARE_SIZE // 2
    characters_positions = [(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20)) for _ in range(len(characters))]
    characters_speed = [random.randint(1, 3) for _ in range(len(characters))]
    characters_alive = [True for _ in range(len(characters))]
    bullets = []
    alive = True
    score = 0

# Inicializar variables del juego
characters = ["A", "B", "C", "D", "E"]
total_collisions = 0
bullet_size = 10
reset_game()

# Función para dibujar los caracteres en pantalla
def draw_characters():
    for i, char in enumerate(characters):
        if characters_alive[i]:
            pygame.draw.rect(SCREEN, (255, 255, 255), (characters_positions[i][0], characters_positions[i][1], CHARACTER_SIZE, CHARACTER_SIZE))
            font = pygame.font.Font(None, 36)
            text = font.render(char, True, (255, 255, 255))
            SCREEN.blit(text, (characters_positions[i][0] + CHARACTER_SIZE // 4, characters_positions[i][1] - CHARACTER_SIZE // 4))

# Función para mover los caracteres
def move_characters():
    for i in range(len(characters)):
        if characters_alive[i]:
            characters_positions[i] = (characters_positions[i][0], characters_positions[i][1] + characters_speed[i])
            if characters_positions[i][1] > HEIGHT:
                characters_positions[i] = (random.randint(0, WIDTH - 20), random.randint(-200, -20))
                characters_speed[i] = random.randint(1, 3)

# Función para detectar colisiones entre las balas y los caracteres
def check_bullet_collisions():
    global score
    for bullet in bullets[:]:
        for i in range(len(characters)):
            if characters_alive[i]:
                if bullet[0] < characters_positions[i][0] + CHARACTER_SIZE and \
                   bullet[0] + bullet_size > characters_positions[i][0] and \
                   bullet[1] < characters_positions[i][1] + CHARACTER_SIZE and \
                   bullet[1] + bullet_size > characters_positions[i][1]:
                    characters_alive[i] = False
                    bullets.remove(bullet)
                    characters_positions[i] = (random.randint(0, WIDTH - 20), random.randint(-200, -20))
                    characters_speed[i] = random.randint(1, 3)
                    score += 1
                    break

# Función para detectar colisiones entre el cuadrado y los caracteres
def check_collisions():
    global alive, total_collisions
    for i in range(len(characters)):
        if characters_alive[i]:
            if x < characters_positions[i][0] + CHARACTER_SIZE and \
               x + SQUARE_SIZE > characters_positions[i][0] and \
               y < characters_positions[i][1] + CHARACTER_SIZE and \
               y + SQUARE_SIZE > characters_positions[i][1]:
                alive = False
                total_collisions += 1
                break

# Función para dibujar los disparos
def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(SCREEN, (0, 255, 0), (bullet[0], bullet[1], bullet_size, bullet_size))

# Función para mover los disparos
def move_bullets():
    for bullet in bullets[:]:
        bullet[1] -= BULLET_SPEED
        if bullet[1] < 0:
            bullets.remove(bullet)

# Función para dibujar el contador de puntos y colisiones
def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Puntos: {score}", True, (255, 255, 255))
    collisions_text = font.render(f"Colisiones: {total_collisions}", True, (255, 255, 255))
    SCREEN.blit(score_text, (10, 10))
    SCREEN.blit(collisions_text, (10, 50))

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and alive:
                bullets.append([x + SQUARE_SIZE // 2 - bullet_size // 2, y])
            elif event.key == pygame.K_s and not alive:
                reset_game()

    if alive:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            y -= SPEED
        if keys[pygame.K_DOWN]:
            y += SPEED
        if keys[pygame.K_LEFT]:
            x -= SPEED
        if keys[pygame.K_RIGHT]:
            x += SPEED

        # Limitamos las posiciones del cuadrado dentro de la pantalla
        x = max(0, min(x, WIDTH - SQUARE_SIZE))
        y = max(0, min(y, HEIGHT - SQUARE_SIZE))

        SCREEN.fill(BACKGROUND_COLOR)

        # Movemos y dibujamos los caracteres
        move_characters()
        draw_characters()

        # Movemos y dibujamos los disparos
        move_bullets()
        draw_bullets()

        # Dibujamos el cuadrado rojo
        pygame.draw.rect(SCREEN, (255, 0, 0), (x, y, SQUARE_SIZE, SQUARE_SIZE))

        # Revisamos colisiones
        check_bullet_collisions()
        check_collisions()

    else:
        SCREEN.fill(BACKGROUND_COLOR)
        font = pygame.font.Font(None, 74)
        text = font.render("¡Has muerto!", True, (255, 0, 0))
        SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    # Dibujamos el contador de puntos y colisiones
    draw_score()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
