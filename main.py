import pygame
import math
import random
from pygame import mixer
import time

pygame.init()
# екран
screen = pygame.display.set_mode((800, 600))
starting = True
clock = pygame.time.Clock()

# Задній фон
backround = pygame.image.load('backround.jpg')
# Додайте новий фон
transformed_background = pygame.image.load('transformed_background.jpg')

# Музика заднього фона
mixer.music.load("backround_music.wav")
mixer.music.play(-1)

# Іконка моєї гри
pygame.display.set_caption("Fearless space")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# Гравець
playerImage = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Противник
enemyImage = []
enemyTransformedImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4

for i in range(num_of_enemies):
    enemyImage.append(pygame.image.load('enemy.png'))
    enemyTransformedImage.append(pygame.image.load('enemy2.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(0, 50))
    enemyX_change.append(1)  # Зменшили швидкість за оссю X
    enemyY_change.append(20)  # Зменшили швидкість за оссю Y

# звук трансформації
transformation_sound = mixer.Sound("transformation.wav")
transformation_sound_played = False

# Пуля
bulletImage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Очки
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# звук програшу
game_over_sound = mixer.Sound("game over sound.wav")
game_over_sound_played = False

# звук перемоги
victory_sound = mixer.Sound("game-won.wav")
victory_sound_played = False

def show_score(x, y):
    score = font.render("Рахунок очків : "+ str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Програш текст
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    global game_over_sound_played
    if not game_over_sound_played:
        mixer.music.stop()
        game_over_sound.play()
        game_over_sound_played = True
    over_text = over_font.render('ГРА ЗАКІНЧЕННА', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Текст перемоги
victory_font = pygame.font.Font('freesansbold.ttf', 64)

def victory_text():
    global victory_sound_played
    if not victory_sound_played:
        mixer.music.stop()
        victory_sound.play()
        victory_sound_played = True
    victory_text = victory_font.render('Перемога!!!', True, (255, 255, 255))
    screen.blit(victory_text, (200, 250))

def player(x, y):
    screen.blit(playerImage, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))

def Collision(enemyX, enemyY, bulletX, bulletY, i):
    distance = math.sqrt (math.pow(enemyX[i]-bulletX, 2) + (math.pow(enemyY[i]-bulletY,2)))
    if distance < 27:
        enemyX[i] = random.randint(0, 736)
        enemyY[i] = random.randint(50, 150)
        return True
    else:
        return False

# ігровий цикл
start_ticks = None  # визначаємо змінну для зберігання часу початку трансформації
while starting:
    # Ігровий фон 
    screen.fill((3, 6, 26))
    if score_value >= 50:  # якщо очки >= 50, використовуємо новий фон
        screen.blit(transformed_background, (0, 0))
    else:
        screen.blit(backround, (0, 0))
    # ...

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            starting = False
        #Клавіатура
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound("fire sound.wav")
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Рух гравця       
    playerX += playerX_change
  
    if playerX <=0:
        playerX = 0
    elif playerX >=736:
        playerX = 736
    #Рух противника
    for i in range(num_of_enemies):

        # Гра закінченна
        if enemyY[i] > 440 and score_value < 150:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <=0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # Трансформація
        if score_value >= 50 and not transformation_sound_played:
            transformation_sound.play()
            transformation_sound_played = True
            for j in range(num_of_enemies):
                enemyImage[j] = enemyTransformedImage[j]  # змінюємо образ на трансформований
                enemyX_change[j] = enemyX_change[j] * 1.8  # швидкість на 1,8 рази
                enemyY_change[j] = enemyY_change[j] * 1.8  # швидкість на 1,8 рази
            mixer.music.stop()  # зупинити музику
            start_ticks = pygame.time.get_ticks()  # отримуємо поточний час

        # перевіряємо, чи минуло 4 секунди після початку трансформації
        if start_ticks:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds >= 4:  # якщо минуло 4 або більше секунд
                mixer.music.load("backround2.wav")
                mixer.music.play(-1) 
                start_ticks = None

        # колізія
        collision = Collision(enemyX, enemyY, bulletX, bulletY, i)
        if collision:
            explosion_Sound = mixer.Sound("boom sound.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)

        if score_value >= 150:  # Перемога
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            victory_text()
            break

        enemy(enemyX[i], enemyY[i], i)

    # Рух Пулі
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
        
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()