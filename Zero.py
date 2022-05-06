import pygame
import random
from pygame import mixer

# from pygame.constants import K_LEFT, K_RIGHT

# Initialize the pygame 
pygame.init()

# Create a screen
screen = pygame.display.set_mode((800,600))

# Title and Icon
pygame.display.set_caption("Zero")
icon = pygame.image.load("eternity.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("Game1.jpg")
# Background music 
mixer.music.load('Background_music.mp3')
mixer.music.play(-1)


# Player
playerImg = pygame.image.load("Spiderman.png")
playerX = 368
playerY = 500
playerX_change = 0
# playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("Hulk.png"))
    enemyX.append(random.randint(10,726))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.4)
    enemyY_change.append(40)

# Web
webImg = pygame.image.load("Spider-web (1).png")
webX = 368
webY = 500
webX_change = 0
webY_change = 2
web_state = "ready"

# Score 
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score():
    score = font.render('Score : ' + str(score_value) , True , (0,0,0) )
    screen.blit(score , (textX , textY))

def game_over_text():
    over_text = over_font.render("GAME OVER" , True , (0,0,0) )
    screen.blit(over_text , (200,250))

def player(x,y):
    screen.blit(playerImg ,( x , y ))

def enemy(x,y,i):
    screen.blit(enemyImg[i] ,( x , y ))

def fire_web(x,y):
    global web_state 
    web_state = "fire"
    screen.blit(webImg,(x+16,y+10))

def isCollision(enemyX,enemyY,webX,webY):
    distance = ((enemyX - webX)**2 + (enemyY - webY)**2)**0.5
    if distance <= 27 :
        return True
    else :
        return False


# Game loop
running = True
while running:
    screen.fill((0,200,200))
    screen.blit(background,(-30,-15))
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
                playerX_change = -0.6
                
            if event.key == pygame.K_RIGHT :
                playerX_change = 0.6
            
            if event.key == pygame.K_SPACE :
                if web_state == "ready":
                    web_sound = mixer.Sound("web_sound.wav")
                    web_sound.play()
                    webX = playerX
                    fire_web(webX,webY)
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_change = 0
                # playerY_change = 0


    # Creating boundaries
    playerX += playerX_change 
    # playerY += playerY_change 
    if playerX <= 0:
        playerX = 0
    elif playerX >=736 :
        playerX = 736
    # if playerY <= 0:
    #     playerY = 0
    # elif playerY >=736 :
    #     playerY = 736

    # Movements of enemy 
    for i in range(num_of_enemies):

        if enemyY[i] >= 460 :
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
            # defeated_sound = mixer.Sound("Defeated.wav")
            # defeated_sound.play()
            # print(score_value) 
            # running = False  

        enemyX[i] += enemyX_change[i] 
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736 :
            enemyX_change[i] = -0.4
            enemyY[i] += enemyY_change[i]


        # Collision 
        collision = isCollision(enemyX[i],enemyY[i],webX,webY)
        if collision :
            explosion_sound = mixer.Sound("Enemy_defeated.wav")
            explosion_sound.play()
            webY = 500
            web_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(10,726)
            enemyY[i] = random.randint(50,150)

            

    # Web movement
    if webY <= 0 :
        webY = 500
        web_state = "ready"

    if web_state == "fire":
        fire_web(webX,webY)
        webY -= webY_change

    # # Collision 
    # collision = isCollision(enemyX,enemyY,webX,webY)
    # if collision :
    #     webY = 500
    #     web_state = "ready"
    #     score += 1
    #     enemyX = random.randint(10,726)
    #     enemyY = random.randint(50,150)

    player(playerX,playerY)
    for i in range(num_of_enemies):
        enemy(enemyX[i],enemyY[i],i)
    show_score()
    pygame.display.update()

    
# print(score)