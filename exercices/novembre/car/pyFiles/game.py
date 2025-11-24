import pygame
import math
from .config import *

def run_game(win):
    track = pygame.image.load("images/fond.png").convert()
    track = pygame.transform.scale(track, (WIDTH, HEIGHT))

    car_image = pygame.image.load("images/car.png").convert_alpha()
    car_image = pygame.transform.smoothscale(car_image, (50, 70))

    font = pygame.font.SysFont(None, 32)

    start_time = pygame.time.get_ticks()
    lap_time = start_time

    car_x = 320
    car_y = 640
    car_angle = 180

    speed = 0
    max_speed = 6
    acceleration = 0.1
    friction = 0.05
    rotation_speed = 3

    checkpoint0 = pygame.Rect(270, 595, 10, 100)
    checkpoint1 = pygame.Rect(865, 225, 100, 10)
    checkpoint2 = pygame.Rect(230, 390, 100, 10)

    checkpoint1_passed = False
    checkpoint2_passed = False

    lastTime = [99, 99, 999]
    bestTime = [99, 99, 999]
    currentLap = 0
    courseTerminee = False
    clock = pygame.time.Clock()

    while not courseTerminee:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                courseTerminee = True

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
            if currentLap == LAP_COUNT:
                # Calcul du temps total
                race_ms = pygame.time.get_ticks() - start_time
                lastRace = [
                    race_ms // 60000,
                    (race_ms // 1000) % 60,
                    race_ms % 1000
                ]

                courseTerminee = True


        pygame.draw.rect(win, NOTCHECK_COLOR, checkpoint0, 2)
        pygame.draw.rect(win, CHECK_COLOR if checkpoint1_passed else NOTCHECK_COLOR, checkpoint1, 2)
        pygame.draw.rect(win, CHECK_COLOR if checkpoint2_passed else NOTCHECK_COLOR, checkpoint2, 2)

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

        lap_text = font.render(f"Lap {currentLap} / {LAP_COUNT}", True, (255, 255, 255))
        win.blit(lap_text, (10, 40))

        pygame.display.update()
    return bestTime, lastRace

def rotate_center(image, angle):
    rotated = pygame.transform.rotate(image, angle)
    rect = rotated.get_rect(center=image.get_rect().center)
    return rotated, rect