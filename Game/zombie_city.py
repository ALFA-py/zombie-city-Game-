# ALFA, V1.0

import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1920, 1080
PLAYER_SPEED = 15
BULLET_SPEED = 40
ZOMBIE_SPEED = 10
ZOMBIE_SPAWN_DELAY = 30
WHITE = (255, 255, 255)
PLAYER_HEALTH = 100
SCORE = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ZOMBIE CITY")

background = pygame.image.load("multimedia/background.png")
player_image = pygame.image.load("multimedia/player.png")
player_image = pygame.transform.scale(player_image, (150, 150))
zombie_image = pygame.image.load("multimedia/zombie.png")
zombie_image = pygame.transform.scale(zombie_image, (150, 150))
start_button_image = pygame.image.load("multimedia/start.png")
start_button_image = pygame.transform.scale(start_button_image, (300, 150))
shot_sound = pygame.mixer.Sound("sonidos/disparo.wav")
zombie_hit_sound = pygame.mixer.Sound("sonidos/zombie_hit.wav")
player_hit_sound = pygame.mixer.Sound("sonidos/player_hit.wav")
pygame.mixer.music.load("sonidos/musica.wav")
pygame.mixer.music.play(-1)

player = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 150, 100, 100)

bullets = []
zombies = []

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

player_health = PLAYER_HEALTH
score = SCORE
zombie_speed = ZOMBIE_SPEED

def draw_background():
    screen.blit(background, (0, 0))

def handle_player_movement(keys):
    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED
    if player.x < 0:
        player.x = 0
    if player.x > WIDTH - player.width:
        player.x = WIDTH - player.width

def spawn_zombie():
    if random.randint(0, ZOMBIE_SPAWN_DELAY) == 0:
        zombie = pygame.Rect(random.randint(0, WIDTH - 100), 0, 100, 100)
        zombies.append(zombie)

def move_bullets():
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            bullets.remove(bullet)

def move_zombies():
    for zombie in zombies[:]:
        zombie.y += zombie_speed
        if zombie.y > HEIGHT:
            zombies.remove(zombie)

def check_collisions():
    global player_health, score, zombie_speed
    bullets_to_remove = []
    zombies_to_remove = []

    for bullet in bullets:
        for zombie in zombies:
            if bullet.colliderect(zombie):
                bullets_to_remove.append(bullet)
                zombies_to_remove.append(zombie)
                zombie_hit_sound.play()
                score += 10
                if score % 50 == 0:
                    zombie_speed += 1

    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)

    for zombie in zombies_to_remove:
        if zombie in zombies:
            zombies.remove(zombie)

    for zombie in zombies[:]:
        if zombie.colliderect(player):
            player_health -= 10
            player_hit_sound.play()
            zombies.remove(zombie)

def draw_elements():
    screen.fill(WHITE)
    draw_background()
    screen.blit(player_image, player)
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 0), bullet)
    for zombie in zombies:
        screen.blit(zombie_image, zombie)
    health_text = font.render(f"Salud: {player_health}", True, (255, 0, 0))
    score_text = font.render(f"Puntuación: {score}", True, (0, 0, 255))
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 50))

def save_high_score(score):
    try:
        with open("highscores.txt", "r") as file:
            high_scores = file.readlines()

        valid_scores = [int(line.strip().split(":")[-1]) for line in high_scores if line.strip().split(":")[-1].isdigit()]
        highest_score = max(valid_scores, default=0)

        if score > highest_score:
            with open("highscores.txt", "w") as file:
                file.write(f"Puntuación: {score}\n")
    except FileNotFoundError:
        with open("highscores.txt", "w") as file:
            file.write(f"Puntuación: {score}\n")

def get_high_score():
    try:
        with open("highscores.txt", "r") as file:
            scores = file.readlines()

        valid_scores = [int(line.strip().split(":")[-1]) for line in scores if line.strip().split(":")[-1].isdigit()]
        return max(valid_scores, default=0)
    except FileNotFoundError:
        return 0

def game_over():
    save_high_score(score)
    highest_score = get_high_score()
    screen.fill((0, 0, 0))

    game_over_text = font.render(f"¡Game Over! Puntuación: {score}", True, (255, 0, 0))
    highest_score_text = font.render(f"Puntuación más alta: {highest_score}", True, (0, 255, 0))
    instruction_text = font.render("Presiona 'R' para reiniciar o 'ESC' para salir", True, (255, 255, 255))

    screen.blit(game_over_text, (WIDTH // 2 - 250, HEIGHT // 2 - 100))
    screen.blit(highest_score_text, (WIDTH // 2 - 250, HEIGHT // 2 - 50))
    screen.blit(instruction_text, (WIDTH // 2 - 250, HEIGHT // 2))

    pygame.display.flip()
    pygame.time.wait(1000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def start_screen():
    screen.fill(WHITE)
    draw_background()
    button_rect = start_button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(start_button_image, button_rect.topleft)
    pygame.display.flip()
    
    wolf_sound = pygame.mixer.Sound("sonidos/wolf.wav")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    wolf_sound.play()
                    return

def main():
    global player_health, score, bullets, zombies, zombie_speed
    player_health = PLAYER_HEALTH
    score = SCORE
    bullets = []
    zombies = []
    zombie_speed = ZOMBIE_SPEED

    start_screen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shot_sound.play()
                    bullet_x = player.x + player.width - 20 
                    bullet_y = player.y + player.height // 2 - 5  
                    bullet = pygame.Rect(bullet_x, bullet_y, 5, 10)
                    bullets.append(bullet)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        keys = pygame.key.get_pressed()
        handle_player_movement(keys)
        spawn_zombie()
        move_bullets()
        move_zombies()
        check_collisions()
        draw_elements()

        if player_health <= 0:
            game_over()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()