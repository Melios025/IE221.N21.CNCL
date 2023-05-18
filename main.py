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

        self.player_sprite = Player()
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

        # enemy
        self.enemies = pygame.sprite.Group()

        # Boss
        self.boss_sprite = Boss()
        self.boss = pygame.sprite.GroupSingle(self.boss_sprite)

        # Text
        self.text = pygame.sprite.Group()

        # Get mouse position

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
            40, f'Health: {self.boss_sprite.health}', 'White', (60, 50), health_display))

    def game_win_condition(self):
        global GAME_ACTIVE
        if self.boss_sprite.health <= 0:
            GAME_ACTIVE = False

    def game_active(self):
        self.background_surface = pygame.image.load(
            'graphics/bg.jpg').convert_alpha()
        self.background_rect = self.background_surface.get_rect(
            center=(640, 360))
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
        self.background_surface = pygame.image.load(
            'graphics/bg.jpg').convert_alpha()
        self.background_rect = self.background_surface.get_rect(
            center=(640, 360))
        screen.blit(self.background_surface, self.background_rect)

        self.mouse_pos = pygame.mouse.get_pos()
        if GAME_START:
            menu_text_display = True
        else:
            menu_text_display = False
        self.text.add(Text(100, 'My Final Project', 'Black',
                      (640, 100), menu_text_display))
        self.text.draw(screen)
        self.text.update()

        # Play button
        self.play_button = Button(None, (640, 300), 'PLAY', pygame.font.Font(
            'font/Pixeltype.ttf', 80), 'Black', 'lightblue')
        self.play_button.changeColor(self.mouse_pos)
        self.play_button.update(screen)

        # Setting button
        self.setting_button = Button(None, (640, 370), 'SETTING', pygame.font.Font(
            'font/Pixeltype.ttf', 80), 'Black', 'red')
        self.setting_button.changeColor(self.mouse_pos)
        self.setting_button.update(screen)

        # Quit button
        self.quit_button = Button(None, (640, 440), 'QUIT', pygame.font.Font(
            'font/Pixeltype.ttf', 80), 'Black', 'red')
        self.quit_button.changeColor(self.mouse_pos)
        self.quit_button.update(screen)
        if not GAME_START:
            return

    def game_over_menu(self):
        self.mouse_pos = pygame.mouse.get_pos()
        if GAME_OVER:
            text_display = True
        else:
            text_display = False
        self.text.add(
            Text(60, f'Your score: {SCORE}', 'black', (640, 100), text_display))
        self.text.draw(screen)
        self.text.update()

        # Restart button
        self.restart_button = Button(None, (640, 300), 'RESTART', pygame.font.Font(
            'font/Pixeltype.ttf', 80), 'Black', 'red')
        self.restart_button.changeColor(self.mouse_pos)
        self.restart_button.update(screen)

        # Main menu button
        self.main_menu_button = Button(None, (640, 370), 'MAIN MENU', pygame.font.Font(
            'font/Pixeltype.ttf', 80), 'Black', 'red')
        self.main_menu_button.changeColor(self.mouse_pos)
        self.main_menu_button.update(screen)

        # Quit button
        self.quit_button.changeColor(self.mouse_pos)
        self.quit_button.update(screen)

        if not GAME_OVER:
            return

    def game_restart(self, back_main):
        global SCORE
        SCORE = 0
        self.enemies.empty()
        self.boss_sprite.bullets.empty()
        self.boss_sprite.rect.x = 640
        self.boss_sprite.rect.y = -100

        self.player_sprite.bullets.empty()
        if not back_main:
            pygame.mouse.set_pos(640, 650)


if __name__ == '__main__':
    pygame.init()
    timer = pygame.USEREVENT + 1
    pygame.time.set_timer(timer, 1000)
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if GAME_START:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.play_button.checkForInput(game.mouse_pos):
                        pygame.mouse.set_pos(640, 600)
                        GAME_START = False
                        GAME_ACTIVE = True
                    if game.quit_button.checkForInput(game.mouse_pos):
                        pygame.quit()
                        sys.exit()
            if GAME_ACTIVE:
                if event.type == timer:
                    if SCORE < BOSS_SPAWN_SCORE:
                        game.enemies.add(Enemies(choice(['blue', 'yellow'])))
            if GAME_OVER:
                if event.type == pygame.MOUSEBUTTONDOWN:
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
        print(CLOCK.get_fps())
        if GAME_START:
            screen.fill('white')
            game.game_main_menu()
        elif GAME_ACTIVE:
            game.game_active()
        elif GAME_OVER:
            pygame.mouse.set_visible(True)
            screen.fill('white')
            game.game_over_menu()
        else:
            screen.fill('white')
        pygame.display.flip()
        CLOCK.tick(60)
