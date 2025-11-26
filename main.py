import pygame, random, sys

pygame.init()
#Definition Fenster, Schriften, Zeit und Farben
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Season Drop – Ordne die Früchte zu!")

font = pygame.font.SysFont("Century Gothic", 28, bold=True)
small_font = pygame.font.SysFont("Century Gothic", 18, bold=True)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (173, 216, 230)

# Hintergrundbild laden
try:
    background_img = pygame.image.load("bilder/hintergrund.jpg").convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
except:
    background_img = None
    screen.fill(SKY)

# Körbe einfügen und position berechnen
seasons = ["Frühling", "Sommer", "Herbst", "Winter"]
basket_width, basket_height = 150, 50
baskets = []

for i in range(4):
    x = i * (WIDTH // 4) + (WIDTH // 8) - basket_width // 2
    baskets.append(pygame.Rect(x, HEIGHT - basket_height - 10, basket_width, basket_height))

# Fruchtkorb-Bild laden
try:
    basket_img = pygame.image.load("bilder/korb.webp")  # dein Bildname
    basket_img = pygame.transform.scale(basket_img, (basket_width, basket_height + 30))
except:
    basket_img = pygame.Surface((basket_width, basket_height))
    basket_img.fill((200, 200, 200))


# Früchte & zugehörige Saisons
fruits = [
    ("Rhabarber", "Frühling"),
    ("Bärlauch", "Frühling"),
    ("Brennnessel", "Frühling"),
    ("Spargel", "Frühling"),
    ("Erdbeere", "Sommer"),
    ("Zuchetti", "Sommer"),
    ("Pflaume", "Sommer"),
    ("Aprikose", "Sommer"),
    ("Gurke", "Sommer"),
    ("Apfel", "Herbst"),
    ("Kürbis", "Herbst"),
    ("Birne", "Herbst"),
    ("Süsskartoffel", "Herbst"),
    ("Ingwer", "Herbst"),
    ("Orange", "Winter"),
    ("Zitrone", "Winter"),
    ("Federkohl", "Winter"),
    ("Rosenkohl", "Winter")

]

#Umlaute anpassen
def safe_filename(name):
    return (name.lower()
                 .replace("ä", "ae")
                 .replace("ö", "oe")
                 .replace("ü", "ue"))

# Frucht-Bild laden
fruit_images = {}
for name, _ in fruits:
    path = f"bilder/{safe_filename(name)}.png"
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (100, 100))
    except:
        img = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.ellipse(img, (255, 100, 100), img.get_rect())
    fruit_images[name] = img


# Funktion, um neue Frucht zu erzeugen
def new_fruit():
    name, season = random.choice(fruits)
    x = random.randint(50, WIDTH - 50)
    y = -40
    return {"name": name, "season": season, "rect": pygame.Rect(x, y, 65, 65)}

# Startwerte
fruit = new_fruit()
score = 0
fall_speed = 2
move_speed = 6
game_over = False

# Reset-Button
button_width, button_height = 200, 50
button_x = WIDTH // 2 - button_width // 2
button_y = HEIGHT // 2 + 40
reset_button = pygame.Rect(button_x, button_y, button_width, button_height)


# Hauptschleife
running = True
game_started = False
show_labels = True
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
label_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 40, 300, 50)

while running:
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(SKY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_started:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_started = True
                    game_over = False
                    score = 0
                    fall_speed = 2
                    fruit = new_fruit()
                    fruit["rect"].y = 0
                if label_button.collidepoint(event.pos):
                    show_labels = not show_labels

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if reset_button.collidepoint(event.pos):
                # Reset der Startwerte
                score = 0
                fall_speed = 2
                fruit = new_fruit()
                game_over = False

    # Frucht bewegen
    keys = pygame.key.get_pressed()
    if game_started and not game_over:
        if keys[pygame.K_LEFT]:
            fruit["rect"].x -= move_speed
        if keys[pygame.K_RIGHT]:
            fruit["rect"].x += move_speed
        if keys[pygame.K_DOWN]:
            fruit["rect"].y += move_speed
        fruit["rect"].y += fall_speed



        # Begrenzung des Spielfelds
        fruit["rect"].x = max(0, min(fruit["rect"].x, WIDTH - fruit["rect"].width))

        # Kollision mit Körben prüfen
        for i, basket in enumerate(baskets):
            if basket.colliderect(fruit["rect"]):
                if fruit["season"] == seasons[i]:
                    score += 1
                    fall_speed += 0.1  # Schwierigkeit erhöhen
                    fruit = new_fruit()
                else:
                    game_over = True

        # Wenn Frucht kein Korb trifft
        if fruit["rect"].bottom > HEIGHT:
            game_over = True

    # Körbe zeichnen
    for i, basket in enumerate(baskets):
        screen.blit(basket_img, (basket.x, basket.y - 10))
        label = font.render(seasons[i], True, WHITE)
        label_rect = label.get_rect(center=(basket.x + basket_width // 2, basket.y + 30))
        screen.blit(label, label_rect)

    # Frucht zeichnen
    if game_started and not game_over:
        screen.blit(fruit_images[fruit["name"]], fruit["rect"])
    if show_labels and not game_over:
        name_label = small_font.render(fruit["name"][:15], True, BLACK)
        screen.blit(name_label, (fruit["rect"].x, fruit["rect"].y - 20))

    # Punkteanzeige
    score_label = font.render(f"Punkte: {score}", True, BLACK)
    screen.blit(score_label, (10, 10))

    # Startbildschirm
    if not game_started:
        title = font.render("Season Drop – Ordne die Früchte zu!", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        pygame.draw.rect(screen, (200, 255, 110), start_button)
        start_text = font.render("Start", True, BLACK)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 18))
        pygame.draw.rect(screen, (180, 110, 50), label_button)
        status_text = "Beschriftung: AN" if show_labels else "Beschriftung: AUS"
        txt = font.render(status_text, True, BLACK)
        screen.blit(txt, (label_button.x + (label_button.width - txt.get_width()) // 2,
                          label_button.y + 10))
        pygame.display.flip()
        clock.tick(60)
        continue

    # Game Over
    if game_over:
        over_label = font.render("Falsche Saison! Spiel vorbei!", True, (139, 69, 19))
        screen.blit(over_label, (WIDTH // 2 - 170, HEIGHT // 2 - 20))

        # Reset-Button zeichnen
        pygame.draw.rect(screen, (173, 216, 255), reset_button)
        btn_label = font.render("Neu starten", True, BLACK)
        btn_rect = btn_label.get_rect(center=reset_button.center)
        screen.blit(btn_label, btn_rect)

    pygame.display.flip()
    clock.tick(60)