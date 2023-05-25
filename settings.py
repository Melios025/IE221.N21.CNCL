import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_START = True  # suppose to be True in game start
GAME_ACTIVE = False  # suppose to be False in game start
GAME_OPTION = False  # suppose to be False in game start
GAME_OVER = False  # suppose to be False in game start
GAME_WIN = False  # suppose to be False in game start
PLAYER_COOLDOWN = 300
SCORE = 0
DIFFICULTY = 'hard'

if DIFFICULTY == 'easy':
    ENEMY_SPAWN = 1000
    ENEMY_COOLDOWN = 700
    BOSS_COOLDOWN = 300
    BOSS_HEALTH = 5
    BOSS_SPAWN_SCORE = 10
if DIFFICULTY == 'medium':
    ENEMY_SPAWN = 750
    ENEMY_COOLDOWN = 500
    BOSS_COOLDOWN = 250
    BOSS_HEALTH = 10
    BOSS_SPAWN_SCORE = 15
if DIFFICULTY == 'hard':
    ENEMY_SPAWN = 500
    ENEMY_COOLDOWN = 250
    BOSS_COOLDOWN = 200
    BOSS_HEALTH = 20
    BOSS_SPAWN_SCORE = 20
SOUND = True
MUSIC = True

# f = open('/setting.txt', 'a')
# print(f.read())
