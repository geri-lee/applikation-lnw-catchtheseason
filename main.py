import pygame, random, sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Season Drop – Fange die Früchte!")

font = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (120, 180, 255)

# Körbe (vier Saisons)
seasons = ["Frühling", "Sommer", "Herbst", "Winter"]
basket_width, basket_height = 150, 50
baskets = []
for i in range(4):
    x = i * (WIDTH // 4) + (WIDTH // 8) - basket_width // 2
    baskets.append(pygame.Rect(x, HEIGHT - basket_height - 10, basket_width, basket_height))

# Farben der Körbe
basket_colors = [(140, 230, 140), (255, 230, 100), (255, 180, 100), (200, 200, 255)]

# Früchte & zugehörige Saisons
fruits = [
    ("Apfel", "Herbst"),
    ("Erdbeere", "Sommer"),
    ("Kürbis", "Herbst"),
    ("Orange", "Winter"),
    ("Kirsche", "Frühling"),
    ("Melone", "Sommer"),
    ("Birne", "Herbst"),
    ("Pflaume", "Sommer"),
    ("Zitrone", "Winter")
]

# Funktion, um neue Frucht zu erzeugen
def new_fruit():
    name, season = random.choice(fruits)
    x = random.randint(50, WIDTH - 50)
    y = -40
    return {"name": name, "season": season, "rect": pygame.Rect(x, y, 40, 40)}

# Startwerte
fruit = new_fruit()
score = 0
fall_speed = 3
move_speed = 6
game_over = False

# Hauptschleife
running = True
while running:
    screen.fill(SKY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if not game_over:
        # Frucht bewegen
        if keys[pygame.K_LEFT]:
            fruit["rect"].x -= move_speed
        if keys[pygame.K_RIGHT]:
            fruit["rect"].x += move_speed
        fruit["rect"].y += fall_speed

        # Begrenzung des Spielfelds
        fruit["rect"].x = max(0, min(fruit["rect"].x, WIDTH - fruit["rect"].width))

        # Kollision mit Körben prüfen
        for i, basket in enumerate(baskets):
            if basket.colliderect(fruit["rect"]):
                if fruit["season"] == seasons[i]:
                    score += 1
                    fall_speed += 0.2  # Schwierigkeit erhöhen
                    fruit = new_fruit()
                else:
                    game_over = True

        # Wenn Frucht den Boden erreicht, ohne zu treffen → Game Over
        if fruit["rect"].bottom > HEIGHT:
            game_over = True

    # Körbe zeichnen
    for i, basket in enumerate(baskets):
        pygame.draw.rect(screen, basket_colors[i], basket)
        label = font.render(seasons[i], True, BLACK)
        screen.blit(label, (basket.x + 15, basket.y + 10))

    # Frucht zeichnen
    pygame.draw.ellipse(screen, (255, 100, 100), fruit["rect"])
    name_label = font.render(fruit["name"][:10], True, BLACK)
    screen.blit(name_label, (fruit["rect"].x - 10, fruit["rect"].y - 30))

    # Punkteanzeige
    score_label = font.render(f"Punkte: {score}", True, BLACK)
    screen.blit(score_label, (10, 10))

    # Game Over
    if game_over:
        over_label = font.render("Falsche Frucht! Spiel vorbei!", True, (255, 0, 0))
        screen.blit(over_label, (WIDTH // 2 - 200, HEIGHT // 2 - 20))

    pygame.display.flip()
    clock.tick(60)