import math
import random

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

roquettes = []
vitRoquettes = 5
meteors = []

lastRocket = pygame.time.get_ticks()
nextMeteor = pygame.time.get_ticks() + random.randint(50, 250)

clock = pygame.time.Clock()
running = True


def createRocket():
    global lastRocket
    lastRocket = pygame.time.get_ticks()
    sons["rocket"].play()
    angle_rad = math.radians(angle)
    # Calcul du déplacement
    dy = - vitRoquettes * math.cos(angle_rad)
    dx = - vitRoquettes * math.sin(angle_rad)
    image = pygame.transform.rotate(images["rocket"], angle)
    rect = image.get_rect()
    rect.center = (WIDTH // 2, HEIGHT // 2)
    roquettes.append({"vx": dx,
                      "vy": dy,
                      "image": image,
                      "rect": rect
                      })

def createMeteor():
    global nextMeteor
    nextMeteor = pygame.time.get_ticks() + random.randint(50, 250)
    choice = random.randint(1, 4)
    if choice == 1:
        x = 0
        y = random.randint(0, HEIGHT)
    elif choice == 2:
        x = 768
        y = random.randint(0, HEIGHT)
    elif choice == 3:
        x = random.randint(0, WIDTH)
        y = 0
    else:
        x = random.randint(0, WIDTH)
        y = 1024
#    angleM = pygame.math.Vector2(x,  y).angle_to((-WIDTH//2, -HEIGHT//2))
    angleM = pygame.math.Vector2(-WIDTH//2 - x, -HEIGHT//2 - y).angle_to((-WIDTH//2, -HEIGHT//2))
    angle_rad = math.radians(angleM)
    # Calcul du déplacement
    dy = - vitRoquettes * math.cos(angle_rad)
    dx = - vitRoquettes * math.sin(angle_rad)
    image = pygame.transform.rotate(images["meteor"], random.randint(0, 360))
    rect = image.get_rect()
    rect.center = (x, y)
    meteors.append({"vx": dx,
                      "vy": dy,
                      "image": image,
                      "rect": rect
                      })




# --- Boucle principale ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    souris_x, souris_y = pygame.mouse.get_pos()
    fusee_x, fusee_y = fusee_rect.center
    angle = pygame.math.Vector2(souris_x - fusee_x, souris_y - fusee_y).angle_to((0, -1))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if pygame.time.get_ticks() - lastRocket > 100:
            createRocket()
    if pygame.time.get_ticks() > nextMeteor:
        createMeteor()
    fusee_rotation = pygame.transform.rotate(images["fusee"], angle)
    fusee_rect = fusee_rotation.get_rect(center=fusee_rect.center)

    for rocket in roquettes:

        rocket["rect"].x += rocket["vx"]
        rocket["rect"].y += rocket["vy"]
        if not fenetre.get_rect().colliderect(rocket["rect"]):
            roquettes.remove(rocket)

    for rocket in meteors:

        rocket["rect"].x += rocket["vx"]
        rocket["rect"].y += rocket["vy"]


    # --- Affichage ---
    fenetre.blit(images["fond"], (0, 0))
    fenetre.blit(fusee_rotation, fusee_rect)
    for rocket in roquettes:
        fenetre.blit(rocket["image"], rocket["rect"])
    for rocket in meteors:
        fenetre.blit(rocket["image"], rocket["rect"])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()