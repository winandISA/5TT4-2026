import pygame
import sys
import math

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
roquettes = []
vitRoquettes = 5
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
lastRocket = pygame.time.get_ticks()
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
            lastRocket = pygame.time.get_ticks()
            angle_radian = -math.radians(angle)
            vy = -vitRoquettes * math.cos(angle_radian)
            vx = vitRoquettes * math.sin(angle_radian)

            rocket_rot = pygame.transform.rotate(images["rocket"], angle)
            rect_rocket = rocket_rot.get_rect(center=fusee_rect.center)

            roquettes.append({
                "image": rocket_rot,
                "rect": rect_rocket,
                "vx": vx,
                "vy": vy
            })

            sons["rocket"].play()

    fusee_rotation = pygame.transform.rotate(images["fusee"], angle)
    fusee_rect = fusee_rotation.get_rect(center=fusee_rect.center)

    for rocket in roquettes:
        rocket["rect"].x += rocket["vx"]
        rocket["rect"].y += rocket["vy"]
        if not fenetre.get_rect().colliderect(rocket["rect"]):
            roquettes.remove(rocket)



    # --- Affichage ---
    fenetre.blit(images["fond"], (0, 0))
    fenetre.blit(fusee_rotation, fusee_rect)
    for rocket in roquettes:
        fenetre.blit(rocket["image"], rocket["rect"])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
