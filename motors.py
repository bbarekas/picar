from buildhat import Motor
from time import sleep
from pynput import keyboard
import time 

motor_left = Motor('A')
motor_right = Motor('B')

def stop():
  motor_left.stop()
  motor_right.stop()


def forward():
  motor_left.start(50)
  motor_right.start(-50)


def back():
  motor_left.start(-50)
  motor_right.start(50)

def left():
  motor_left.start(50)
  motor_right.start(50)


def right():
  motor_left.start(-50)
  motor_right.start(-50)




#while True:
#    try:
#        if keyboard.is_pressed('left'):
#            print('You Pressed left!')
#        elif keyboard.is_pressed('right'):
#            print('You Pressed right!')
#        elif keyboard.is_pressed('down'):
#            print('You Pressed down!')
#        elif keyboard.is_pressed('up'):
#            print('You Pressed up!')
#            
#        time.sleep(0.5)
#
#    except:
#        break


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
#with keyboard.Listener(
#        on_press=on_press,
#        on_release=on_release) as listener:
#    listener.join()

# ...or, in a non-blocking fashion:
#listener = keyboard.Listener(
#    on_press=on_press,
#    on_release=on_release)
#listener.start()


# The event listener will be running in this block
with keyboard.Events() as events:
    for event in events:
        if event.key == keyboard.Key.esc:
            break
        else:
            print('Received event {}'.format(event))
            

# Press PAGE UP then PAGE DOWN to type "foobar".
#keyboard.add_hotkey('page up, page down', lambda: keyboard.write('foobar'))

# Blocks until you press esc.
# keyboard.wait('esc')
print("Wait ..")
time.sleep(5)

