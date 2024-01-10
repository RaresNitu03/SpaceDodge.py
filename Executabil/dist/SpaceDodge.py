import pygame
import time
import random
import pygame.mask
import sys

#initializam modulele Pygame pentru font si sunet
pygame.font.init()
pygame.mixer.init()

#definim dimensiunile ferestrei 
WIDTH = 1000 
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

#incarcam intr-o variabila imaginea de funal
BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))

#definim dimensiunele navetei spatiale si incarcam imaginea acesteia
SPACESHIP_WIDTH = 80
SPACESHIP_HEIGHT = 120
SPACESHIP = pygame.transform.scale(pygame.image.load("spaceship.png"), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
#definim o maska pentru a avea dimensiunile cat mai exacte ale navetei spatiale
SPACESHIP_MASK = pygame.mask.from_surface(SPACESHIP)

#definim dinmensiunile si viteza obstacolelor
STAR_WIDTH, STAR_HEIGHT = 10, 20
STAR_VEL = 3

#initializam fonul textului
FONT = pygame.font.SysFont("comicsans", 30)

#incarcam fisierul de muzica pentru fundal
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.5)  # Adjust the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

#creeam functia de desenare a elementelor pe ecran
def draw(spaceship, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    #afisam timpul de cand a inceput jocul pe ecran in coltul din stanga sus
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    #afisarea pe ecran a navei spatiale
    WIN.blit(SPACESHIP, (spaceship.x, spaceship.y))

    #afisarea pe ecran a obstacolelor
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

#functia principala a jocului
def main():
    run = True

    #initializam variabile pentru nava si timp
    spaceship = pygame.Rect(200, HEIGHT - SPACESHIP_HEIGHT, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    #initializam variabilele pentru generarea obstacolelor
    star_add_increment = 2000
    star_count = 0

    #creeam o lista pentru a salva obstacolele 
    stars = []

    hit = False

    while run:
        #actualizam contorul pentru a adauga stele si pentru a afla timpul scurs
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        #generam obstacole la intervale regulate
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            #reducem intervalul de generare al stelelor pentru a creste dificultatea
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        #verificam daca fereastra a fost inchisa
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        #realizarea miscarii navetei spatiale prin intermediul tastelor apasate
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship.x - SPACESHIP_WIDTH + 80>= 0:
            spaceship.x -= SPACESHIP_WIDTH * 0.125
        if keys[pygame.K_RIGHT] and spaceship.x + SPACESHIP_WIDTH <= WIDTH:
            spaceship.x += SPACESHIP_WIDTH * 0.125
        if keys[pygame.K_UP] and spaceship.y - SPACESHIP_HEIGHT + 60 >= 0:
            spaceship.y -= SPACESHIP_HEIGHT * 0.1
        if keys[pygame.K_DOWN] and spaceship.y + SPACESHIP_HEIGHT + 10 <= HEIGHT:
            spaceship.y += SPACESHIP_HEIGHT * 0.1

        #realizam miscarea obstacolelor 
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            else:
                #pentru fiecare obstacol de pe ecran se creeaza o maska pentru a putea verifica coliziunea
                star_rect = pygame.Rect(star.x, star.y, STAR_WIDTH, STAR_HEIGHT)
                star_mask = pygame.mask.from_surface(pygame.Surface((STAR_WIDTH, STAR_HEIGHT)))
                offset = (star_rect.x - spaceship.x, star_rect.y - spaceship.y)
                #verificam daca a avut loc coliziunea intre obstacol si nava spatiala
                if SPACESHIP_MASK.overlap(star_mask, offset):
                    stars.remove(star)
                    hit=True
                    break
    
            #daca naveta a fost atinsa de un obstacol oprim jocul 
            if hit:
                lost_text = FONT.render("You Lost!", 1, "white")
                WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
                pygame.display.update()
                pygame.mixer.music.stop()  # Stop the music when the game ends
                pygame.time.delay(1000)
                sys.exit()

        #desenam obiectele pe ecran
        draw(spaceship, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()
