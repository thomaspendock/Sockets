from grafix import *
from macColors import *
from random import randint, choice
import threading
import time
import sys

# Circular import, cant run as main but can be an imported module
from test_socket import API 

msg_color = 255 # Default: white
print_lock = threading.Lock()

def set_user_color():
    global msg_color
    msg_color = randint(17, 231)
    

def welcome():
    '''Prints welcome and info'''
    welcome_msg = 'W E L C O M E'
    b1, rw = border(welcome_msg, 4, 1, index=237)
    b2, rw = border(b1, 0, 0, rw, index=243)
    b3, rw = border(b2, 0, 0, rw, index=247)
    print(b3)
    
def commands():
    command_color = 117
    comment_color = 115
    max_title_len = 54
    commands = ''
    
    commands_col = 'Commands:'
    spacing = ' ' * (max_title_len-len(commands_col))
    comments_col = 'Usage:'
    commands += fg(commands_col, index=command_color)
    commands += spacing
    commands += fg(comments_col, index=comment_color)
    commands += '\n'

    commands_underline = '-' * (max_title_len - 8)
    spacing = ' ' * (max_title_len-len(commands_underline))
    comments_underline = '-' * 30

    commands += fg(commands_underline + spacing + comments_underline, index=243) + '\n'
    
    max_code_len  = 5
    for cmd in  API:
        cmd_name = cmd.__name__
        title, usage = cmd.__doc__.split('\n')
        title = ('%s - ' % cmd_name) + title
        spacing = ' ' * (max_title_len-len(title)) # If neg this breaks
        commands += fg(title, index=command_color) + spacing + fg(usage, index=comment_color)
        commands += '\n'
    commands += '\n'
    print(commands)

def user_info(user_name, user_address):
    your_name    = bg('Your name: ' + user_name, index=67)
    your_address = bg('Your receiving address: ' + user_address, rgb=(0,3,3)) + '\n'
    print(your_name)
    print(your_address)

def goodbye():
    print(fg('Goodbye.', index=196))

def error(error_msg):
    print_lock.acquire()
    print(fg(error_msg, index=196))
    print_lock.release()
    
def user_color(msg):
    global msg_color
    
    return fg(msg, index=msg_color)

def message_prompt():
    return '\b\b\b> '

def on_received(sender_name, message):
    print_lock.acquire()

    text = message['text']
    animated = False if 'animation' not in message else message['animation']

    sys.stdout.write(sender_name + ': ')
    
    if animated and 'color' in message:
        animate = choice([animate1, animate2, animate3, animate4])
        animate(text, message['color'])
    else:
        sys.stdout.write(text)
        
    sys.stdout.write('\n> ')
    sys.stdout.flush()
    
    print_lock.release()


def command_output(sender_name, msg, out, fail=True):
    s = ''
    color = 196 if fail else 46
    s += fg(msg, index=color)
    if len(out) > 0:
        s += fg(' Showing ' + sender_name+'\'s output...\n', index=42)
        s += '\n' + out + '\n'
    return s

# put in grafix module??

def light(s, i, color, r=5):
    '''Places a symmetrical light inside the text'''
    l = len(s)
    new_s = ''
    for j in range(len(s)):
        dis = abs(i - j)
        rj = 0 if dis > r else r - dis

        colorj = color + rj

        new_s += fg(s[j], index=colorj)
    
    return new_s, l

def seperate(s, space):
    new_s = ''
    for c in s:
        new_s += ' '*space
        new_s += c
    new_s += ' '*len(s)
    return new_s, len(new_s)

def appear(s, i):
    base = 232
    return fg(s, index=base+i), len(s)

def glitch(s, i):

    new_s = ''
    for j in range(len(s)):
        new_s += s[j] if j < i else chr(randint(ord('a'), ord('z')))

    return new_s, len(s)

def animate1(message, color):
    for i in range(0, len(message) + 1):
        sub_message = message
        s, l = glitch(sub_message, i)
        sys.stdout.write(s)
        sys.stdout.flush()
        time.sleep(0.019)
        sys.stdout.write('\b' * l)
        
    sys.stdout.write(fg(message, index=color))
    sys.stdout.flush()

def animate4(message, color):
    for i in range(0, 24):
        sub_message = message
        s, l = appear(sub_message, i)
        sys.stdout.write(s)
        sys.stdout.flush()
        time.sleep(0.045)
        sys.stdout.write('\b' * l)
        
    sys.stdout.write(fg(message, index=color))
    sys.stdout.flush()

def animate3(message, color):
    for i in range(5, -1, -1):
        sub_message = message
        s, l = seperate(sub_message, i)
        
        sys.stdout.write(s)
        sys.stdout.flush()
        time.sleep(0.15 + 0.019)
        sys.stdout.write('\b' * l)
        
    sys.stdout.write(fg(message, index=color))
    sys.stdout.flush()
    

def animate2(message, color):
    r = 10
    
    for i in range(r + len(message)):
        sub_message = message #message[:i]
        s, l = light(sub_message, i, color, r=r)
        
        sys.stdout.write(s)
        sys.stdout.flush()
        time.sleep(0.019)
        sys.stdout.write('\b' * l)
        
    sys.stdout.write(fg(message, index=color))
    sys.stdout.flush()
    



        
