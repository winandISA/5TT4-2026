import pygame
import sys

# --- constantes ---
WIDTH, HEIGHT = 1024, 768
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plateformer - base")
clock = pygame.time.Clock()

# --- fond ---
# adapte le nom du fichier si nécessaire (ex: "fond.png.png")
background = pygame.image.load("images/fond.png").convert()
background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

# --- plateforme ---
platform_img = pygame.image.load("images/PF2.png").convert_alpha()
platform_img = pygame.transform.smoothscale(platform_img, (300, 90))
platform_rect = platform_img.get_rect()
platform_rect.midbottom = (WIDTH // 2, HEIGHT - 80)  # position à ajuster si tu veux

# --- héros ---
hero_img = pygame.image.load("images/hero/Idle (1).png").convert_alpha()
# redimensionne le héros (tu peux changer ces valeurs)
hero_img = pygame.transform.smoothscale(hero_img, (100, 130))
hero_rect = hero_img.get_rect()
# on pose le héros sur la plateforme
hero_rect.midbottom = (platform_rect.centerx, platform_rect.top + 12)

# --- boucle principale ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # affichage
    screen.blit(background, (0, 0))
    screen.blit(platform_img, platform_rect)
    screen.blit(hero_img, hero_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
