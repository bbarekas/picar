import pygame
from buildhat import Motor
from buildhat import MotorPair
from buildhat import Hat
import time 

#motor_left = Motor('A')
#motor_right = Motor('B')
pair = MotorPair('A', 'B')
pair.set_default_speed(10)
direction = 2

def stop():
  pair.stop()

def forward():
  global direction
  hat.green_led(True)
  hat.orange_led(False)
  if direction != 0:
    #pair.run_for_degrees(20,-10,10)
    pair.run_for_degrees(90,-25,25)
    #pair.run_for_degrees(10,-10,10)
  else:  
    pair.run_for_degrees(90,-25,25)
  direction = 0 



def back():
  global direction
  hat.green_led(False)
  hat.orange_led(True)
  if direction != 1:
    #pair.run_for_degrees(20,10,-10)
    pair.run_for_degrees(90,25,-25)
    #pair.run_for_degrees(10,10,-10)
  else:  
    pair.run_for_degrees(90,25,-25)
  direction = 1


def left():
  global direction
  pair.run_for_degrees(90,25,25)
  direction = 2


def right():
  global direction
  pair.run_for_degrees(90,-25,-25)
  direction = 2

hat = Hat()
print(hat.get())

direction = 2
pygame.init()
screen = pygame.display.set_mode((500, 450))
x1, y1 = 300, 350
while True:
    screen.fill((0, 0, 0))
    circle1 = pygame.draw.circle(screen, (249, 246, 238), (x1, y1), 35)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            exit()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_LEFT:
                x1 -= 10
                print("Left arrow key is pressed")
                left()
            if i.key == pygame.K_RIGHT:
                x1 += 10
                print("Right arrow key is pressed")
                right()
            if i.key == pygame.K_UP:
                y1 -= 10
                print("Up arrow key is pressed")
                forward()
            if i.key == pygame.K_DOWN:
                y1 += 10
                print("Down arrow key is pressed")
                back()

            #time.sleep(0.5)
            #stop()
            
    pygame.display.update()
