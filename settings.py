import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
PLAYER_NAME = ''
GAME_START = True  # suppose to be True in game start
GAME_ACTIVE = False  # suppose to be False in game start
GAME_OPTION = False  # suppose to be False in game start
GAME_OVER = False  # suppose to be False in game start
GAME_WIN = False  # suppose to be False in game start
SCORE_BOARD = False # suppose to be False in game start
PLAYER_COOLDOWN = 300
SCORE = 0
DIFFICULTY = 'easy'
if DIFFICULTY == 'easy':
    ENEMY_SPAWN = 1000
    ENEMY_COOLDOWN = 700
    BOSS_COOLDOWN = 300
    BOSS_HEALTH = 5
    BOSS_SPAWN_SCORE = 10
SOUND = True
MUSIC = True




