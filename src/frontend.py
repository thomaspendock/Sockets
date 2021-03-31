from grafix import *
from macColors import *
from random import randint
from test_socket import API

msg_color = 255 # Default: white

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
    max_title_len = 48
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
        title, usage = cmd.__doc__.split('\n')
        spacing = ' ' * (max_title_len-len(title)) # If neg this breaks
        commands += fg(title, index=command_color) + spacing + fg(usage, index=comment_color)
        commands += '\n'
    #commands += fg('SET <name> <address>', index=command_color)
    #commands += fg('# Remembers address\'s name\n', index=comment_color)
    #commands += fg('MSG <name> <message>', index=command_color)
    #commands += fg('# Send data to the remembered name\n', index=comment_color)
    #commands += fg('QUIT', index=command_color)
    #commands += fg('# Quit\n', index=comment_color)
    commands += '\n'
    print(commands)

def user_info(user_address):
    your_address = bg('Your receiving address: ' + user_address, rgb=(0,3,3)) + '\n'
    print(your_address)

def goodbye():
    print(fg('Goodbye.', index=196))

def error(error_msg):
    print(fg(error_msg, index=196))

def user_color(msg):
    global msg_color
    
    return fg(msg, index=msg_color)

def message_prompt():
    return '> '

def on_received(sender_name, message):
    print(sender_name+':', message)









        
