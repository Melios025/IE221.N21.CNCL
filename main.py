import pygame
import sys
import json
from enemies import Enemies
from enemies import Meteor
from player import Player
from enemies import Boss
from random import choice
from text import Text
from button import Button
from settings import *


class Game():
    """Game class to init the game
    
    Methods:
        change_difficulty(difficulty): Change difficulty of the game to match the setting.
        
        check_collide(): Check collision from sprites to others.
        
        check_collide_boss(): Check collision from boss's sprites to player's sprites.
        
        display_score(): Display the score on screen of gameplay
        
        display_health(): Display the health of boss on screen of gameplay
        
        game_win_condition(): Check if the game match the win condition and change game state
        
        save_game(): Save the player's score to save file.
        
        game_restart(back_main): Do things when press restart or back_to_main button.
        
        game_active(): Main gameplay state
        
        game_main_menu(): Main menu state        
        
        game_over_menu(): Game over menu state
        
        game_win_menu(): Game win menu state
        
        game_option_menu(): Game option menu state
        
        score_board(): Game score board state
    """
    
    def __init__(self):
        """Initialize all sprites that should be used by the game
        
        Load background, sounds, etc
        Create buttons
        Set time from beginning of the game to 0
        """

        # Player
        self.player_sprite = Player()
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

        # Enemy
        self.enemies = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()

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
        
        # Background for game win and game settings
        self.background_surface_win_setting = pygame.image.load('graphics/bg_win_setting.png').convert_alpha()
        self.background_rect_win_setting = self.background_surface_win_setting.get_rect(center=(640,360))

        # Background for game score board
        self.background_surface_scoreboard = pygame.image.load('graphics/bg_scoreboard.jpg').convert_alpha()
        self.background_surface_scoreboard = pygame.transform.rotozoom(self.background_surface_scoreboard, 0, 1.3)
        self.background_rect_scoreboard = self.background_surface_scoreboard.get_rect(center=(640,360))
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

    def change_difficulty(self, difficulty):
        """Change difficulty of the game to match the setting.
        
        Set global variable (ENEMY_SPAWN, ENEMY_COOLDOWN, etc) to match the difficulty. 
        Set boss atribute of cooldown and health to match the global variables.

        Args:
            difficulty (string): has 3 values( easy, medium, hard ) 
        """
        global ENEMY_SPAWN, ENEMY_COOLDOWN, BOSS_COOLDOWN, BOSS_HEALTH, BOSS_SPAWN_SCORE
        if difficulty == 'easy':
            ENEMY_SPAWN = 1000
            ENEMY_COOLDOWN = 700
            BOSS_COOLDOWN = 300
            BOSS_HEALTH = 5
            BOSS_SPAWN_SCORE = 10
        if difficulty == 'medium':
            ENEMY_SPAWN = 750
            ENEMY_COOLDOWN = 500
            BOSS_COOLDOWN = 250
            BOSS_HEALTH = 10
            BOSS_SPAWN_SCORE = 15
        if difficulty == 'hard':
            ENEMY_SPAWN = 500
            ENEMY_COOLDOWN = 300
            BOSS_COOLDOWN = 200
            BOSS_HEALTH = 20
            BOSS_SPAWN_SCORE = 20
        self.boss_sprite.set_boss_cooldown_health(BOSS_COOLDOWN, BOSS_HEALTH)

    def check_collide(self):
        """Check collision from sprites to others
        
        Check collision and change game state variables if necessary
        Check collision and add score if necessary
        Kill sprite if necessary
        """
        global GAME_OVER, GAME_ACTIVE, SCORE
        # Collide from bullet to enemy
        if self.player_sprite.bullets:
            for bullet in self.player_sprite.bullets:
                if pygame.sprite.spritecollide(bullet, self.enemies, True):
                    bullet.kill()
                    SCORE += 1
                if pygame.sprite.spritecollide(bullet, self.meteors, True):
                    bullet.kill()
                    SCORE += 1

        # Collide from player to enemy
        if pygame.sprite.spritecollide(self.player_sprite, self.enemies, False):
            GAME_ACTIVE = False
            GAME_OVER = True
        if pygame.sprite.spritecollide(self.player_sprite, self.meteors, False):
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
        """Check collision from boss's sprites to player's sprites
        
        Check collosion and change game state if necessary
        Kill sprite if necessary
        """
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
        """Display the score on screen of gameplay."""
        if GAME_ACTIVE:
            score_display = True
        else:
            score_display = False
        self.text.add(
            Text(40, f'Player: {PLAYER_NAME}', 'White', (88, 20), score_display))
        self.text.add(
            Text(40, f'Score: {SCORE}', 'White', (60, 50), score_display))

    def display_health(self):
        """Display the health of boss on screen of gameplay."""
        if GAME_ACTIVE:
            health_display = True
        else:
            health_display = False
        self.text.add(Text(
            40, f'Health: {self.boss_sprite.health}', 'White', (60, 75), health_display))

    def game_win_condition(self):
        """Check if the game match the win condition and change game state."""
        global GAME_ACTIVE, GAME_WIN, SCORE
        if self.boss_sprite.health <= 0:
            SCORE += 10
            GAME_ACTIVE = False
            GAME_WIN = True

    def save_game(self):
        """Save the player's score to save file."""
        with open('save.txt') as save_file:
            json_decoded = json.load(save_file)
        json_decoded[PLAYER_NAME] = SCORE
        with open('save.txt', 'w') as save_file:
            json.dump(json_decoded, save_file)

    def game_main_menu(self):
        """Main menu state
        
        Draw background, button, text, etc.
        """
        # Draw background
        screen.blit(self.background_surface_start, self.background_rect_start)
        self.mouse_pos = pygame.mouse.get_pos()
        if GAME_START:
            menu_text_display = True
        else:
            menu_text_display = False

        self.text.add(Text(100, 'My Final Project', 'White',
                      (640, 130), menu_text_display))
        self.text.add(Text(60, f'Player name: {PLAYER_NAME}', 'White',
                      (640, 200), menu_text_display))
        self.text.draw(screen)
        self.text.update()

        # Play button
        self.play_button = Button(None, (640, 330), 'PLAY', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'White', 'red')
        self.play_button.changeColor(self.mouse_pos)
        self.play_button.update(screen)

        # Score board button
        self.score_board_button = Button(None, (640, 380), 'SCORE BOARD', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'White', 'red')
        self.score_board_button.changeColor(self.mouse_pos)
        self.score_board_button.update(screen)

        # Setting button
        self.setting_button = Button(None, (640, 430), 'SETTING', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'White', 'red')
        self.setting_button.changeColor(self.mouse_pos)
        self.setting_button.update(screen)

        # Quit button
        self.quit_button = Button(None, (640, 480), 'QUIT', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'White', 'red')
        self.quit_button.changeColor(self.mouse_pos)
        self.quit_button.update(screen)
        if not GAME_START:
            return

    def score_board(self):
        """Game score board state
        
        Load score board saved from the file
        Draw background, text, button for game scoreboard menu
        """
        screen.blit(self.background_surface_scoreboard,self.background_rect_scoreboard)
        self.mouse_pos = pygame.mouse.get_pos()
        if SCORE_BOARD:
            text_display = True
        else:
            text_display = False
        with open('save.txt') as save_file:
            data = json.load(save_file)
        data_sort = dict(
            sorted(data.items(), key=lambda x: x[1], reverse=True))
        self.text.add(Text(100, 'SCORE BOARD', 'white',
                      (640, 130), text_display))
        score_board_y = 200
        for key, value in data_sort.items():
            self.text.add(Text(50, f'{key}: {value}', 'white',
                               (640, score_board_y), text_display))
            score_board_y += 40
        self.close_button = Button(None, (1230, 50), 'X', pygame.font.Font(
            'font/Pixeltype.ttf', 100), 'white', 'red')

        self.close_button.update(screen)
        self.text.draw(screen)
        self.text.update()  

    def game_option_menu(self):
        """Game option menu state
        
        Draw background, text, button for game option menu
        Change difficulty
        Turn on sound or music
        """
        screen.blit(self.background_surface_win_setting, self.background_rect_win_setting)
        self.mouse_pos = pygame.mouse.get_pos()
        if GAME_OPTION:
            text_display = True
        else:
            text_display = False
        # Difficulty option
        self.text.add(
            Text(50, 'Game difficulty: ', 'white', (500, 250), text_display))
        if DIFFICULTY == 'easy':
            self.setting_easy = Button(None, (500, 300), 'Easy', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'red', 'red')
        else:
            self.setting_easy = Button(None, (500, 300), 'Easy', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'white', 'red')

        if DIFFICULTY == 'medium':
            self.setting_medium = Button(None, (640, 300), 'Medium', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'red', 'red')
        else:
            self.setting_medium = Button(None, (640, 300), 'Medium', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'white', 'red')

        if DIFFICULTY == 'hard':
            self.setting_hard = Button(None, (780, 300), 'Hard', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'red', 'red')
        else:
            self.setting_hard = Button(None, (780, 300), 'Hard', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'white', 'red')

        # Sound and music

        self.text.add(
            Text(50, 'Sound and music: ', 'white', (500, 350), text_display))
        if SOUND == True:
            self.setting_sound = Button(None, (500, 400), 'Sound', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'red', 'red')
        else:
            self.setting_sound = Button(None, (500, 400), 'Sound', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'white', 'red')
        if MUSIC == True:
            self.setting_music = Button(None, (640, 400), 'Music', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'red', 'red')
        else:
            self.setting_music = Button(None, (640, 400), 'Music', pygame.font.Font(
                'font/Pixeltype.ttf', 60), 'white', 'red')

        self.close_button = Button(None, (1230, 50), 'X', pygame.font.Font(
            'font/Pixeltype.ttf', 100), 'white', 'red')

        self.close_button.update(screen)
        self.setting_easy.update(screen)
        self.setting_medium.update(screen)
        self.setting_hard.update(screen)
        self.setting_sound.update(screen)
        self.setting_music.update(screen)
        self.text.draw(screen)
        self.text.update()
    
    def game_active(self):
        """Main gameplay state
        
        Draw background, player, enemy or boss and everything else
        Check if game win or over(through check_collide function)
        """
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

        self.meteors.draw(screen)
        self.meteors.update()

        # Draw boss
        if SCORE >= BOSS_SPAWN_SCORE:
            self.boss.draw(screen)
            # self.enemies.empty()
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
    
    def game_over_menu(self):
        """Game over menu state
        
        Draw background,button, text for game over menu
        """
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

    def game_restart(self, back_main):
        """Do things when press restart or back_to_main button.
        
        Set every thing to default according to game's difficulty.
        If not back to main: set player's mouse (the spaceship) to bottom of screen.

        Args:
            back_main (bool): Check if player press restart(0) or back_to_main(1).
        """
        global SCORE
        SCORE = 0
        self.change_difficulty(DIFFICULTY)
        game.time = pygame.time.get_ticks()
        self.meteors.empty()
        self.enemies.empty()
        self.boss_sprite.bullets.empty()
        self.boss_sprite.rect.x = 640
        self.boss_sprite.rect.y = -100

        self.player_sprite.bullets.empty()
        if not back_main:
            pygame.mouse.set_pos(640, 650)
            
    def game_win_menu(self):
        """Game win menu state
        
        Draw background, text, button for game win menu
        """
        screen.blit(self.background_surface_win_setting, self.background_rect_win_setting)
        self.mouse_pos = pygame.mouse.get_pos()
        if GAME_WIN:
            text_display = True
        else:
            text_display = False

        self.text.add(
            Text(100, 'GAME WIN !!!', 'white', (640, 250), text_display))
        self.text.add(
            Text(80, f'Your score: {SCORE}', 'white', (640, 310), text_display))
        self.text.draw(screen)
        self.text.update()
        self.main_menu_button = Button(None, (640, 410), 'MAIN MENU', pygame.font.Font(
            'font/Pixeltype.ttf', 60), 'white', 'red')
        self.main_menu_button.changeColor(self.mouse_pos)
        self.main_menu_button.update(screen)
        if not GAME_WIN:
            return


# Main game loop
if __name__ == '__main__': 
    pygame.init()
    timer = pygame.USEREVENT + 1
    game = Game()

    pygame.time.set_timer(timer, ENEMY_SPAWN)
    pygame.mixer.music.load('audio/bg_music.mp3')
    pygame.mixer.music.set_volume(0.2)
    if MUSIC == True:
        pygame.mixer.music.play(1, 30)
        
    game_menu_sound = pygame.mixer.Sound('audio/game_ui.mp3')
    game_over_sound = pygame.mixer.Sound('audio/game_over.mp3')
    game_win_sound = pygame.mixer.Sound('audio/game_win.mp3')
    game_start_sound = pygame.mixer.Sound('audio/game_start.mp3')
    while True:
        """Main game loop."""
        if SOUND == False:
            if game_menu_sound != None:
                pygame.mixer.Sound.set_volume(game_menu_sound, 0)
            if game_over_sound != None:
                pygame.mixer.Sound.set_volume(game_over_sound, 0)
            if game_win_sound != None:
                pygame.mixer.Sound.set_volume(game_win_sound, 0)
            if game_start_sound != None:
                pygame.mixer.Sound.set_volume(game_start_sound, 0)
        else:
            if game_menu_sound != None:
                pygame.mixer.Sound.set_volume(game_menu_sound, 1)
            if game_over_sound != None:
                pygame.mixer.Sound.set_volume(game_over_sound, 1)
            if game_win_sound != None:
                pygame.mixer.Sound.set_volume(game_win_sound, 1)
            if game_start_sound != None:
                pygame.mixer.Sound.set_volume(game_start_sound, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_game()
                pygame.quit()
                sys.exit()
            if GAME_START:
                if event.type == pygame.MOUSEBUTTONUP:
                    if game.play_button.checkForInput(game.mouse_pos):
                        pygame.mouse.set_pos(640, 600)
                        game_start_sound.play()
                        game_over_sound = pygame.mixer.Sound(
                            'audio/game_over.mp3')
                        game_win_sound = pygame.mixer.Sound(
                            'audio/game_win.mp3')
                        GAME_START = False
                        GAME_ACTIVE = True
                    if game.score_board_button.checkForInput(game.mouse_pos):
                        game_start_sound.play()
                        game_over_sound = pygame.mixer.Sound(
                            'audio/game_over.mp3')
                        game_win_sound = pygame.mixer.Sound(
                            'audio/game_win.mp3')
                        GAME_START = False
                        SCORE_BOARD = True
                    if game.setting_button.checkForInput(game.mouse_pos):
                        game_menu_sound.play()
                        GAME_START = False
                        GAME_OPTION = True
                    if game.quit_button.checkForInput(game.mouse_pos):
                        game.save_game()
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        PLAYER_NAME = PLAYER_NAME[:-1]
                    else:
                        PLAYER_NAME += event.unicode
            if SCORE_BOARD:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.close_button.checkForInput(game.mouse_pos):
                        game_menu_sound.play()
                        SCORE_BOARD = False
                        GAME_START = True
            if GAME_OPTION:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.close_button.checkForInput(game.mouse_pos):
                        game_menu_sound.play()
                        GAME_OPTION = False
                        GAME_START = True
                    if game.setting_easy.checkForInput(game.mouse_pos) and DIFFICULTY != 'easy':
                        DIFFICULTY = 'easy'
                        game_menu_sound.play()
                        game.change_difficulty('easy')
                        pygame.time.set_timer(timer, ENEMY_SPAWN)

                    if game.setting_medium.checkForInput(game.mouse_pos) and DIFFICULTY != 'medium':
                        DIFFICULTY = 'medium'
                        game_menu_sound.play()
                        game.change_difficulty('medium')
                        pygame.time.set_timer(timer, ENEMY_SPAWN)

                    if game.setting_hard.checkForInput(game.mouse_pos) and DIFFICULTY != 'hard':
                        DIFFICULTY = 'hard'
                        game_menu_sound.play()
                        game.change_difficulty('hard')
                        pygame.time.set_timer(timer, ENEMY_SPAWN)

                    if game.setting_sound.checkForInput(game.mouse_pos) and SOUND != True:
                        game_menu_sound.play()
                        SOUND = True
                        pygame.mixer.Sound.set_volume(
                            game.player_sprite.shoot_sound, 1)
                    elif game.setting_sound.checkForInput(game.mouse_pos) and SOUND != False:
                        SOUND = False
                        pygame.mixer.Sound.set_volume(
                            game.player_sprite.shoot_sound, 0)

                    if game.setting_music.checkForInput(game.mouse_pos) and MUSIC != True:
                        game_menu_sound.play()
                        MUSIC = True
                        pygame.mixer.music.play()
                    elif game.setting_music.checkForInput(game.mouse_pos) and MUSIC != False:
                        game_menu_sound.play()
                        MUSIC = False
                        pygame.mixer.music.stop()
            if GAME_ACTIVE:
                if event.type == timer:
                    if SCORE < BOSS_SPAWN_SCORE:
                        game.enemies.add(
                            Enemies(choice(['blue', 'yellow', 'blue'])))
                    else:
                        game.meteors.add(
                            Meteor(choice([1, 2, 3, 4])))
            if GAME_OVER:
                if event.type == pygame.MOUSEBUTTONUP:
                    if game.restart_button.checkForInput(game.mouse_pos):
                        game_start_sound.play()
                        if MUSIC == True:
                            pygame.mixer.music.play(0)
                        game_over_sound = pygame.mixer.Sound(
                            'audio/game_over.mp3')
                        game_win_sound = pygame.mixer.Sound(
                            'audio/game_win.mp3')
                        game.save_game()
                        game.game_restart(False)
                        GAME_OVER = False
                        GAME_ACTIVE = True
                    if game.main_menu_button.checkForInput(game.mouse_pos):
                        if MUSIC == True:
                            pygame.mixer.music.play(0)
                        game_menu_sound.play()
                        game.save_game()
                        game.game_restart(True)
                        GAME_OVER = False
                        GAME_START = True
                    if game.quit_button.checkForInput(game.mouse_pos):
                        game.save_game()
                        pygame.quit()
                        sys.exit()
            if GAME_WIN:
                if event.type == pygame.MOUSEBUTTONUP:
                    if game.main_menu_button.checkForInput(game.mouse_pos):
                        if MUSIC == True:
                            pygame.mixer.music.play(0)
                        game_over_sound = pygame.mixer.Sound(
                            'audio/game_over.mp3')
                        game_win_sound = pygame.mixer.Sound(
                            'audio/game_win.mp3')
                        game_menu_sound.play()
                        game.save_game()
                        game.game_restart(True)
                        GAME_WIN = False
                        GAME_START = True
        # Game layout for each game state
        if GAME_START:
            screen.fill('white')
            game.game_main_menu()
        elif GAME_ACTIVE:
            for enemy in game.enemies:
                enemy.set_cooldown(ENEMY_COOLDOWN)
            if game.time == 0:
                game.time = pygame.time.get_ticks()
            game.game_active()
        elif SCORE_BOARD:
            screen.fill('white')
            game.score_board()
        elif GAME_OPTION:
            game.game_option_menu()
        elif GAME_OVER:
            pygame.mixer.music.stop()
            if game_over_sound != None:
                game_over_sound.play()
                game_over_sound = None
            pygame.mouse.set_visible(True)
            screen.fill('white')
            game.game_over_menu()
        elif GAME_WIN:
            game.game_win_menu()
            pygame.mixer.music.stop()
            if game_win_sound != None:
                game_win_sound.play()
                game_win_sound = None
            pygame.mouse.set_visible(True)
        pygame.display.flip()
        CLOCK.tick(60)