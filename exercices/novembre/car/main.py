import pygame
from pyFiles.config import WIDTH, HEIGHT
from pyFiles.menu import run_menu
from pyFiles.game import run_game

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
best_lap = [99, 99, 999]
best_race = [99, 99, 999]
last_lap = [99, 99, 999]
last_race = [99, 99, 999]

running = True
while running:

    choice = run_menu(win, last_lap, last_race, best_lap, best_race)

    if choice == "quit":
        running = False
        break

    last_lap, last_race = run_game(win)
    if last_lap < best_lap:
        best_lap = last_lap
    if last_race < best_race:
        best_race = last_race

pygame.quit()