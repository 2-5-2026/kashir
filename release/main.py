import pygame
import json
import sys
from pygame import mixer

# --- Konstante ---
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BACKGROUND_COLOR = (254, 238, 145)
BUTTON_COLOR = (204, 197, 197)
BUTTON_HOVER_COLOR = (179, 170, 170)
FPS = 60

DEFAULT_DATA = {
    "pl_Wins": 0, "ai_Wins": 0, "draws": 0,
    "pl_r": 0, "pl_p": 0, "pl_s": 0,
    "seed": 0, "lang": "hr"
}

REQUIRED_KEYS = ("pl_Wins", "ai_Wins", "draws", "pl_r", "pl_p", "pl_s", "seed", "lang")

# Koordinate i dimenzije gumba
# 0=kamen, 1=škare, 2=papir, 3=kreni, 4=izađi, 5=kuća, 6=hr, 7=en, 8=it
COORDS = [
    (614, 780), (864, 780), (1114, 780),
    (1400, 500), (1400, 800), (1800, 50),
    (1200, 32), (1400, 32), (1600, 32)
]
BUTTON_RADII = [
    (96, 96), (96, 96), (96, 96),
    (200, 100), (200, 100), (48, 48),
    (96, 48), (96, 48), (96, 48)
]

# --- Jezici ---
LANGUAGES = {
    "hr": ["Kamen: ", "Škare: ", "Papir: ", "Debug", "Kreni", "Izađi",
           "Pobjede: ", "Porazi: ", "Remiziranja: ", "Pobjeda", "Poraz", "Remi",
           "Seed: ", "Udio kamen: ", "Udio škare: ", "Udio papir: "],
    "en": ["Rock: ", "Scissors: ", "Paper: ", "Debug", "Start", "Quit",
           "Wins: ", "Defeats: ", "Draws: ", "Win", "Defeat", "Draw",
           "Seed: ", "Rock percentage: ", "Scissors percentage: ", "Paper percentage: "],
    "it": ["Sasso: ", "Forbici: ", "Carta: ", "Debug", "Inizia", "Esci",
           "Vittorie: ", "Perdite: ", "Pareggi: ", "Vittoria", "Perdita", "Pareggio",
           "Seed: ", "Percentuale sasso: ", "Percentuale forbici: ", "Percentuale carta: "],
}

IMAGE_MAP = {}  # popunjava se nakon pygame.init()


# --- Funkcije ---

def check_click(button, mouse):
    """Provjerava je li miš unutar granica gumba."""
    x, y = COORDS[button]
    w, h = BUTTON_RADII[button]
    return x <= mouse[0] <= x + w * 2 and y <= mouse[1] <= y + h * 2


def load_data():
    """Učitava stanje igre iz data.txt (JSON format)."""
    try:
        with open("data.txt") as f:
            data = json.loads(f.read())
            if not all(k in data for k in REQUIRED_KEYS):
                return dict(DEFAULT_DATA)
            return data
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return dict(DEFAULT_DATA)


def save_data(data):
    """Sprema stanje igre u data.txt."""
    with open("data.txt", "w") as f:
        json.dump(data, f)


def pseudo_random(seed):
    """Linearni kongruencijski generator (LCG)."""
    return (1664525 * seed + 1013904223) % (2 ** 32)


def ai_pick_move(seed, data, cheats_input=None):
    """
    AI protivnika. Analizira igračeve poteze i bira protupotez.
    Ako je cheats_input zadan (0/1/2), simulira bez promjene stanja.
    Vraća (novi_seed, ai_potez) ili samo ai_potez ako je cheats.
    """
    rock = data["pl_r"]
    scissors = data["pl_s"]
    paper = data["pl_p"]

    if cheats_input is not None:
        counts = [rock, scissors, paper]
        counts[cheats_input] += 1
        rock, scissors, paper = counts

    moves = [rock, scissors, paper]
    most_played = moves.index(max(moves))
    counter_pick = (most_played - 1) % 3
    total = sum(moves)
    maximum = max(moves)

    if total == 0:
        seed = pseudo_random(seed)
        ai_move = seed % 3
    else:
        ratio = maximum / total
        # Određujemo prag: što dominantniji potez, veća šansa za counter
        if ratio >= 0.8:
            threshold = 5  # 5/7 = ~71% counter
            modulo = 7
        elif ratio >= 0.65:
            threshold = 4  # 4/6 = ~67% counter
            modulo = 6
        elif ratio >= 0.5:
            threshold = 3  # 3/5 = 60% counter
            modulo = 5
        elif ratio >= 0.4:
            threshold = 2  # 2/4 = 50% counter
            modulo = 4
        else:
            threshold = 0  # potpuno nasumično
            modulo = 3

        seed = pseudo_random(seed)
        rng = seed % modulo

        if threshold > 0 and rng >= (modulo - threshold):
            ai_move = counter_pick
        else:
            # Nasumični odabir - novi seed za ravnomjernu distribuciju
            seed = pseudo_random(seed)
            ai_move = seed % 3

    if cheats_input is not None:
        return ai_move
    else:
        return seed, ai_move


def check_game_result(player, ai_move):
    """Vraća rezultat: 'win', 'lose' ili 'draw'."""
    if player == ai_move:
        return "draw"
    elif (player + 1) % 3 == ai_move:
        return "win"
    else:
        return "lose"


def result_color(result):
    """Vraća boju za rezultat."""
    if result == "win":
        return (0, 255, 0)
    elif result == "lose":
        return (255, 0, 0)
    else:
        return (255, 100, 0)


def result_text(result, lang):
    """Vraća lokalizirani tekst za rezultat."""
    if result == "win":
        return lang[9]
    elif result == "lose":
        return lang[10]
    else:
        return lang[11]


# --- Inicijalizacija ---
pygame.init()
mixer.init()

clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 64)
font2 = pygame.font.Font(pygame.font.get_default_font(), 32)

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kashir")

# Učitavanje slika
image_rock = pygame.image.load("rock.png").convert_alpha()
image_scissors = pygame.image.load("scissors.png").convert_alpha()
image_paper = pygame.image.load("paper.png").convert_alpha()
image_house = pygame.image.load("house.png").convert_alpha()
image_hr = pygame.image.load("flag_hr.png").convert_alpha()
image_en = pygame.image.load("flag_br.png").convert_alpha()
image_it = pygame.image.load("flag_it.png").convert_alpha()

image_rock = pygame.transform.scale(image_rock, (BUTTON_RADII[0][0] * 2, BUTTON_RADII[0][1] * 2))
image_scissors = pygame.transform.scale(image_scissors, (BUTTON_RADII[1][0] * 2, BUTTON_RADII[1][1] * 2))
image_paper = pygame.transform.scale(image_paper, (BUTTON_RADII[2][0] * 2, BUTTON_RADII[2][1] * 2))
image_house = pygame.transform.scale(image_house, (BUTTON_RADII[5][0] * 2, BUTTON_RADII[5][1] * 2))

IMAGE_MAP = {"rock": image_rock, "scissors": image_scissors, "paper": image_paper}
MOVE_NAMES = ["rock", "scissors", "paper"]

# Učitavanje glazbe
music_loaded = False
try:
    mixer.music.load("music.mp3")
    mixer.music.set_volume(1.0)
    music_loaded = True
except pygame.error:
    print("Upozorenje: music.mp3 nije pronađena, igra nastavlja bez glazbe.")

# --- Stanje igre ---
data = load_data()
seed = data["seed"]
lang = LANGUAGES.get(data["lang"], LANGUAGES["hr"])
status = "Home"       # "Home" ili "Main"
played = False
player_pick = None
image_ai = None
text_game = font.render("", 32, (0, 0, 0))
text_game_rect = text_game.get_rect()

debug = False
cheats = False
combo = 0
timer = 0
typed = False
toggled = False
toggled2 = False
state_changed = True  # za spremanje samo kad treba

# Keširani tekst objekti
cached_texts = {}


def update_cached_texts():
    """Ažurira keširane tekstove za rezultate."""
    cached_texts["wins"] = font.render(lang[6] + str(data["pl_Wins"]), 32, (0, 255, 0))
    cached_texts["draws"] = font.render(lang[8] + str(data["draws"]), 32, (255, 100, 0))
    cached_texts["defeats"] = font.render(lang[7] + str(data["ai_Wins"]), 32, (255, 0, 0))
    cached_texts["start"] = font.render(lang[4], 32, (0, 0, 0))
    cached_texts["quit"] = font.render(lang[5], 32, (0, 0, 0))
    cached_texts["start_rect"] = cached_texts["start"].get_rect(center=(1600, 600))
    cached_texts["quit_rect"] = cached_texts["quit"].get_rect(center=(1600, 900))


update_cached_texts()


def play_move(move_index):
    """Igrač odabire potez (0=kamen, 1=škare, 2=papir)."""
    global seed, played, player_pick, image_ai, text_game, text_game_rect, state_changed

    keys_map = ["pl_r", "pl_s", "pl_p"]
    data[keys_map[move_index]] += 1

    seed, ai_move = ai_pick_move(seed, data)

    result = check_game_result(move_index, ai_move)
    color = result_color(result)
    text = result_text(result, lang)

    if result == "win":
        data["pl_Wins"] += 1
    elif result == "lose":
        data["ai_Wins"] += 1
    else:
        data["draws"] += 1

    text_game = font.render(text, 32, color)
    text_game_rect = text_game.get_rect(center=(960, 380))

    player_pick = MOVE_NAMES[move_index]
    image_ai = pygame.image.load(MOVE_NAMES[ai_move] + ".png").convert_alpha()
    image_ai = pygame.transform.scale(image_ai, (BUTTON_RADII[1][0] * 2, BUTTON_RADII[1][1] * 2))

    played = True
    state_changed = True
    update_cached_texts()


# --- Glavni loop ---
while True:
    mouse = pygame.mouse.get_pos()

    # Glazba
    if music_loaded and not mixer.music.get_busy():
        mixer.music.play()

    # Događaji
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            data["seed"] = seed
            save_data(data)
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if status == "Main":
                for i in range(3):
                    if check_click(i, mouse):
                        play_move(i)
                if check_click(5, mouse):
                    status = "Home"
                    played = False
                    text_game = font.render("", 32, (0, 0, 0))

            elif status == "Home":
                if check_click(3, mouse):
                    status = "Main"
                if check_click(4, mouse):
                    data["seed"] = seed
                    save_data(data)
                    pygame.quit()
                    sys.exit()
                for idx, lang_code in [(6, "hr"), (7, "en"), (8, "it")]:
                    if check_click(idx, mouse):
                        lang = LANGUAGES[lang_code]
                        data["lang"] = lang_code
                        state_changed = True
                        update_cached_texts()

    # Tipke
    keys = pygame.key.get_pressed()

    # Jačina glazbe
    if music_loaded:
        if keys[pygame.K_UP]:
            mixer.music.set_volume(min(1.0, mixer.music.get_volume() + 0.01))
        if keys[pygame.K_DOWN]:
            mixer.music.set_volume(max(0.0, mixer.music.get_volume() - 0.01))

    # Tipkovnički prečaci za poteze
    if status == "Main" and not typed:
        if keys[pygame.K_1]:
            play_move(0)
            typed = True
        elif keys[pygame.K_2]:
            play_move(1)
            typed = True
        elif keys[pygame.K_3]:
            play_move(2)
            typed = True

    if not keys[pygame.K_1] and not keys[pygame.K_2] and not keys[pygame.K_3]:
        typed = False

    # Cheat combo: K-I-F-L-A
    if timer > 0:
        timer -= 1
    else:
        combo = 0

    if keys[pygame.K_k] and combo == 0:
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
            cheats = not cheats

    if not keys[pygame.K_a]:
        toggled = False

    # Debug toggle
    if keys[pygame.K_d]:
        if not toggled2:
            toggled2 = True
            debug = not debug
    else:
        toggled2 = False

    # --- Renderiranje ---
    screen.fill(BACKGROUND_COLOR)

    if status == "Main":
        # Gumbi za poteze
        for i in range(3):
            color = BUTTON_HOVER_COLOR if check_click(i, mouse) else BUTTON_COLOR
            pygame.draw.rect(screen, color, [COORDS[i][0], COORDS[i][1],
                             BUTTON_RADII[i][0] * 2, BUTTON_RADII[i][1] * 2])

        # Gumb kuća
        color = BUTTON_HOVER_COLOR if check_click(5, mouse) else BUTTON_COLOR
        pygame.draw.rect(screen, color, [COORDS[5][0], COORDS[5][1],
                         BUTTON_RADII[5][0] * 2, BUTTON_RADII[5][1] * 2])

        # Slike poteza
        screen.blit(image_rock, COORDS[0])
        screen.blit(image_scissors, COORDS[1])
        screen.blit(image_paper, COORDS[2])
        screen.blit(image_house, COORDS[5])

        # Prikaz igračevog i AI odabira
        if played and player_pick:
            pygame.draw.rect(screen, BUTTON_COLOR, [COORDS[1][0], COORDS[1][1] - 300,
                             BUTTON_RADII[1][0] * 2, BUTTON_RADII[1][1] * 2])
            screen.blit(IMAGE_MAP[player_pick], (COORDS[1][0], COORDS[1][1] - 300))

        if played and image_ai:
            pygame.draw.rect(screen, BUTTON_COLOR, [COORDS[1][0], 100,
                             BUTTON_RADII[1][0] * 2, BUTTON_RADII[1][1] * 2])
            screen.blit(image_ai, (COORDS[1][0], 100))

        # Rezultat i statistika
        screen.blit(text_game, text_game_rect)
        screen.blit(cached_texts["wins"], (50, 64))
        screen.blit(cached_texts["draws"], (50, 128))
        screen.blit(cached_texts["defeats"], (50, 196))

        # Debug prikaz
        if debug:
            screen.blit(font2.render(lang[3], 32, (0, 0, 0)), (50, 350))
            screen.blit(font2.render(lang[0] + str(data["pl_r"]), 32, (0, 0, 0)), (50, 400))
            screen.blit(font2.render(lang[1] + str(data["pl_s"]), 32, (0, 0, 0)), (50, 450))
            screen.blit(font2.render(lang[2] + str(data["pl_p"]), 32, (0, 0, 0)), (50, 500))
            screen.blit(font2.render(lang[12] + str(seed), 32, (0, 0, 0)), (50, 550))
            total_moves = data["pl_r"] + data["pl_s"] + data["pl_p"]
            if total_moves > 0:
                screen.blit(font2.render(lang[13] + f"{100 * data['pl_r'] / total_moves:.2f}%", 32, (0, 0, 0)), (50, 600))
                screen.blit(font2.render(lang[14] + f"{100 * data['pl_s'] / total_moves:.2f}%", 32, (0, 0, 0)), (50, 650))
                screen.blit(font2.render(lang[15] + f"{100 * data['pl_p'] / total_moves:.2f}%", 32, (0, 0, 0)), (50, 700))

        # Cheat prikaz
        if cheats:
            for i in range(3):
                ai_move = ai_pick_move(seed, data, cheats_input=i)
                result = check_game_result(i, ai_move)
                color = result_color(result)
                text = result_text(result, lang)
                rendered = font2.render(text, 32, color)
                rect = rendered.get_rect(center=(COORDS[i][0] + BUTTON_RADII[i][0], COORDS[i][1] + 250))
                screen.blit(rendered, rect)

    elif status == "Home":
        # Gumbi kreni/izađi
        for i in (3, 4):
            color = BUTTON_HOVER_COLOR if check_click(i, mouse) else BUTTON_COLOR
            pygame.draw.rect(screen, color, [COORDS[i][0], COORDS[i][1],
                             BUTTON_RADII[i][0] * 2, BUTTON_RADII[i][1] * 2])

        screen.blit(cached_texts["start"], cached_texts["start_rect"])
        screen.blit(cached_texts["quit"], cached_texts["quit_rect"])
        screen.blit(icon, (20, 20))
        screen.blit(image_hr, COORDS[6])
        screen.blit(image_en, COORDS[7])
        screen.blit(image_it, COORDS[8])

    # Jačina glazbe
    if music_loaded:
        vol_text = font2.render(f"Jačina glazbe: {mixer.music.get_volume() * 100:.1f}%", 32, (0, 0, 0))
        vol_rect = vol_text.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))
        screen.blit(vol_text, vol_rect)

    # Spremanje samo kad je potrebno
    if state_changed:
        data["seed"] = seed
        save_data(data)
        state_changed = False

    pygame.display.update()
    clock.tick(FPS)
