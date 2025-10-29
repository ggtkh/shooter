import pygame
import sys
from random import  randint

pygame.init()

game_font = pygame.font.Font(None, 30)

screen_width, screen_height = 800, 700
screen_fill_color = (32, 52, 71)
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Shooter Game, Ninga")

fighter_step = 0.4
fighter_is_shifting = False
fighter_image = pygame.image.load('images/fighter.png')
fighter_width, fighter_height = fighter_image.get_size()
fighter_x, fighter_y = (screen_width - fighter_width)/2, screen_height - fighter_height
fighter_is_moving_right, fighter_is_moving_left = False, False

ROCKET_STEP = 0.5
rocket_image = pygame.image.load('images/rocket.png')
rocket_width, rocket_height = rocket_image.get_size()
rocket_was_fired = False

alien_step = 0.1
alien_image = pygame.image.load('images/alien.png')
alien_width, alien_height = alien_image.get_size()
alien_x, alien_y = randint(0, screen_width - alien_width), 0

kill_count = 0
kill_count_text = f"Kill Count: {kill_count}"

# Tutorial screen
screen.fill(screen_fill_color)
screen.blit(fighter_image, (fighter_x, fighter_y))
screen.blit(alien_image, (alien_x, alien_y))

screen.blit(game_font.render("Moving: A, D or KeyLeft, KeyRight", True, 'White'), (5,5))
screen.blit(game_font.render("Shooting: W, SPACE or KeyUp", True, 'White'), (5, 30))
screen.blit(game_font.render("Speed Shift: LShift or RShift", True, 'White'), (5, 55))

pygame.display.update()

pygame.time.wait(5000)


game_is_running = True
while game_is_running:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                fighter_is_moving_left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                fighter_is_moving_right = True
            if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                rocket_was_fired = True
                rocket_x, rocket_y = fighter_x + fighter_width / 2 - rocket_width / 2, fighter_y - rocket_height
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                fighter_is_shifting = True
                fighter_step += 0.7

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                fighter_is_moving_left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                fighter_is_moving_right = False
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                fighter_is_shifting = False
                fighter_step -= 0.7

    if fighter_is_moving_left and fighter_x >= fighter_step:
        fighter_x -= fighter_step

    if fighter_is_moving_right and fighter_x <= screen_width - fighter_width - fighter_step:
        fighter_x += fighter_step

    alien_y += alien_step


    if rocket_was_fired and rocket_y >= 0:
        rocket_y -= ROCKET_STEP


    else:
        rocket_was_fired = False
        rocket_x, rocket_y = fighter_x + fighter_width / 2 - rocket_width / 2, fighter_y - rocket_height


    screen.fill(screen_fill_color)
    screen.blit(fighter_image, (fighter_x, fighter_y))
    screen.blit(alien_image, (alien_x, alien_y))
    kill_count_text = f"Kill Count: {kill_count}"
    screen.blit(game_font.render(kill_count_text, True, 'White'), (5, 5))

    if rocket_was_fired:
        screen.blit(rocket_image, (rocket_x, rocket_y))


    pygame.display.update()

    if alien_y + alien_height >= fighter_y:
        game_is_running = False

    if rocket_was_fired and\
            alien_x - rocket_width <= rocket_x <= alien_x + alien_width and\
            alien_y < rocket_y < alien_y + alien_height - rocket_height:
            rocket_was_fired = False
            alien_x, alien_y = randint(0, screen_width - alien_width), 0
            alien_step += 0.02
            fighter_step += 0.01
            kill_count += 1


game_over_text = game_font.render("Game Over!", True, 'White')
game_over_rectangle = game_over_text.get_rect()
game_over_rectangle.center = (screen_width/2, screen_height/2)

screen.blit(game_over_text, game_over_rectangle)

pygame.display.update()

pygame.time.wait(5000)

pygame.quit()