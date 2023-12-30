'''
Portfolio Project
Snake Game - Main Game 
By Quang Vo
Last Update: 04/01/2023
'''

import pygame
import random

pygame.init()

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Game")

snake_color = (0, 255, 0)
food_color = (255, 0, 0)
bg_color = (0, 0, 0)

class Snake:
    """
    Represents the snake
    """
    def __init__(self):
        """
        Initialize the snake with size 1 and starting position
        """
        self.size = 1
        self.elements = [(100, 100)]
        self.x = 10
        self.y = 0

    def move(self):
        """
        Move the snake based on its current direction
        """
        for i in range(len(self.elements)-1, 0, -1):
            self.elements[i] = self.elements[i-1]
        self.elements[0] = (self.elements[0][0] + self.x, self.elements[0][1] + self.y)

    def grow(self):
        """
        Increase the size of the snake by one and add a new element
        """
        self.size += 1
        self.elements.append((0, 0))

class Food:
    """
    Represents the food
    """
    def __init__(self):
        """
        Initialize the food with a random position and color
        """
        self.position = (0, 0)
        self.color = food_color
        self.randomize_position()

    def randomize_position(self):
        """
        Randomize the position of the food within the game window
        """
        self.position = (random.randint(0, width-10), random.randint(0, height-10))

def collision(rect1, rect2):
    """
    Check for collision between two rectangles
    """
    return (rect1[0] < rect2[0] + rect2[2] and
            rect1[0] + rect1[2] > rect2[0] and
            rect1[1] < rect2[1] + rect2[3] and
            rect1[1] + rect1[3] > rect2[1])

snake = Snake()
food = Food()

HIGH_SCORE_FILE = "high_score.txt"
try:
    with open(HIGH_SCORE_FILE, "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

def menu():
    """
    Displays the main menu
    """
    screen.fill(bg_color)
    font = pygame.font.SysFont(None, 30)
    new_game_text = font.render("Press 1 to start a new game", True, (255, 255, 255))
    high_score_text = font.render("Press 2 to view high score", True, (255, 255, 255))
    quit_text = font.render("Press 3 to quit", True, (255, 255, 255))
    screen.blit(new_game_text, (50, 50))
    screen.blit(high_score_text, (50, 125))
    screen.blit(quit_text, (50, 200))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                reset_game()
                return
            elif event.key == pygame.K_2:
                view_high_score()
            elif event.key == pygame.K_3:
                pygame.quit()
                quit()

def update_high_score(score):
    """
    Updates the high score
    """
    global high_score
    if score > high_score:
        high_score = score
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(high_score))

def view_high_score():
    """
    Shows the highest score
    """
    screen.fill(bg_color)
    font = pygame.font.SysFont(None, 30)
    high_score_text = font.render(f"High score: {high_score}", True, (255, 255, 255))
    back_text = font.render("Press any key to return to menu", True, (255, 255, 255))
    screen.blit(high_score_text, (50, 50))
    screen.blit(back_text, (50, 100))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return

def reset_game():
    """
    Resets the game state
    """
    global snake, food, menu_open
    snake = Snake()
    food = Food()
    menu_open = False

def game_over(score):
    """
    Displays the game over screen
    """
    global menu_open
    while True:
        screen.fill(bg_color)
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Your score: {score}", True, (255, 255, 255))
        high_score_text = font.render(f"High score: {high_score}", True, (255, 255, 255))
        menu_text = font.render("Press any key to return to menu", True, (255, 255, 255))
        screen.blit(score_text, (50, 50))
        screen.blit(high_score_text, (280, 50))
        screen.blit(menu_text, (50, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                reset_game()
                menu_open = True
                return

reset_game()
menu_open = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if menu_open:
                if event.key == pygame.K_1:
                    reset_game()
                    menu_open = False
                elif event.key == pygame.K_2:
                    view_high_score()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    quit()
            else:
                if event.key == pygame.K_ESCAPE:
                    menu_open = True
                if snake.x != 0 or snake.y != 0:
                    if event.key == pygame.K_LEFT:
                        snake.x = -10
                        snake.y = 0
                    elif event.key == pygame.K_RIGHT:
                        snake.x = 10
                        snake.y = 0
                    elif event.key == pygame.K_UP:
                        snake.y = -10
                        snake.x = 0
                    elif event.key == pygame.K_DOWN:
                        snake.y = 10
                        snake.x = 0
    if menu_open:
        menu()
    else:
        snake.move()

        if collision(snake.elements[0] + (10, 10), food.position + (10, 10)):
            snake.grow()
            food.randomize_position()

        if (snake.elements[0][0] < 0 or snake.elements[0][0] > width-10 or
            snake.elements[0][1] < 0 or snake.elements[0][1] > height-10 or
            any(snake.elements.count(e) > 1 for e in snake.elements[1:])):
            update_high_score(snake.size-1)
            game_over(snake.size-1)
            snake.x = 0
            snake.y = 0
            menu_open = True 

        screen.fill(bg_color)
        for element in snake.elements:
            pygame.draw.rect(screen, snake_color, pygame.Rect(element[0], element[1], 10, 10))
        pygame.draw.rect(screen, food.color, pygame.Rect(food.position[0], food.position[1], 10, 10))

        pygame.display.update()

    clock.tick(10)
