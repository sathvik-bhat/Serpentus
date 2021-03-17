import pygame
import time
import random

pygame.init()

# screen
width = 800
height = 448
highscore = 0
size = (width, height)
screen = pygame.display.set_mode(size)

# add food images
apple = pygame.image.load('./images/apple.png')
plum = pygame.image.load('./images/plum.png')
oranges = pygame.image.load('./images/orange.png')
strawberry = pygame.image.load('./images/strawberry.png')

orange = pygame.Color("orange")
black = pygame.Color("black")

# add sounds
eat = pygame.mixer.Sound('./sounds/eat.wav')
music = pygame.mixer.music.load('./sounds/music.mp3')
pygame.mixer.music.play(-1)

from os import path

class Snake():
    # snake body is represented as
    # [Tail, n-1th part, n-2th part,............2nd turn, 1st turn, Head]
    # For every movement, a new element is added at the and which becomes the head
    # and current tail is removed and the first element becomes the new tail

    def __init__(self):
        self.colour = "Snake"
        self.head = [(width + 32) / 2, (height + 32) / 2]
        self.tail = [(width) / 2, (height + 32) / 2]
        self.body = [self.tail, self.head]
        self.speed = 0.2
        self.x_inc = 0
        self.y_inc = 0
        self.prev_dir = None

    @staticmethod
    def pos(b, a):  # Position of b wrt a   a,b are lists of the form [x,y]
        if (a == b):
            return 's'
        elif (b[0] == a[0]):
            if (b[1] < a[1]):
                return 'u'
            elif (b[1] > a[1]):
                return 'd'
        elif (b[1] == a[1]):
            if (b[0] > a[0]):
                return 'r'
            elif (b[0] < a[0]):
                return 'l'

    def movement(self, event):  # Identifies key inputs and changes x_inc and y_inc
        if event.key == pygame.K_LEFT:
            if (self.prev_dir != 'r'):
                self.x_inc = -16
                self.y_inc = 0
                self.prev_dir = 'l'

        elif event.key == pygame.K_RIGHT:
            if (self.prev_dir != 'l'):
                self.x_inc = 16
                self.y_inc = 0
                self.prev_dir = 'r'

        elif event.key == pygame.K_UP:
            if (self.prev_dir != 'd'):
                self.y_inc = -16
                self.x_inc = 0
                self.prev_dir = 'u'

        elif event.key == pygame.K_DOWN:
            if (self.prev_dir != 'u'):
                self.y_inc = 16
                self.x_inc = 0
                self.prev_dir = 'd'

    def move_one_step(self):  # moves the sname by one step depending on x_inc and y_inc
        snake = self.body
        if (self.x_inc != 0 or self.y_inc != 0):
            time.sleep(1 / (self.speed * 100))
            # Head
            snake.append([snake[-1][0] + self.x_inc, snake[-1][1] + self.y_inc])
            # Tail
            snake.pop(0)

    def add_new(self):  # Increases the length of the snake
        snake = self.body
        if (self.pos(snake[1], snake[0]) == 'r'):
            snake.insert(0, [snake[0][0] - 16, snake[0][1]])
        elif (self.pos(snake[1], snake[0]) == 'l'):
            snake.insert(0, [snake[0][0] + 16, snake[0][1]])
        elif (self.pos(snake[1], snake[0]) == 'u'):
            snake.insert(0, [snake[0][0], snake[0][1] + 16])
        elif (self.pos(snake[1], snake[0]) == 'd'):
            snake.insert(0, [snake[0][0], snake[0][1] - 16])
        return snake

    def boundary(self):  # Snake emerges from opposite side if it goes out of the boundary
        snake = self.body
        for point in snake:
            if point[0] >= width:
                point[0] = 0
            elif (point[0] <= -16):
                point[0] = width - 16
            if point[1] >= height:
                point[1] = 0
            elif (point[1] <= -16):
                point[1] = height - 16

    def display(self):  # Displays the snake on the screen
        snake = self.body
        for i in snake:
            coordinates = [i[0], i[1]]
            pygame.draw.rect(screen, black, pygame.Rect(i[0], i[1], 16, 16))
        return coordinates

    def death(self, run):
        count = 0
        for i in range(len(self.body) - 1):
            if (self.body[-1] == self.body[i]):
                count += 1

        if (count != 0):
            over = pygame.font.Font('valianttimes3d.ttf', 80)
            overt = over.render('GAME OVER', True, (0, 0, 255))
            screen.blit(overt, (width / 2, height / 2))

            # opening file which stores highscores
            with open('./highscore.txt', 'w') as f:
                try:
                    highscore = int(f.read())
                except:
                    highscore = 0

            # writing new highscore into file
            if(score.display() >= highscore):
                highscore = score.display()
                with open('./highscore.txt', 'w') as f:
                    f.write(str(highscore))

            h_score = pygame.font.Font('valianttimes3d.ttf', 80)
            h_score1 = h_score.render('HIGH SCORE: ' + str(highscore), True, (0, 0, 255))
            screen.blit(h_score1, (50, 50))
            pygame.display.update()
            time.sleep(3)
            run = False
        return run


class Score():
    # score_total = 0

    def __init__(self):
        self.total = 0

    def update_score(self):
        if(food.respawn() == 1):
            self.total += 1
        elif(food.respawn() == 2):
            self.total += 2
        elif(food.respawn() == 3):
            self.total += 3
        elif(food.respawn() == 4):
            self.total += 10

    def display(self):
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = self.font.render('Score ' + str(self.total), True, (0, 255, 0), (0, 0, 0))
        self.textRect = self.text.get_rect()
        self.textRect.center = (40, 10)
        screen.blit(self.text, self.textRect)
        return(self.total)


class Food():
    def __init__(self):
        self.food_position = None
        self.food_spawn = False

    def respawn(self):
        if self.food_spawn is False:  # When a food is taken it will respawn randomly
            self.weighted_list = random.choices([1, 2, 3, 4], weights = (40, 30, 20, 10), k=1) # implementing different foods with different probabilities of occuring. fruit with lower points has a higher chance of occuring
            self.n = self.weighted_list[0]
            self.food_position = [random.randint(1, width / 16 - 1) * 16, random.randint(1, height / 16 - 1) * 16]
            self.food_spawn = True  # It will set the food to True again, to keep the cycle
        return self.n

    def eat(self, snake, score):
        if snake.body[-1] == self.food_position:
            score.update_score()
            snake.add_new()
            eat.play()
            self.food_spawn = False  # It removes the food from the board

    def display(self):
        if (self.n == 1):
            screen.blit(apple, (self.food_position))
        elif (self.n == 2):
            screen.blit(oranges, (self.food_position))
        elif (self.n == 3):
            screen.blit(plum, (self.food_position))
        elif (self.n == 4):
            screen.blit(strawberry, (self.food_position))


snake = Snake()
score = Score()
food = Food()

run = True
while run:

    screen.fill((150, 0, 0))
    score.display()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            snake.movement(event)

    snake.move_one_step()

    snake.boundary()


    food.eat(snake, score)
    food.respawn()
    food.display()


    score.display()


    snake.display()
    run = snake.death(run)

    pygame.display.update()