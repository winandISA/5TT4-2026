import pygame
import math

pygame.init()

notCheckColor = (150, 150, 150)
checkColor = (0, 255, 0)
lastTime = [99, 99, 999]
bestTime = [99, 99, 999]
lap = 3
currentLap = 0

# --- Fenêtre ---
WIDTH, HEIGHT = 1024, 768
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Course F1")

# --- Chargement images ---
track = pygame.image.load("images/fond.png").convert()
track = pygame.transform.scale(track, (WIDTH, HEIGHT))

car_image = pygame.image.load("images/car.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (50, 70))

# --- Position de départ ---
car_x = 320
car_y = 640
car_angle = 180  # voiture vers le haut

speed = 0
max_speed = 6
acceleration = 0.1
friction = 0.05
rotation_speed = 3

# --- Chrono ---
start_time = pygame.time.get_ticks()
lap_time = start_time
font = pygame.font.SysFont(None, 32)

# --- Checkpoints (à ajuster selon ton circuit) ---
checkpoint0 = pygame.Rect(270, 595, 10, 100)
checkpoint1 = pygame.Rect(865, 225, 100, 10)
checkpoint2 = pygame.Rect(230, 390, 100, 10)

checkpoint1_passed = False
checkpoint2_passed = False


def rotate_center(image, angle):
    """Retourne une image tournée autour de son centre"""
    rotated = pygame.transform.rotate(image, angle)
    rect = rotated.get_rect(center=image.get_rect().center)
    return rotated, rect


clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Gestion des touches ---
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
        # friction
        if speed > 0:
            speed -= friction
        elif speed < 0:
            speed += friction

        if abs(speed) < 0.05:
            speed = 0

    # Rotation uniquement si on roule un peu
    if speed != 0:
        if keys[pygame.K_RIGHT]:
            car_angle += rotation_speed
        if keys[pygame.K_LEFT]:
            car_angle -= rotation_speed

    # --- Déplacement ---
    rad = math.radians(car_angle)
    car_x += math.cos(rad) * speed
    car_y += math.sin(rad) * speed

    if car_x <0 or car_x > WIDTH or car_y < 0 or car_y > HEIGHT:
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
            #            checkpoint0 = pygame.Rect(270, 595, 10, 100)
#            checkpoint1 = pygame.Rect(865, 225, 100, 10)
#            checkpoint2 = pygame.Rect(230, 390, 100, 10)

    # --- Affichage fond ---
    win.blit(track, (0, 0))

    # --- Affichage voiture ---
    rotated_car, rect = rotate_center(car_image, -car_angle)
    rect.center = (car_x, car_y)
    win.blit(rotated_car, rect.topleft)

    # --- Gestion des checkpoints ---
    car_center = rect.center

    if checkpoint1.collidepoint(car_center):
        checkpoint1_passed = True

    if checkpoint2.collidepoint(car_center) and checkpoint1_passed:
        checkpoint2_passed = True

    if checkpoint0.collidepoint(car_center) and checkpoint1_passed and checkpoint2_passed:
        checkpoint1_passed = False
        checkpoint2_passed = False

        elapsed_ms = pygame.time.get_ticks() - start_time
        total_seconds = elapsed_ms // 1000
        lastTime[2] = elapsed_ms % 1000
        lastTime[0] = total_seconds // 60
        lastTime[1] = total_seconds % 60
        if lastTime[0] < bestTime[0] or (lastTime[0] == bestTime[0] and lastTime[1] < bestTime[1]) or (lastTime[0] == bestTime[0] and lastTime[1] == bestTime[1] and lastTime[2] < bestTime[2]):
            bestTime[0] = lastTime[0]
            bestTime[1] = lastTime[1]
            bestTime[2] = lastTime[2]
        lap_time = pygame.time.get_ticks()
        currentLap += 1


    # (Option : si les deux sont passés, tu peux faire quelque chose :
    # if checkpoint1_passed and checkpoint2_passed:
    #     print("Tous les checkpoints passés !")

    # --- Dessin visuel des checkpoints (contour) ---
    pygame.draw.rect(win, notCheckColor , checkpoint0, 2)
    pygame.draw.rect(win, checkColor if checkpoint1_passed else notCheckColor, checkpoint1, 2)
    pygame.draw.rect(win, checkColor if checkpoint2_passed else notCheckColor, checkpoint2, 2)

    # --- Chrono ---
    elapsed_ms = pygame.time.get_ticks() - start_time
    total_seconds = elapsed_ms // 1000
    milliseconds = elapsed_ms % 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    time_text = font.render(f"Current Time:  {minutes:02d}:{seconds:02d}:{milliseconds} Last Time: {lastTime[0]:02d}:{lastTime[1]:02d}:{lastTime[2]:02d} Best Time :{bestTime[0]:02d}:{bestTime[1]:02d}:{bestTime[2]:02d}", True, (255, 255, 255))
    win.blit(time_text, (10, 10))

    lap_text = font.render(f"Lap {currentLap} on {lap}", True, (255, 255, 255))
    win.blit(lap_text, (10, 40))
    # --- Affichage état des checkpoints ---
    cp1_color = checkColor if checkpoint1_passed else notCheckColor
    cp2_color = checkColor if checkpoint2_passed else notCheckColor

    cp1_text = font.render("CP1", True, cp1_color)
    cp2_text = font.render("CP2", True, cp2_color)

    win.blit(cp1_text, (10, 70))
    win.blit(cp2_text, (60, 70))

    pygame.display.update()

pygame.quit()
