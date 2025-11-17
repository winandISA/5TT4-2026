import pygame
import math

pygame.init()

notCheckColor = (150, 150, 150)
checkColor = (0, 255, 0)
lastTime = [99, 99, 999]
bestTime = [99, 99, 999]
lap = 3
currentLap = 0

# --- Nouveaux éléments pour le menu ---
state = "menu"
font_big = pygame.font.SysFont(None, 60)
start_button = pygame.Rect(412, 500, 200, 70)

bestRace = [99, 99, 999]
lastRace = [99, 99, 999]

# --- Fenêtre ---
WIDTH, HEIGHT = 1024, 768
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Course F1")

# --- Chargement images ---
track = pygame.image.load("images/fond.png").convert()
track = pygame.transform.scale(track, (WIDTH, HEIGHT))

car_image = pygame.image.load("images/car.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (50, 70))

logo = pygame.image.load("images/carFace.png").convert_alpha()
logo = pygame.transform.smoothscale(logo, (300, 200))

# --- Position de départ ---
car_x = 320
car_y = 640
car_angle = 180

speed = 0
max_speed = 6
acceleration = 0.1
friction = 0.05
rotation_speed = 3

# --- Chrono ---
start_time = pygame.time.get_ticks()
lap_time = start_time
font = pygame.font.SysFont(None, 32)

# --- Checkpoints ---
checkpoint0 = pygame.Rect(270, 595, 10, 100)
checkpoint1 = pygame.Rect(865, 225, 100, 10)
checkpoint2 = pygame.Rect(230, 390, 100, 10)

checkpoint1_passed = False
checkpoint2_passed = False


def rotate_center(image, angle):
    rotated = pygame.transform.rotate(image, angle)
    rect = rotated.get_rect(center=image.get_rect().center)
    return rotated, rect


clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60)

    # ================================
    # --- ÉCRAN DE DÉMARRAGE ---
    # ================================
    if state == "menu":

        win.fill((10, 10, 40))

        logo_rect = logo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        win.blit(logo, logo_rect.topleft)

        title = font_big.render("Course F1", True, (255, 255, 255))
        win.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        # Affichage des records
        bt = bestTime
        br = bestRace

        rec1 = font.render(f"Meilleur Tour : {l[0]:02d}:{bt[1]:02d}:{bt[2]:03d} Temps  Total : {br[0]:02d}:{br[1]:02d}:{br[2]:03d}", True, (255, 255, 255))
        rec2 = font.render(f"Record Tour   : {bt[0]:02d}:{bt[1]:02d}:{bt[2]:03d} Record Total : {br[0]:02d}:{br[1]:02d}:{br[2]:03d}", True, (255, 255, 255))

        win.blit(rec1, (WIDTH//2 - rec1.get_width()//2, 250))
        win.blit(rec2, (WIDTH//2 - rec2.get_width()//2, 290))

        # Bouton START
        mouse_pos = pygame.mouse.get_pos()
        color = (0, 180, 0) if start_button.collidepoint(mouse_pos) else (0, 130, 0)

        pygame.draw.rect(win, color, start_button, border_radius=10)
        pygame.draw.rect(win, (255, 255, 255), start_button, 3, border_radius=10)

        start_txt = font_big.render("START", True, (255, 255, 255))
        win.blit(start_txt, (start_button.centerx - start_txt.get_width()//2,
                             start_button.centery - start_txt.get_height()//2))

        # Gestion clic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    # Reset complet pour un nouveau départ
                    state = "pyFiles"
                    currentLap = 0
                    checkpoint1_passed = False
                    checkpoint2_passed = False
                    speed = 0
                    car_x = 320
                    car_y = 640
                    car_angle = 180
                    start_time = pygame.time.get_ticks()
                    lap_time = start_time

        pygame.display.update()
    else:
        # ================================
        # --- MODE JEU (ton code intact) ---
        # ================================

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            speed += acceleration
            if speed > max_speed:
                speed = max_speed
        elif keys[pygame.K_DOWN]:
            speed -= acceleration
            if speed < -max_speed / 2:
                speed = -max_speed / 2
        else:
            if speed > 0:
                speed -= friction
            elif speed < 0:
                speed += friction
            if abs(speed) < 0.05:
                speed = 0

        if speed != 0:
            if keys[pygame.K_RIGHT]:
                car_angle += rotation_speed
            if keys[pygame.K_LEFT]:
                car_angle -= rotation_speed

        rad = math.radians(car_angle)
        car_x += math.cos(rad) * speed
        car_y += math.sin(rad) * speed

        if car_x < 0 or car_x > WIDTH or car_y < 0 or car_y > HEIGHT:
            speed = 0
            if checkpoint2_passed:
                car_x = 290
                car_y = 370
                car_angle = 90
            elif checkpoint1_passed:
                car_x = 925
                car_y = 205
                car_angle = 90
            else:
                car_x = 320
                car_y = 640
                car_angle = 180

        win.blit(track, (0, 0))

        rotated_car, rect = rotate_center(car_image, -car_angle)
        rect.center = (car_x, car_y)
        win.blit(rotated_car, rect.topleft)

        car_center = rect.center

        if checkpoint1.collidepoint(car_center):
            checkpoint1_passed = True

        if checkpoint2.collidepoint(car_center) and checkpoint1_passed:
            checkpoint2_passed = True

        # --- Passage ligne de départ ---
        if checkpoint0.collidepoint(car_center) and checkpoint1_passed and checkpoint2_passed:
            checkpoint1_passed = False
            checkpoint2_passed = False

            # Temps du tour
            elapsed_ms = pygame.time.get_ticks() - lap_time
            total_seconds = elapsed_ms // 1000
            lastTime = [
                total_seconds // 60,
                total_seconds % 60,
                elapsed_ms % 1000
            ]

            # Record du tour
            if lastTime < bestTime:
                bestTime = lastTime.copy()

            lap_time = pygame.time.get_ticks()
            currentLap += 1

            # --- Fin de course ---
            if currentLap == lap:
                # Calcul du temps total
                race_ms = pygame.time.get_ticks() - start_time
                lastRace = [
                    race_ms//60000,
                    (race_ms//1000) % 60,
                    race_ms % 1000
                ]

                if lastRace < bestRace:
                    bestRace = lastRace.copy()

                state = "menu"
                continue

        pygame.draw.rect(win, notCheckColor, checkpoint0, 2)
        pygame.draw.rect(win, checkColor if checkpoint1_passed else notCheckColor, checkpoint1, 2)
        pygame.draw.rect(win, checkColor if checkpoint2_passed else notCheckColor, checkpoint2, 2)

        elapsed_ms = pygame.time.get_ticks() - start_time
        total_seconds = elapsed_ms // 1000
        milliseconds = elapsed_ms % 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        time_text = font.render(
            f"Current: {minutes:02d}:{seconds:02d}:{milliseconds:03d} "
            f"Last: {lastTime[0]:02d}:{lastTime[1]:02d}:{lastTime[2]:03d} "
            f"Best: {bestTime[0]:02d}:{bestTime[1]:02d}:{bestTime[2]:03d}",
            True, (255, 255, 255)
        )
        win.blit(time_text, (10, 10))

        lap_text = font.render(f"Lap {currentLap} / {lap}", True, (255, 255, 255))
        win.blit(lap_text, (10, 40))

        pygame.display.update()

pygame.quit()
