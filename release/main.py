#Importi
import pygame
from pygame import mixer
pygame.time.Clock().tick(60)

#Funkcije
def check_click(button, silent):  #Gleda za klik na botunima
    if coords[button][0] <= mouse[0] <= coords[button][0] + button_radii[button][0] * 2:
        if coords[button][1] <= mouse[1] <= coords[button][1] + button_radii[button][1] * 2:
            if not (silent):
                print("Pass")
            return (True)
        else:
            if not (silent):
                print("Fail B")
            return (False)
    else:
        if not (silent):
            print("Fail A")
        return (False)


def load():  #Loada podatke iz data.txt
    try:
        with open("data.txt") as f:
            f = f.read()
            data = eval(f)
            if not (("pl_Wins" in data) and ("ai_Wins" in data) and ("draws" in data) and ("pl_r" in data) and (
                    "pl_p" in data) and ("pl_s" in data) and ("seed" in data) and ("lang" in data)):
                data = {"pl_Wins": 0, "ai_Wins": 0, "draws": 0, "pl_r": 0, "pl_p": 0, "pl_s": 0, "seed": 0,
                        "lang": "hr"}
    except:
        with open("data.txt", "w") as f:
            f.write('{"pl_Wins":0,"ai_Wins":0,"draws":0,"pl_r":0,"pl_p":0,"pl_s":0,"seed":0,"lang":"en"}')
            data = {"pl_Wins": 0, "ai_Wins": 0, "draws": 0, "pl_r": 0, "pl_p": 0, "pl_s": 0, "seed": 0, "lang": "hr"}
    return (data)


def random(seed):  #Pseudorandom generator totalno ne za varanje
    return ((1664525 * seed + 1013904223) % (2 ** 32))


def ai(seed, cheats, input):  #AI protivnika. Što više igrač igra npr kamen, to je veča šansa da će AI igrat papir
    global image_ai
    rock = data["pl_r"]
    scissors = data["pl_s"]
    paper = data["pl_p"]
    if cheats == True:
        if input == 0:
            rock += 1
        elif input == 1:
            scissors += 1
        else:
            paper += 1
    l = [rock, scissors, paper]
    most_played = l.index(max(l))
    counter_pick = (most_played - 1) % 3
    total = sum(l)
    maximum = max(l)
    if maximum / (total) >= 0.8:
        seed = random(seed)
        rng = seed % 7
        if rng >= 2:
            ai_pick = counter_pick
        else:
            ai_pick = rng
    elif maximum / (total) >= 0.65:
        seed = random(seed)
        rng = seed % 6
        if rng >= 2:
            ai_pick = counter_pick
        else:
            ai_pick = rng
    elif maximum / (total) >= 0.5:
        seed = random(seed)
        rng = seed % 5
        if rng >= 2:
            ai_pick = counter_pick
        else:
            ai_pick = rng
    elif maximum / (total) >= 0.4:
        seed = random(seed)
        rng = seed % 4
        if rng >= 2:
            ai_pick = counter_pick
        else:
            ai_pick = rng
    else:
        seed = random(seed)
        rng = seed % 3
        ai_pick = rng
    if cheats:
        return (ai_pick)
    else:
        image_ai = pygame.image.load(["rock", "scissors", "paper"][ai_pick] + ".png").convert_alpha()
        image_ai = pygame.transform.scale(image_ai, (button_radii[1][0] * 2, button_radii[1][1] * 2))
        return (seed, ai_pick)


def check_game(player, ai):  #Gleda tko je pobijedio
    global text_game
    global text_game_rectangle
    global played
    if player == ai:
        text_game = font.render(lang[11], 32, (255, 100, 0))
        data["draws"] += 1
    elif (player + 1) % 3 == ai:
        text_game = font.render(lang[9], 32, (0, 255, 0))
        data["pl_Wins"] += 1
    else:
        text_game = font.render(lang[10], 32, (255, 0, 0))
        data["ai_Wins"] += 1
    # text_game_rectangle=(864,350)
    text_game_rectangle = text_game.get_rect()
    text_game_rectangle.center = (960, 380)
    played = True


def check_game_cheats(player, ai):  #Uuuuhm ništa haha
    if player == ai:
        return (lang[11])
    elif (player + 1) % 3 == ai:
        return (lang[9])
    else:
        return (lang[10])


def game_color(player, ai):
    if player == ai:
        return ((255, 100, 0))
    elif (player + 1) % 3 == ai:
        return ((0, 255, 0))
    else:
        return ((255, 0, 0))


def load_lang(lang):  #Učita jezik bez da napravi kopiju liste
    return (eval("lang_" + lang))


#Varijable
coords = [(614, 780), (864, 780), (1114, 780), (1400, 500), (1400, 800), (1800, 50), (1200, 32), (1400, 32), (1600, 32),(1200, 136), (1400, 136), (1600, 136),(1200, 240), (1400, 240), (1600, 240)]
button_radii = [(96, 96), (96, 96), (96, 96), (200, 100), (200, 100), (48, 48), (96, 48), (96, 48), (96, 48), (96, 48), (96, 48), (96, 48), (96, 48), (96, 48), (96, 48)]
button1 = (204, 197, 197)
button2 = (179, 170, 170)
#Jezici
lang_hr = ["Kamen: ", "Škare: ", "Papir: ", "Debug", "Kreni", "Izađi", "Pobjede: ", "Porazi: ", "Remiziranja: ",
           "Pobjeda", "Poraz", "Remi", "Seed: ", "Udio kamen: ", "Udio škare: ", "Udio papir: ","Jačina glazbe: "]
lang_en = ["Rock: ", "Scissors: ", "Paper: ", "Debug", "Start", "Quit", "Wins: ", "Defeats: ", "Draws: ", "Win",
           "Defeat", "Draw", "Seed: ", "Rock percentage: ", "Scissors percentage: ", "Paper percentage: ","Music volume: "]
lang_it = ["Sasso: ", "Forbici: ", "Carta: ", "Debug", "Inizia", "Esci", "Vittorie: ", "Perdite: ", "Pareggi: ",
           "Vittoria", "Perdita", "Pareggio", "Seed: ", "Percentuale sasso: ", "Percentuale forbici: ",
           "Percentuale carta: ","Volume: "]
lang_nl = ["Steen: ", "Schaar: ", "Papier: ", "Debug", "Starten", "Stoppen", "Gewonnen: ", "Verloren: ", "Gelijkspeeld: ", "Gewonnen", "Verloren", "Gelijkspel", "Seed: ", "Steen percentage: ", "Schaar percentage: ", "Papier percentage: ", "Muziekvolume: "]
lang_ua = ["Камінь: ", "Ножиці: ", "Папір: ", "Debug", "Старт", "Вийти", "Перемоги: ", "Поразки: ", "Нічиї: ", "Перемога", "Поразка", "Нічия", "Seed: ", "Відсоток каменю: ", "Відсоток ножиць: ", "Відсоток паперу: ", "Гучність музики: "]
lang_pl = ["Kamień: ", "Nożyczki: ", "Papier: ", "Debug", "Start", "Wyjdź", "Wygrane: ", "Przegrane: ", "Remisy: ", "Wygrana", "Przegrana", "Remis", "Seed: ", "Procent kamienia: ", "Procent nożyczek: ", "Procent papieru: ", "Głośność muzyki: "]
lang_fr = ["Pierre: ", "Ciseaux: ", "Papier: ", "Debug", "Commencer", "Quitter", "Victoires: ", "Défaites: ", "Égalités: ", "Victoire", "Défaite", "Égalité", "Seed: ", "Pourcentage pierre: ", "Pourcentage ciseaux: ", "Pourcentage papier: ", "Volume musique: "]
lang_de = ["Stein: ", "Schere: ", "Papier: ", "Debug", "Starten", "Beenden", "Siege: ", "Niederlagen: ", "Unentschieden: ", "Sieg", "Niederlage", "Unentschieden", "Seed: ", "Stein Prozent: ", "Schere Prozent: ", "Papier Prozent: ", "Musiklautstärke: "]
lang_pe = ["Piedra: ", "Tijeras: ", "Papel: ", "Debug", "Empezar", "Salir", "Victorias: ", "Derrotas: ", "Empates: ", "Victoria", "Derrota", "Empate", "Seed: ", "Porcentaje piedra: ", "Porcentaje tijeras: ", "Porcentaje papel: ", "Volumen música: "]
#Još varijabli
data = load()
seed = data["seed"]
played = False
status = "Home"
lang = load_lang(data["lang"])
timer = 0
typed = False
quit=False

debug = False
cheats = False  # uhmmmm ništa haha

pygame.init()
mixer.init()
#Fontovi
font = pygame.font.Font(pygame.font.get_default_font(), 64)
font2 = pygame.font.Font(pygame.font.get_default_font(), 32)

screen_size = pygame.display.Info()
screen_width = screen_size.current_w
screen_height = screen_size.current_h

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((1920, 1080))  #Uhm kao najkorištenija rezolucija
pygame.display.set_caption("Kashir")  #Promijeniti ovo ako treba
#Loadanje slika
image_scissors = pygame.image.load("scissors.png").convert_alpha()
image_rock = pygame.image.load("rock.png").convert_alpha()
image_paper = pygame.image.load("paper.png").convert_alpha()
image_logo = pygame.image.load("icon.png").convert_alpha()
image_house = pygame.image.load("house.png").convert_alpha()
image_hr = pygame.image.load("flag_hr.png").convert_alpha()
image_it = pygame.image.load("flag_it.png").convert_alpha()
image_en = pygame.image.load("flag_br.png").convert_alpha()
image_de = pygame.image.load("flag_de.png").convert_alpha()
image_fr = pygame.image.load("flag_fr.png").convert_alpha()
image_pe = pygame.image.load("flag_pe.png").convert_alpha()
image_ua = pygame.image.load("flag_ua.png").convert_alpha()
image_pl = pygame.image.load("flag_pl.png").convert_alpha()
image_nl = pygame.image.load("flag_nl.png").convert_alpha()
image_scissors = pygame.transform.scale(image_scissors, (button_radii[1][0] * 2, button_radii[1][1] * 2))
image_rock = pygame.transform.scale(image_rock, (button_radii[0][0] * 2, button_radii[0][1] * 2))
image_paper = pygame.transform.scale(image_paper, (button_radii[2][0] * 2, button_radii[2][1] * 2))
image_house = pygame.transform.scale(image_house, (button_radii[5][0] * 2, button_radii[5][1] * 2))
#Loadanje glazbe
try:
    music = mixer.music.load("music.mp3")
    mixer.music.set_volume(0.5)
    music_loaded=True
except:
    print("Could not load music.mp3")
    music_loaded=False
# lenght=music.get_lenght()

text_game = font.render("", 32, (255, 255, 0))
text_game_rectangle = text_game.get_rect()

pygame.display.flip()
# print(mixer.music.get_pos())


while True:  #Glavni loop
    width = screen.get_width()
    height = screen.get_height()

    if (not (mixer.music.get_busy())) and music_loaded:
        mixer.music.play()

    mouse = pygame.mouse.get_pos()
    for buttons in pygame.event.get():  #Botuni
        if buttons.type == pygame.QUIT:
            pygame.quit()
        if buttons.type == pygame.MOUSEBUTTONDOWN:
            if check_click(0, True) and status == "Main":
                data["pl_r"] += 1
                seed, ai_pick = ai(seed, False, 0)
                check_game(0, ai_pick)
                player_pick = "rock"
            if check_click(1, True) and status == "Main":
                data["pl_s"] += 1
                seed, ai_pick = ai(seed, False, 0)
                check_game(1, ai_pick)
                player_pick = "scissors"
            if check_click(2, True) and status == "Main":
                data["pl_p"] += 1
                seed, ai_pick = ai(seed, False, 0)
                check_game(2, ai_pick)
                player_pick = "paper"
            if check_click(5, True) and status == "Main":
                status = "Home"
                played = False
                text_game = font.render("", 32, (0, 0, 0))
            if check_click(3, True) and status == "Home":
                status = "Main"
            if check_click(4, True) and status == "Home":
                pygame.quit()
                quit=True
                break
            if check_click(6, True) and status == "Home":
                lang = load_lang("hr")
                data["lang"] = "hr"
            if check_click(7, True) and status == "Home":
                lang = load_lang("en")
                data["lang"] = "en"
            if check_click(8, True) and status == "Home":
                lang = load_lang("it")
                data["lang"] = "it"
            if check_click(9, True) and status == "Home":
                lang = load_lang("nl")
                data["lang"] = "nl"
            if check_click(10, True) and status == "Home":
                lang = load_lang("ua")
                data["lang"] = "ua"
            if check_click(11, True) and status == "Home":
                lang = load_lang("pl")
                data["lang"] = "pl"
            if check_click(12, True) and status == "Home":
                lang = load_lang("fr")
                data["lang"] = "fr"
            if check_click(13, True) and status == "Home":
                lang = load_lang("de")
                data["lang"] = "de"
            if check_click(14, True) and status == "Home":
                lang = load_lang("pe")
                data["lang"] = "pe"

    if quit:
        break

    keys = pygame.key.get_pressed()

    if timer > 0:
        timer -= 1
    else:
        combo = 0
    # Jačina glazbe
    if keys[pygame.K_UP] and not(typed):
        mixer.music.set_volume(round(mixer.music.get_volume() + 0.1,1))
        music_volume = mixer.music.get_volume()
        #print(mixer.music.get_volume())
        typed=True

    if keys[pygame.K_DOWN] and not(typed):
        mixer.music.set_volume(round(mixer.music.get_volume() - 0.1,1))
        music_volume=mixer.music.get_volume()
        #print(mixer.music.get_volume())
        typed=True

    if keys[pygame.K_m] and not(typed):
        if mixer.music.get_volume()==0:
            mixer.music.set_volume(music_volume)
        else:
            mixer.music.set_volume(0)
        typed=True
    # Tipke
    if keys[pygame.K_1] and status == "Main" and not (typed):
        data["pl_r"] += 1
        seed, ai_pick = ai(seed, False, 0)
        check_game(0, ai_pick)
        player_pick = "rock"
        typed = True
    if keys[pygame.K_2] and status == "Main" and not (typed):
        data["pl_s"] += 1
        seed, ai_pick = ai(seed, False, 0)
        check_game(1, ai_pick)
        player_pick = "scissors"
        typed = True
    if keys[pygame.K_3] and status == "Main" and not (typed):
        data["pl_p"] += 1
        seed, ai_pick = ai(seed, False, 0)
        check_game(2, ai_pick)
        player_pick = "paper"
        typed = True

    if not (keys[pygame.K_1]) and not (keys[pygame.K_2]) and not (keys[pygame.K_3]) and not (keys[pygame.K_m]) and not (keys[pygame.K_DOWN]) and not (keys[pygame.K_UP]):
        typed = False

    if keys[pygame.K_k]:  # Ništa ovdje haha
        timer = 100
        combo = 1
    elif keys[pygame.K_i] and combo == 1:
        timer = 100
        combo = 2
    elif keys[pygame.K_f] and combo == 2:
        timer = 100
        combo = 3
    elif keys[pygame.K_l] and combo == 3:
        timer = 100
        combo = 4
    elif keys[pygame.K_a] and combo == 4:
        timer = 0
        combo = 0
        if not toggled:
            toggled = True
            if cheats == True:
                cheats = False
            else:
                cheats = True
    else:
        toggled = False

    if keys[pygame.K_d]:  # debug menu
        if not toggled2:
            toggled2 = True
            if debug == True:
                debug = False
            else:
                debug = True
    else:
        toggled2 = False

    screen.fill((254, 238, 145))  #Pozadina
    # Prikaz igračeva odabira
    if played:
        pygame.draw.rect(screen, button1,
                         [coords[1][0], coords[1][1] - 300, button_radii[0][0] * 2, button_radii[0][1] * 2])
        screen.blit(eval("image_" + player_pick), (coords[1][0], coords[1][1] - 300))

    if status == "Main":  #Kvadrati botuna
        if check_click(0, True):
            pygame.draw.rect(screen, button2,
                             [coords[0][0], coords[0][1], button_radii[0][0] * 2, button_radii[0][1] * 2])

        else:
            pygame.draw.rect(screen, button1,
                             [coords[0][0], coords[0][1], button_radii[0][0] * 2, button_radii[0][1] * 2])

        if check_click(1, True):
            pygame.draw.rect(screen, button2,
                             [coords[1][0], coords[1][1], button_radii[1][0] * 2, button_radii[1][1] * 2])

        else:
            pygame.draw.rect(screen, button1,
                             [coords[1][0], coords[1][1], button_radii[1][0] * 2, button_radii[1][1] * 2])

        if check_click(2, True):
            pygame.draw.rect(screen, button2,
                             [coords[2][0], coords[2][1], button_radii[2][0] * 2, button_radii[2][1] * 2])

        else:
            pygame.draw.rect(screen, button1,
                             [coords[2][0], coords[2][1], button_radii[2][0] * 2, button_radii[2][1] * 2])

        if check_click(5, True):
            pygame.draw.rect(screen, button2,
                             [coords[5][0], coords[5][1], button_radii[5][0] * 2, button_radii[5][1] * 2])

        else:
            pygame.draw.rect(screen, button1,
                             [coords[5][0], coords[5][1], button_radii[5][0] * 2, button_radii[5][1] * 2])
    elif status == "Home":
        if check_click(3, True):
            pygame.draw.rect(screen, button2,
                             [coords[3][0], coords[3][1], button_radii[3][0] * 2, button_radii[3][1] * 2])
        else:
            pygame.draw.rect(screen, button1,
                             [coords[3][0], coords[3][1], button_radii[3][0] * 2, button_radii[3][1] * 2])

        if check_click(4, True):
            pygame.draw.rect(screen, button2,
                             [coords[4][0], coords[4][1], button_radii[4][0] * 2, button_radii[4][1] * 2])
        else:
            pygame.draw.rect(screen, button1,
                             [coords[4][0], coords[4][1], button_radii[4][0] * 2, button_radii[4][1] * 2])
    #Random textovi
    text_wins = font.render(lang[6] + str(data["pl_Wins"]), 32, (0, 255, 0))
    text_wins_rectangle = (50, 64)
    text_draws = font.render(lang[8] + str(data["draws"]), 32, (255, 100, 0))
    text_draws_rectangle = (50, 128)
    text_defeats = font.render(lang[7] + str(data["ai_Wins"]), 32, (255, 0, 0))
    text_defeats_rectangle = (50, 196)

    text_start = font.render(lang[4], 32, (0, 0, 0))
    text_start_rectangle = text_start.get_rect()
    text_start_rectangle.center = (1600, 600)
    text_quit = font.render(lang[5], 32, (0, 0, 0))
    text_quit_rectangle = text_quit.get_rect()
    text_quit_rectangle.center = (1600, 900)

    text_music=font2.render(lang[16]+str(100*round(mixer.music.get_volume(),1))+"%",32,(0,0,0))
    text_music_rectangle=(1450, 1025)

    screen.blit(text_music,text_music_rectangle)

    if debug:
        text_debug = font2.render(lang[3], 32, (0, 0, 0))
        text_debug_rectangle = (50, 350)
        text_seed = font2.render(lang[12] + str(seed), 32, (0, 0, 0))
        text_seed_rectangle = (50, 550)
        text_rock = font2.render(lang[0] + str(data["pl_r"]), 32, (0, 0, 0))
        text_rock_rectangle = (50, 400)
        text_scissors = font2.render(lang[1] + str(data["pl_s"]), 32, (0, 0, 0))
        text_scissors_rectangle = (50, 450)
        text_paper = font2.render(lang[2] + str(data["pl_p"]), 32, (0, 0, 0))
        text_paper_rectangle = (50, 500)
        if data["pl_r"] + data["pl_p"] + data["pl_s"] > 0:
            text_rockP = font2.render(
                lang[13] + str(100 * data["pl_r"] / (data["pl_r"] + data["pl_p"] + data["pl_s"])) + "%", 32, (0, 0, 0))
            text_rockP_rectangle = (50, 600)
            text_scissorsP = font2.render(
                lang[14] + str(100 * data["pl_s"] / (data["pl_r"] + data["pl_p"] + data["pl_s"])) + "%", 32, (0, 0, 0))
            text_scissorsP_rectangle = (50, 650)
            text_paperP = font2.render(
                lang[15] + str(100 * data["pl_p"] / (data["pl_r"] + data["pl_p"] + data["pl_s"])) + "%", 32, (0, 0, 0))
            text_paperP_rectangle = (50, 700)

    if cheats:  #Nema ništa ovdje haha
        text_cheats0 = font2.render(check_game_cheats(0, ai(seed, True, 0)), 32, game_color(0, ai(seed, True, 0)))
        text_cheats0_rectangle = text_cheats0.get_rect()
        text_cheats0_rectangle.center = (coords[0][0] + button_radii[0][1], coords[0][1] + 250)
        text_cheats1 = font2.render(check_game_cheats(1, ai(seed, True, 1)), 32, game_color(1, ai(seed, True, 1)))
        text_cheats1_rectangle = text_cheats1.get_rect()
        text_cheats1_rectangle.center = (coords[1][0] + button_radii[1][1], coords[1][1] + 250)
        text_cheats2 = font2.render(check_game_cheats(2, ai(seed, True, 2)), 32, game_color(2, ai(seed, True, 2)))
        text_cheats2_rectangle = text_cheats2.get_rect()
        text_cheats2_rectangle.center = (coords[2][0] + button_radii[2][1], coords[2][1] + 250)

    if played and status == "Main":
        pygame.draw.rect(screen, button1, [coords[1][0], 100, button_radii[1][0] * 2, button_radii[1][1] * 2])
        screen.blit(image_ai, (coords[1][0], 100))

    if status == "Main":  #Prikaz slika i teksta
        screen.blit(image_scissors, (coords[1][0], coords[1][1]))
        screen.blit(image_rock, (coords[0][0], coords[0][1]))
        screen.blit(image_paper, (coords[2][0], coords[2][1]))
        screen.blit(image_house, (coords[5][0], coords[5][1]))
        screen.blit(text_game, text_game_rectangle)
        screen.blit(text_wins, text_wins_rectangle)
        screen.blit(text_draws, text_draws_rectangle)
        screen.blit(text_defeats, text_defeats_rectangle)
    elif status == "Home":
        screen.blit(text_start, text_start_rectangle)
        screen.blit(text_quit, text_quit_rectangle)
        screen.blit(image_logo, (20, 20))
        screen.blit(image_hr, (coords[6][0], coords[6][1]))
        screen.blit(image_en, (coords[7][0], coords[7][1]))
        screen.blit(image_it, (coords[8][0], coords[8][1]))

        screen.blit(image_nl, (coords[9][0], coords[9][1]))
        screen.blit(image_ua, (coords[10][0], coords[10][1]))
        screen.blit(image_pl, (coords[11][0], coords[11][1]))

        screen.blit(image_fr, (coords[12][0], coords[12][1]))
        screen.blit(image_de, (coords[13][0], coords[13][1]))
        screen.blit(image_pe, (coords[14][0], coords[14][1]))

    if debug and status == "Main":
        screen.blit(text_rock, text_rock_rectangle)
        screen.blit(text_scissors, text_scissors_rectangle)
        screen.blit(text_paper, text_paper_rectangle)
        screen.blit(text_debug, text_debug_rectangle)
        screen.blit(text_seed, text_seed_rectangle)
        if data["pl_r"] + data["pl_p"] + data["pl_s"] > 0:
            screen.blit(text_rockP, text_rockP_rectangle)
            screen.blit(text_scissorsP, text_scissorsP_rectangle)
            screen.blit(text_paperP, text_paperP_rectangle)

    if cheats and status == "Main":  # Uhmmmm hehe
        screen.blit(text_cheats0, text_cheats0_rectangle)
        screen.blit(text_cheats1, text_cheats1_rectangle)
        screen.blit(text_cheats2, text_cheats2_rectangle)
    # Spremanje u data.txt
    data["seed"] = seed
    with open("data.txt", "w") as f:
        f.write(str(data))

    pygame.display.update()

print("Never gonna give you up!")
