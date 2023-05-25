import pygame
import sys
from enemies import Enemies
from player import Player
from enemies import Boss
from random import choice
from text import Text
from button import Button

from settings import *

class Game():
    def __init__(self):
        
        # Player
        self.player_sprite = Player()
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

        # Enemy
        self.enemies = pygame.sprite.Group()

        # Boss
        self.boss_sprite = Boss()
        self.boss = pygame.sprite.GroupSingle(self.boss_sprite)

        # Time
        self.time = 0

        # Text
        self.text = pygame.sprite.Group()

        self.background_surface = pygame.image.load(
            'graphics/bg.jpg').convert_alpha()
        self.background_rect = self.background_surface.get_rect(
            center=(640, 360))

        # Background for game start
        self.background_surface_start = pygame.image.load(
            'graphics/bg_start.jpg').convert_alpha()
        self.background_surface_start = pygame.transform.rotozoom(
            self.background_surface_start, 0, 0.3)
        self.background_rect_start = self.background_surface.get_rect(
            center=(640, 360))

        # Background for game over
        self.background_surface_over = pygame.image.load(
            'graphics/bg_over.jpg').convert_alpha()
        self.background_surface_over = pygame.transform.rotozoom(
            self.background_surface_over, 0, 0.3)
        self.background_rect_over = self.background_surface_over.get_rect(
            center=(640, 360))

        # Buttons
        self.setting_easy = Button(None, (500, 300), 'Easy', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'red', 'red')
        self.setting_medium = Button(None, (500, 300), 'Medium', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'red', 'red')
        self.setting_hard = Button(None, (500, 300), 'Hard', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'red', 'red')
        self.setting_sound = Button(None, (500, 400), 'Sound', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'red', 'red')
        self.setting_music = Button(None, (640, 400), 'Music', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'red', 'red')

    def check_collide(self):
        global GAME_OVER, GAME_ACTIVE, SCORE
        # Colide from bullet to enemy
        if self.player_sprite.bullets:
            for bullet in self.player_sprite.bullets:
                if pygame.sprite.spritecollide(bullet, self.enemies, True):
                    bullet.kill()
                    SCORE += 1

        # Colide from player to enemy
        if pygame.sprite.spritecollide(self.player_sprite, self.enemies, False):
            GAME_ACTIVE = False
            GAME_OVER = True

        # Colide from bullet to player
        if self.enemies:
            for enemy in self.enemies:
                for bullet in enemy.bullets:
                    if pygame.sprite.spritecollide(bullet, self.player, False):
                        bullet.kill()
                        GAME_ACTIVE = False
                        GAME_OVER = True

    def check_collide_boss(self):
        global GAME_ACTIVE, GAME_OVER
        if self.player_sprite.bullets:
            for bullet in self.player_sprite.bullets:
                if pygame.sprite.spritecollide(bullet, self.boss, False):
                    bullet.kill()
                    self.boss_sprite.health -= 1

        if pygame.sprite.spritecollide(self.player_sprite, self.boss, False):
            GAME_ACTIVE = False
            GAME_OVER = True

        if self.boss_sprite.bullets:
            for bullet in self.boss_sprite.bullets:
                if pygame.sprite.spritecollide(bullet, self.player, False):
                    bullet.kill()
                    GAME_ACTIVE = False
                    GAME_OVER = True

    def display_score(self):
        if GAME_ACTIVE:
            score_display = True
        else:
            score_display = False
        self.text.add(
            Text(40, f'Score: {SCORE}', 'White', (60, 20), score_display))

    def display_health(self):
        if GAME_ACTIVE:
            health_display = True
        else:
            health_display = False
        self.text.add(Text(
            40, f'Health: {self.boss_sprite.health}', 'White', (55, 50), health_display))

    def game_win_condition(self):
        global GAME_ACTIVE, GAME_WIN
        if self.boss_sprite.health <= 0:
            GAME_ACTIVE = False
            GAME_WIN = True

    def game_active(self):
        # Draw background
        screen.blit(self.background_surface, self.background_rect)

        # Draw player
        self.player_sprite.bullets.draw(screen)
        self.player.draw(screen)
        self.player.update()

        # Draw enemy
        for enemy in self.enemies:
            enemy.bullets.draw(screen)
        self.enemies.draw(screen)
        self.enemies.update()

        # Draw boss
        if SCORE >= BOSS_SPAWN_SCORE:
            self.boss.draw(screen)
            self.enemies.empty()
            self.boss.update()
            if self.boss_sprite.rect.top <= 0:
                self.boss_sprite.rect.y += 5
            else:
                self.boss_sprite.bullets.draw(screen)
        # Check collide
        self.check_collide()
        if SCORE >= BOSS_SPAWN_SCORE:
            self.check_collide_boss()

        # Draw tips
        current_time = pygame.time.get_ticks()
        if current_time - self.time < 3000:
            tips_display = True
            self.text.add(Text(
                30, f'Tips: Try to reach {BOSS_SPAWN_SCORE} point to meet the boss level', 'White', (640, 50), tips_display))
        else:
            tips_display = False

        # Display score
        self.display_score()
        if SCORE >= BOSS_SPAWN_SCORE:
            self.display_health()
        self.text.draw(screen)
        self.text.update()

        # Game win
        self.game_win_condition()
        if not GAME_ACTIVE:
            return

    def game_main_menu(self):
        # Draw background
        screen.blit(self.background_surface_start, self.background_rect_start)

        self.mouse_pos = pygame.mouse.get_pos()
        if GAME_START:
            menu_text_display = True
        else:
            menu_text_display = False
        self.text.add(Text(100, 'My Final Project', 'White',
                      (640, 130), menu_text_display))
        self.text.draw(screen)
        self.text.update()

        # Play button
        self.play_button = Button(None, (640, 330), 'PLAY', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'White', 'red')
        self.play_button.changeColor(self.mouse_pos)
        self.play_button.update(screen)

        # Setting button
        self.setting_button = Button(None, (640, 400), 'SETTING', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'White', 'red')
        self.setting_button.changeColor(self.mouse_pos)
        self.setting_button.update(screen)

        # Quit button
        self.quit_button = Button(None, (640, 470), 'QUIT', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'White', 'red')
        self.quit_button.changeColor(self.mouse_pos)
        self.quit_button.update(screen)
        if not GAME_START:
            return

    def game_over_menu(self):
        screen.blit(self.background_surface_over, self.background_rect_over)
        self.mouse_pos = pygame.mouse.get_pos()
        if GAME_OVER:
            text_display = True
        else:
            text_display = False
        self.text.add(
            Text(100, 'GAME OVER', 'white', (640, 100), text_display))
        self.text.add(
            Text(80, f'Your score: {SCORE}', 'white', (640, 170), text_display))
        self.text.draw(screen)
        self.text.update()

        # Restart button
        self.restart_button = Button(None, (640, 330), 'RESTART', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'white', 'red')
        self.restart_button.changeColor(self.mouse_pos)
        self.restart_button.update(screen)

        # Main menu button
        self.main_menu_button = Button(None, (640, 400), 'MAIN MENU', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'white', 'red')
        self.main_menu_button.changeColor(self.mouse_pos)
        self.main_menu_button.update(screen)

        # Quit button
        self.quit_button.changeColor(self.mouse_pos)
        self.quit_button.update(screen)

        if not GAME_OVER:
            return

    def game_win_menu(self):
        if GAME_WIN:
            text_display = True
        else:
            text_display = False

        self.text.add(
            Text(100, 'GAME WIN !!!', 'white', (640, 340), text_display))
        self.text.add(
            Text(80, f'Your score: {SCORE}', 'white', (640, 400), text_display))
        self.text.draw(screen)
        self.text.update()
        if not GAME_WIN:
            return

    def game_restart(self, back_main):
        global SCORE
        SCORE = 0
        game.time = pygame.time.get_ticks()
        self.enemies.empty()
        self.boss_sprite.bullets.empty()
        self.boss_sprite.rect.x = 640
        self.boss_sprite.rect.y = -100

        self.player_sprite.bullets.empty()
        if not back_main:
            pygame.mouse.set_pos(640, 650)

    def game_option_menu(self):
        self.mouse_pos = pygame.mouse.get_pos()
        if GAME_OPTION:
            text_display = True
        else:
            text_display = False
        # Difficulty option
        self.text.add(
            Text(50, 'Game DIFFICULTY: ', 'black', (500, 250), text_display))
        if DIFFICULTY == 'easy':
            self.setting_easy = Button(None, (500, 300), 'Easy', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'red', 'red')
        else:
            self.setting_easy = Button(None, (500, 300), 'Easy', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'black', 'red')

        if DIFFICULTY == 'medium':
            self.setting_medium = Button(None, (640, 300), 'Medium', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'red', 'red')
        else:
            self.setting_medium = Button(None, (640, 300), 'Medium', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'black', 'red')

        if DIFFICULTY == 'hard':
            self.setting_hard = Button(None, (780, 300), 'Hard', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'red', 'red')
        else:
            self.setting_hard = Button(None, (780, 300), 'Hard', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'black', 'red')

        # Sound and music

        self.text.add(
            Text(50, 'Sound and music: ', 'black', (500, 350), text_display))
        if SOUND == True:
            self.setting_sound = Button(None, (500, 400), 'Sound', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'red', 'red')
        else:
            self.setting_sound = Button(None, (500, 400), 'Sound', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'black', 'red')
        if MUSIC == True:
            self.setting_music = Button(None, (640, 400), 'Music', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'red', 'red')
        else:
            self.setting_music = Button(None, (640, 400), 'Music', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'black', 'red')

        self.close_button = Button(None, (1230, 50), 'X', pygame.font.Font(
            'font/Pixeltype.ttf', 100), 'black', 'red')

        self.close_button.update(screen)
        self.setting_easy.update(screen)
        self.setting_medium.update(screen)
        self.setting_hard.update(screen)
        self.setting_sound.update(screen)
        self.setting_music.update(screen)
        self.text.draw(screen)
        self.text.update()


if __name__ == '__main__':
    pygame.init()
    timer = pygame.USEREVENT + 1
    pygame.time.set_timer(timer, ENEMY_SPAWN)
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if GAME_START:
                if event.type == pygame.MOUSEBUTTONUP:
                    if game.play_button.checkForInput(game.mouse_pos):
                        pygame.mouse.set_pos(640, 600)
                        GAME_START = False
                        GAME_ACTIVE = True
                    if game.setting_button.checkForInput(game.mouse_pos):
                        GAME_START = False
                        GAME_OPTION = True
                    if game.quit_button.checkForInput(game.mouse_pos):
                        pygame.quit()
                        sys.exit()
            if GAME_OPTION:
                 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.close_button.checkForInput(game.mouse_pos):
                        GAME_OPTION = False
                        GAME_START = True
                    if game.setting_easy.checkForInput(game.mouse_pos) and DIFFICULTY != 'easy':
                        DIFFICULTY = 'easy'
                        ENEMY_SPAWN = 1000
                        ENEMY_COOLDOWN = 700
                        BOSS_COOLDOWN = 300
                        BOSS_HEALTH = 5
                        BOSS_SPAWN_SCORE = 10

                    if game.setting_medium.checkForInput(game.mouse_pos) and DIFFICULTY != 'medium':
                        DIFFICULTY = 'medium'
                        ENEMY_SPAWN = 750
                        ENEMY_COOLDOWN = 500
                        BOSS_COOLDOWN = 250
                        BOSS_HEALTH = 10
                        BOSS_SPAWN_SCORE = 15

                    if game.setting_hard.checkForInput(game.mouse_pos) and DIFFICULTY != 'hard':
                        DIFFICULTY = 'hard'
                        ENEMY_SPAWN = 500
                        ENEMY_COOLDOWN = 1
                        BOSS_COOLDOWN = 200
                        BOSS_HEALTH = 20
                        BOSS_SPAWN_SCORE = 20
                        game.enemies.update()

                    if game.setting_sound.checkForInput(game.mouse_pos) and SOUND != True:
                        SOUND = True
                    elif game.setting_sound.checkForInput(game.mouse_pos) and SOUND != False:
                        SOUND = False

                    if game.setting_music.checkForInput(game.mouse_pos) and MUSIC != True:
                        MUSIC = True
                    elif game.setting_music.checkForInput(game.mouse_pos) and MUSIC != False:
                        MUSIC = False
                    
            if GAME_ACTIVE:
                if event.type == timer:
                    if SCORE < BOSS_SPAWN_SCORE:
                        game.enemies.add(
                            Enemies(choice(['blue', 'yellow', 'blue'])))
            if GAME_OVER:
                if event.type == pygame.MOUSEBUTTONUP:
                    if game.restart_button.checkForInput(game.mouse_pos):
                        game.game_restart(False)
                        GAME_OVER = False
                        GAME_ACTIVE = True
                    if game.main_menu_button.checkForInput(game.mouse_pos):
                        game.game_restart(True)
                        GAME_OVER = False
                        GAME_START = True
                    if game.quit_button.checkForInput(game.mouse_pos):
                        pygame.quit()
                        sys.exit()
        # print(CLOCK.get_fps())
        if GAME_START:
            screen.fill('white')
            game.game_main_menu()
        elif GAME_ACTIVE:
            print(DIFFICULTY, game.enemies)
            if game.time == 0:
                game.time = pygame.time.get_ticks()
            game.game_active()
        elif GAME_OPTION:
            print(DIFFICULTY, game.enemies)
            screen.fill('white')
            game.game_option_menu()
        elif GAME_OVER:
            pygame.mouse.set_visible(True)
            screen.fill('white')
            game.game_over_menu()
        elif GAME_WIN:
            screen.fill('black')
            game.game_win_menu()
        pygame.display.flip()
        CLOCK.tick(60)
