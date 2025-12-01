import pygame
import sys

WIDTH = 1024
HEIGHT = 768
pygame.init()
fenetre = pygame.display.set_mode((WIDTH, HEIGHT))

images = {}

images["fond"] = pygame.image.load("images/fond.png").convert()
images["fusee"] = pygame.image.load("images/fusee.png").convert_alpha()
images["fusee"] = pygame.transform.smoothscale(images["fusee"], (50, 70))
images["rocket"] = pygame.image.load("images/rocket.png").convert_alpha()
images["rocket"] = pygame.transform.smoothscale(images["rocket"], (20, 25))
images["meteor"] = pygame.image.load("images/meteor.png").convert_alpha()
images["meteor"] = pygame.transform.smoothscale(images["meteor"], (50, 50))

sons = {}

sons["musique"] = pygame.mixer.Sound("sons/musique.mp3")
sons["rocket"] = pygame.mixer.Sound("sons/rocket.mp3")
sons["explosion"] = pygame.mixer.Sound("sons/explosion.wav")

pygame.display.set_caption("Jeu de fusée - Version de base")

# --- Position initiale de la fusée ---
fusee_rect = images["fusee"].get_rect()
fusee_rect.center = (WIDTH // 2, HEIGHT // 2)

clock = pygame.time.Clock()
running = True

# --- Boucle principale ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # --- Affichage ---
    fenetre.blit(images["fond"], (0, 0))
    fenetre.blit(images["fusee"], fusee_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
