import pygame, random, sys

pygame.init()

#============= Konstanten =============#
#Farben, Bildschirm, Schriftart
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (173, 216, 230)
BASKET_SIZE = (150, 50)
FRUIT_SIZE = (100,100)
FONT = pygame.font.SysFont("Century Gothic",28,bold=True)
SMALL_FONT = pygame.font.SysFont("Century Gothic",18,bold=True)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Season Drop – Ordne die Früchte zu!")
clock = pygame.time.Clock()

#Früchte und Saisons
seasons = ["Frühling","Sommer","Herbst","Winter"]
fruits = [
    ("Rhabarber","Frühling"),
    ("Bärlauch","Frühling"),
    ("Brennnessel","Frühling"),
    ("Spargel","Frühling"),
    ("Erdbeere","Sommer"),
    ("Zuchetti","Sommer"),
    ("Pflaume","Sommer"),
    ("Aprikose","Sommer"),
    ("Gurke","Sommer"),
    ("Apfel","Herbst"),
    ("Kürbis","Herbst"),
    ("Birne","Herbst"),
    ("Süsskartoffel","Herbst"),
    ("Ingwer","Herbst"),
    ("Orange","Winter"),
    ("Zitrone","Winter"),
    ("Federkohl","Winter"),
    ("Rosenkohl","Winter")
]

#============= FUNKTIONEN =============#

#Bilder laden
def load_image(path, size = None, fallback_color = (200,200,200)):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img,size) if size else img
    except:
        surf = pygame.Surface(size or (50,50),pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf

#Umlaute anpassen
def safe_filename(name):
    return (name.lower()
                .replace("ä","ae")
                .replace("ö","oe")
                .replace("ü","ue"))

#Neue Frucht erstellen
def new_fruit():
    name,season = random.choice(fruits)
    rect = pygame.Rect(random.randint(50,WIDTH-50), -40, 65, 65)
    return {"name":name,"season":season,"rect":rect}

#Button zeichnen
def draw_button(rect,text,color):
    pygame.draw.rect(screen,color,rect)
    label = FONT.render(text,True,BLACK)
    screen.blit(label,label.get_rect(center=rect.center))

#Game Reseten
def reset_game():
    return new_fruit(),0,2,False


#============= BILDER LADEN =============#

#Hintergrund
bg = load_image("bilder/hintergrund.jpg",(WIDTH,HEIGHT), fallback_color=SKY)

#Körbe
baskets = [
    pygame.Rect(i * (WIDTH//4) + (WIDTH//8) - BASKET_SIZE[0]//2,
                HEIGHT-BASKET_SIZE[1]-10, *BASKET_SIZE)
    for i in range(4)
]
basket_img = load_image("bilder/korb.webp",(150,80))

#Früchte
fruit_images = {
    name: load_image(f"bilder/{safe_filename(name)}.png",FRUIT_SIZE,(255,100,100))
    for name,_ in fruits
}

#============= SPIEL-STATUS =============#
fruit, score, fall_speed, game_over = reset_game()
running = True
game_started = False
show_labels = True

#Buttons zeichnen
start_button = pygame.Rect(WIDTH//2-100,HEIGHT//2-25,200,50)
label_button = pygame.Rect(WIDTH//2-150,HEIGHT//2+40,300,50)
reset_button = pygame.Rect(WIDTH//2-100,HEIGHT//2+40,200,50)


#============= HAUPTSCHLEIFE =============#
while running:
    if bg:
        screen.blit(bg,(0,0))
    else:
        screen.fill(SKY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #kein aktives Spiel
        if not game_started:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    fruit,score,fall_speed,game_over = reset_game()
                    game_started = True
                if label_button.collidepoint(event.pos):
                    show_labels = not show_labels

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if reset_button.collidepoint(event.pos):
                fruit,score,fall_speed,game_over = reset_game()


    #aktives Spiel
    if game_started and not game_over:

        keys = pygame.key.get_pressed()
        fruit["rect"].x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 6        #rechts/links
        fruit["rect"].y += fall_speed + (keys[pygame.K_DOWN] * 6)                  #verschnellern nach unten
        fruit["rect"].x = max(0, min(fruit["rect"].x, WIDTH-fruit["rect"].width))  #Spielfeld Begrenzen

        # Kollision Korb
        for i,basket in enumerate(baskets):
            if basket.colliderect(fruit["rect"]):
                if fruit["season"] == seasons[i]:
                    score += 1
                    fall_speed += 0.1           #Schwierigkeit erhöhen
                    fruit = new_fruit()
                else:
                    game_over = True

        #Wenn Frucht kein Korb trifft
        if fruit["rect"].bottom > HEIGHT:
            game_over = True


    #========== ZEICHNEN ==========#

    #Körbe
    for i,basket in enumerate(baskets):
        screen.blit(basket_img,(basket.x,basket.y-10))
        txt = FONT.render(seasons[i],True,WHITE)
        screen.blit(txt,txt.get_rect(center=(basket.x+75,basket.y+30)))

    #Körbe
    if game_started and not game_over:
        screen.blit(fruit_images[fruit["name"]],fruit["rect"])
        if show_labels:
            screen.blit(SMALL_FONT.render(fruit["name"],True,BLACK),(fruit["rect"].x,fruit["rect"].y-20))

    #Punkteanzeige
    screen.blit(FONT.render(f"Punkte: {score}",True,BLACK),(10,10))

    #========== STARTBILDSCHIRM ==========#
    if not game_started:
        title=FONT.render("Season Drop – Ordne die Früchte zu!",True,BLACK)
        screen.blit(title,(WIDTH//2-title.get_width()//2,HEIGHT//2-100))
        draw_button(start_button,"Start",(200,255,110))
        draw_button(label_button,f"Beschriftung: {'AN' if show_labels else 'AUS'}",(180,110,50))
        pygame.display.flip()
        clock.tick(60)
        continue

    #========== GAME OVER ==========#
    if game_over:
        screen.blit(FONT.render("Falsche Saison! Spiel vorbei!",True,(139,69,19)),(WIDTH//2-170,HEIGHT//2-20))
        draw_button(reset_button,"Neu starten",(173,216,255))

    pygame.display.flip()
    clock.tick(60)