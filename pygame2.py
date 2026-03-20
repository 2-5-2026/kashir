import pygame
import sys

# 1. INITIALIZATION
pygame.init()

# Set to Fullscreen (or use (800, 600) for testing)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Kamen, Škare, Papir")

# 2. SETUP ASSETS (Load things ONCE here)
width = screen.get_width()
height = screen.get_height()

# Colors
bg_color = (254, 238, 145)  # Your yellow background
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

# Logo setup
try:
    original_logo = pygame.image.load('logo.png')
    logo = pygame.transform.scale(original_logo, (500, 371))
except:
    print("Logo file not found, skipping logo load.")
    logo = None

# Font setup
smallfont = pygame.font.SysFont('Corbel', 35)
text = smallfont.render('quit', True, "white")

# 3. THE ONE AND ONLY MAIN LOOP
while True:
    # A. Get Input
    mouse = pygame.mouse.get_pos()
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if ev.type == pygame.MOUSEBUTTONDOWN:
            # Quit Button Logic
            if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
                pygame.quit()
                sys.exit()

    # B. DRAWING (Order matters!)
    
    # 1st: Background
    screen.fill(bg_color) 

    # 2nd: Logo
    if logo:
        screen.blit(logo, (660, 50))

    # 3rd: Button Rectangle (Hover effect)
    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
        pygame.draw.rect(screen, color_light, [width/2, height/2, 140, 40])
    else:
        pygame.draw.rect(screen, color_dark, [width/2, height/2, 140, 40])

    # 4th: Text on top of button
    screen.blit(text, (width/2 + 40, height/2))
    
    # 5th: Push everything to the monitor
    pygame.display.update()
