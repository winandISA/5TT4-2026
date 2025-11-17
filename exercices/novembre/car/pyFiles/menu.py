import pygame
from .config import WIDTH, HEIGHT

def run_menu(win, last_lap, last_race, best_lap, best_race):

    # --- Logo plus grand ---
    logo = pygame.image.load("images/carFace.png").convert_alpha()
    logo = pygame.transform.smoothscale(logo, (450, 300))

    font_title = pygame.font.SysFont(None, 80)
    font_line = pygame.font.SysFont(None, 36)
    font_button = pygame.font.SysFont(None, 60)

    # --- Bouton START ---
    start_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 180, 300, 80)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    return "start"

        # --- Fond ---
        win.fill((10, 10, 40))

        # --- Logo ---
        logo_rect = logo.get_rect(center=(WIDTH // 2, 180))
        win.blit(logo, logo_rect.topleft)

        # --- Titre ---
        title = font_title.render("Course F1", True, (255, 255, 255))
        win.blit(title, (WIDTH//2 - title.get_width()//2, 350))

        # --- Informations en double colonnes ---
        # Formatage des chaînes
        lap_line  = f"Last Lap: {last_lap[0]:02d}:{last_lap[1]:02d}:{last_lap[2]:03d}   |   Best Lap: {best_lap[0]:02d}:{best_lap[1]:02d}:{best_lap[2]:03d}"
        race_line = f"Last Race: {last_race[0]:02d}:{last_race[1]:02d}:{last_race[2]:03d} | Best Race: {best_race[0]:02d}:{best_race[1]:02d}:{best_race[2]:03d}"

        lap_text  = font_line.render(lap_line, True, (255,255,255))
        race_text = font_line.render(race_line, True, (255,255,255))

        # Centrage des deux lignes
        win.blit(lap_text,  (WIDTH//2 - lap_text.get_width()//2, 420))
        win.blit(race_text, (WIDTH//2 - race_text.get_width()//2, 460))

        # --- Bouton START ---
        pygame.draw.rect(win, (0, 130, 0), start_button, border_radius=10)
        pygame.draw.rect(win, (255, 255, 255), start_button, 3, border_radius=10)

        start_txt = font_button.render("START", True, (255, 255, 255))
        win.blit(start_txt, (
            start_button.centerx - start_txt.get_width()//2,
            start_button.centery - start_txt.get_height()//2
        ))

        pygame.display.update()
