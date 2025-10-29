import pygame
import sys
from fighter import Fighter
from alien import Alien
from ball import Ball
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FILL_COLOR, GAME_CAPTION
from old import screen_fill_color


class Game:
    def __init__(self):
        pygame.display.set_caption(GAME_CAPTION)
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen_fill_color = SCREEN_FILL_COLOR
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_font = pygame.font.Font(None, 30)
        self.game_score = 0

        self.fighter = Fighter()
        self.alien = Alien()
        self.ball = Ball(fighter=self.fighter)

        self.game_is_running = True

    def run(self):
        while self.game_is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.handle_key_event(event)

            self.update_game_state()
            self.draw_screen()

        self.show_game_over()

    def handle_key_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.fighter.move_left()
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.fighter.move_right()
            if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                self.ball.fire()
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.fighter.stop_shifting()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.fighter.stop_moving()
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.fighter.stop_moving()
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.fighter.stop_shifting()


    def update_game_state(self):
        self.fighter.update_position()
        self.alien.update_position()
        self.ball.update_position()

        if self.ball.is_out_of_screen():
            self.ball.reset()

        if self.ball.is_collision(self.alien):
            self.ball.reset()
            self.alien.reset()
            self.game_score += 1

        if self.alien.has_reached_fighter(self.fighter):
            self.game_is_running = False

    def draw_screen(self):
        self.screen.fill(self.screen_fill_color)
        self.screen.blit(self.fighter.image, (self.fighter.x, self.fighter.y))
        self.screen.blit(self.alien.image, (self.alien.x, self.alien.image))
        if self.ball.was_fired:
            self.screen.blit(self.ball.image, (self.ball.x, self.ball.y))
        self.show_game_score()
        pygame.display.update()

    def show_game_score(self):
        game_score_text = f"Kill Count: {self.game_score}"
        self.screen.blit(self.game_font.render(game_score_text, True, 'White'), (5, 5))

    def show_game_over(self):
        game_over_text = self.game_font.render("Game Over!", True, 'White')
        game_over_rectangle = game_over_text.get_rect()
        game_over_rectangle.center = (self.screen_width / 2, self.screen_height / 2)

        self.screen.blit(game_over_text, game_over_rectangle)

        pygame.display.update()

        pygame.time.wait(5000)

