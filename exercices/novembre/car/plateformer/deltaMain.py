from inspect import walktree

import pygame
import sys

# --- constantes ---
WIDTH, HEIGHT = 1024, 768
FPS = 60
GRAVITY = 1            # force de gravité (pixels par frame²)
PLAYER_SPEED = 5       # vitesse de déplacement horizontal
JUMP_STRENGTH = -18    # force du saut (négatif = vers le haut)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plateformer - chevalier")
clock = pygame.time.Clock()

# --- fond ---
background = pygame.image.load("images/fond.png").convert()
background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

# --- plateforme ---
platform_img = pygame.image.load("images/PF2.png").convert_alpha()
platform_img = pygame.transform.smoothscale(platform_img, (300, 90))
platform_rect = platform_img.get_rect()
platform_rect.midbottom = (WIDTH // 2, HEIGHT - 80)

# --- animation de marche ---
walk_frames = []
dead_frames = []
idle_frames = []
for i in range(1, 11):  # Walk (1) à Walk (10)
    path = f"images/hero/Walk ({i}).png"
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.smoothscale(img, (100, 130))
    walk_frames.append(img)
    path = f"images/hero/Dead ({i}).png"
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.smoothscale(img, (100, 130))
    dead_frames.append(img)
    path = f"images/hero/Idle ({i}).png"
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.smoothscale(img, (100, 130))
    idle_frames.append(img)

# image actuelle du héros
hero_img = idle_frames[0]
hero_rect = hero_img.get_rect()
hero_rect.midbottom = (platform_rect.centerx, platform_rect.top - 150)

# état du héros
velocity_y = 0
is_dead = False
looking_right = True

# animation
walk_index = 0.0
idle_index = 0.0
anim_speed = 0.3  # plus petit = animation plus lente


def is_on_platform():
    """Retourne True si le héros est posé sur la plateforme."""
    return hero_rect.bottom == platform_rect.top + 12 and velocity_y == 0


# --- boucle principale ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # saut
        if event.type == pygame.KEYDOWN and not is_dead:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                if is_on_platform():
                    velocity_y = JUMP_STRENGTH

    keys = pygame.key.get_pressed()

    if not is_dead:
        # --- déplacement horizontal ---
        moving = False

        if keys[pygame.K_LEFT]:
            hero_rect.x -= PLAYER_SPEED
            moving = True
            looking_right = False

        if keys[pygame.K_RIGHT]:
            hero_rect.x += PLAYER_SPEED
            moving = True
            looking_right = True

        # limites écran
        if hero_rect.left < 0:
            hero_rect.left = 0
        if hero_rect.right > WIDTH:
            hero_rect.right = WIDTH

        # --- gravité ---
        velocity_y += GRAVITY
        hero_rect.y += velocity_y

        # --- collision avec la plateforme ---
        if hero_rect.colliderect(platform_rect) and velocity_y > 0:
            hero_rect.bottom = platform_rect.top + 12
            velocity_y = 0

        # --- mort si on tombe en bas ---
        if hero_rect.top >= HEIGHT:
            is_dead = True
            idle_index = 0.0
            hero_img = dead_frames[0]
            # on garde la position horizontale
            centerx = hero_rect.centerx
            hero_rect = hero_img.get_rect()
            hero_rect.midbottom = (centerx, HEIGHT)

        # --- choix de l'image (idle / walk) ---
        if not is_dead:
            if moving:
                idle_index = 0.0
                walk_index += anim_speed
                if walk_index >= len(walk_frames):
                    walk_index = 0.0
                hero_img = walk_frames[int(walk_index)]
            else:
                walk_index = 0.0
                idle_index += anim_speed
                if idle_index >= len(idle_frames):
                    idle_index = 0.0
                hero_img = idle_frames[int(idle_index)]
    else:
        walk_index += anim_speed
        if walk_index >= len(walk_frames):
            running = False
            walk_index = 0.0
        else:
            hero_img = dead_frames[int(walk_index)]
    # --- affichage ---
    screen.blit(background, (0, 0))
    screen.blit(platform_img, platform_rect)

    # retourne le sprite si on regarde à gauche (que si vivant)
    img_to_draw = hero_img
    if not is_dead and not looking_right:
        img_to_draw = pygame.transform.flip(hero_img, True, False)

    screen.blit(img_to_draw, hero_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
