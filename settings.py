import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_START = True
GAME_ACTIVE = False
GAME_OVER = False
GAME_WIN = False
BOSS_HEALTH = 5
PLAYER_COOLDOWN = 300
ENEMY_COOLDOWN = 700
BOSS_COOLDOWN = 300
SCORE = 0
BOSS_SPAWN_SCORE = 10

# f = open('/setting.txt', 'a')
# print(f.read())