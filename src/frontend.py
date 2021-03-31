from grafix import *
from macColors import *
from random import randint
import threading

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

    commands_underline = '-' * 40
    spacing = ' ' * (max_title_len-len(commands_underline))
    comments_underline = '-' * 20

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
    s = sender_name+': ' + message + '\n'
    s += '> '
    
    print(s, end='')
    print_lock.release()


def command_output(sender_name, msg, out, fail=True):
    s = ''
    color = 196 if fail else 46
    s += fg(msg, index=color)
    if len(out) > 0:
        s += fg(sender_name+'\'s output:\n', index=42)
        s += '\n' + out + '\n'
    return s





        
