import pygame
import time
pygame.init()

# screen
width=800
height=600
size=(width,height)
screen=pygame.display.set_mode(size)

# snake
snake_image=pygame.image.load("Snake.png")

head=[(width+32)/2 , (height+32)/2]
tail=[(width)/2 , (height+32)/2]

# Initial
snake=[tail,head]    # [Tail, n-1th part, n-2th part,............2nd turn, 1st turn, Head]
                     # For every movement, a new element is added at the and which becomes the head
                     # and current tail is removed and the first element becomes the new tail

# Position of b wrt a   a,b are lists of the form [x,y]
def pos(b,a):
    if(a==b):
        return 's'
    elif(b[0]==a[0]):
        if(b[1]<a[1]):
            return 'u'
        elif(b[1]>a[1]):
            return 'd'
    elif(b[1]==a[1]):
        if(b[0]>a[0]):
            return 'r'
        elif(b[0]<a[0]):
            return 'l'

def move_one_step(snake,x_inc,y_inc):
    if(x_inc!=0 or y_inc!=0):
        time.sleep(1/(speed*100))
        # Head
        snake.append( [ snake[-1][0]+x_inc , snake[-1][1]+y_inc ] )
        # Tail
        snake.pop(0)
    return snake


def add_new(snake):    # Increases the length of the snake
    if(pos(snake[1],snake[0])=='r'):
        snake.insert(0,[snake[0][0]-16,snake[0][1]])
    elif(pos(snake[1],snake[0])=='l'):
        snake.insert(0,[snake[0][0]+16,snake[0][1]])
    elif(pos(snake[1],snake[0])=='u'):
        snake.insert(0,[snake[0][0],snake[0][1]+16])
    elif(pos(snake[1],snake[0])=='d'):
        snake.insert(0,[snake[0][0],snake[0][1]-16])
    return snake

def key_press(snake,event,speed,x_inc,y_inc):
    if event.key==pygame.K_a:
        snake=add_new(snake)

    elif event.key==pygame.K_LEFT:
        x_inc= -16
        y_inc=0

    elif event.key==pygame.K_RIGHT:
        x_inc= 16
        y_inc=0

    elif event.key==pygame.K_UP:
        y_inc= -16
        x_inc=0
        
    elif event.key==pygame.K_DOWN:
        y_inc= 16
        x_inc=0
    return (snake,x_inc,y_inc)

def boundary(snake):
    for point in snake:
        if point[0]>=width:
            point[0]=0
        elif(point[0]<=-16):
            point[0]=width-16
        if point[1]>=height:
            point[1]=0
        elif(point[1]<=-16):
            point[1]=height-16
    return snake



def display_snake(snake):
    for i in snake:
        coordinates=(i[0],i[1])
        screen.blit(snake_image,coordinates)
    


run=True
speed=0.2
x_inc,y_inc=0,0
while run:
    screen.fill((150,0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        elif event.type==pygame.KEYDOWN:
            snake,x_inc,y_inc=key_press(snake,event,speed,x_inc,y_inc)            

    snake=move_one_step(snake,x_inc,y_inc)

    snake=boundary(snake)

    display_snake(snake)

    pygame.display.update()
