from inspect import iscode
import pygame
from pygame.locals import *
import time
import random

SIZE = 40


class Apple:
    def __init__(self, parent_screen):
        self.apple = pygame.image.load("snake_game/resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3
         
    def move(self):
        self.x = random.randint(0, 19) * SIZE
        self.y = random.randint(0, 19) * SIZE

    def draw(self):
        self.parent_screen.blit(self.apple,(self.x,self.y))
        pygame.display.flip()

class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_Screen = surface
        self.block = pygame.image.load("snake_game/resources/block.jpg").convert()
        # creates an array of [] length long
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'
        
    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
        
    def draw(self):
        self.parent_Screen.fill((110, 110, 10))
        #drawing the block on the surface
        for length in range(self.length):
            self.parent_Screen.blit(self.block,(self.x[length],self.y[length]))
        pygame.display.flip()
        
    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'
    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction =  'down'

    def walk(self):
        
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
            
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and Apple Game")
        
        pygame.mixer.init()
        # self.play_background_music()
        #background screen- making class member with self so that it is available to other methods
        self.surface = pygame.display.set_mode((800, 800))
        self.surface.fill((110, 110, 10))
        self.snake = Snake(self.surface, 3)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        
    def isCollision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                # means there is a collision
                return True
        return False 
        
    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        
        #snake colliding with apple
        if self.isCollision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            # sound = pygame.mixer.Sound("snake_game/resources/ding.mp3")
            # pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()
     
        #snake colliding with self
        for i in range(3, self.snake.length):
            if self.isCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                # sound = pygame.mixer.Sound("snake_game/resources/crash.mp3")
                # pygame.mixer.Sound.play(sound)
                raise "Collision Occured"
    
    def display_score(self):
        font = pygame.font.SysFont('comicsans', 30)  
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (600, 10))
        
    def play_background_music(self):
        pygame.mixer.music.load("snake_game/resources/theme.mp3")
        pygame.mixer.music.play()
        
    def show_game_over(self):
        self.surface.fill((110, 110, 10))
        font = pygame.font.SysFont('comicsans', 20)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (100, 300))
        line2 = font.render("To play the game again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (100, 350))
        pygame.display.flip()
        
    def reset(self):
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)
        
        
    def run(self):
        running = True
        pause = False
        
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    #makes it so escape key exits
                    if event.key == K_ESCAPE:
                        running = False
                
                    if event.key == K_RETURN:
                        pause = False
                
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                # makes it so there is an X out in the top right
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
                
            time.sleep(0.2)
            
if __name__ == "__main__":
    game = Game()
    game.run()