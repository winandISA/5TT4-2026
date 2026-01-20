import pygame
import pytmx

# --- CONFIGURATION ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
ZOOM_FACTOR = 2  # Pour afficher la map et le perso 2x plus grand


class Knight(pygame.sprite.Sprite):
    def __init__(self, pos, obstacles):
        super().__init__()
        # Perso plus grand (environ 64x64 avec le zoom)
        img = pygame.image.load("map/knight.png").convert_alpha()
        self.image = pygame.transform.scale(img, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15, -15)  # Hitbox ajustée

        self.obstacles = obstacles
        self.direction = pygame.math.Vector2()

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.y = (keys[pygame.K_DOWN] - keys[pygame.K_UP])
        self.direction.x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        for rect in self.obstacles:
            if rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox.right = rect.left
                    if self.direction.x < 0: self.hitbox.left = rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.hitbox.bottom = rect.top
                    if self.direction.y < 0: self.hitbox.top = rect.bottom

    def update(self):
        self.input()
        self.move(PLAYER_SPEED)


# --- INITIALISATION ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

tmx_data = pytmx.load_pygame("map/sans titre.tmx")

# Extraction des collisions et du spawn
obstacles = [pygame.Rect(obj.x, obj.y, obj.width, obj.height) for obj in tmx_data.get_layer_by_name("Collisions")]
spawn = tmx_data.get_layer_by_name("Points")[0]
knight = Knight((spawn.x, spawn.y), obstacles)

# Création d'une surface pour la map (pour optimiser et zoomer)
map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight
full_map_surface = pygame.Surface((map_width, map_height))

for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid in layer:
            tile = tmx_data.get_tile_image_by_gid(gid)
            if tile:
                full_map_surface.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

# Redimensionnement de la map pour l'effet "plus grand"
scaled_map = pygame.transform.scale(full_map_surface, (map_width * ZOOM_FACTOR, map_height * ZOOM_FACTOR))

# --- BOUCLE PRINCIPALE ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # Mise à jour du perso
    knight.update()

    # CALCUL DE LA CAMÉRA (OFFSET)
    # On veut que le perso soit au milieu de l'écran
    # Offset = (Centre écran) - (Position Joueur zoomée)
    offset_x = (SCREEN_WIDTH // 2) - (knight.rect.centerx * ZOOM_FACTOR)
    offset_y = (SCREEN_HEIGHT // 2) - (knight.rect.centery * ZOOM_FACTOR)

    # RENDU
    screen.fill((30, 30, 30))

    # Dessiner la map décalée
    screen.blit(scaled_map, (offset_x, offset_y))

    # Dessiner le perso décalé
    # On crée un rect temporaire pour l'affichage
    player_draw_pos = (knight.rect.x * ZOOM_FACTOR + offset_x, knight.rect.y * ZOOM_FACTOR + offset_y)
    # Note : Le perso est déjà scalé dans sa classe, on l'affiche juste à la position offset
    screen.blit(knight.image, player_draw_pos)

    pygame.display.update()
    clock.tick(60)

pygame.quit()