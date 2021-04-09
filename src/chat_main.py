import socket
import threading
import time
import sys
from random import randint, choice
from Frontend import frontend
from Send.send_api import *
from Receive import recv

import subprocess
import json
from Games import TicTacToeClass
from Games import GameInterface
import pickle

from Receive import recv

from Data.data import set_myname, set_myaddr, set_name

# import user_info # not implemented

# error when user joins back in?
# "Could not find that address"
# when user leaves, EXEC
# TAKE A WHILE W 5 by 5 board
# game ends??
# name --> active game (only 1)
active_games = dict()

def addr_str(ip_port):
    return ':'.join(ip_port)

# Absolutley no parsing should be handled by API functions....
class ParseError(Exception):
    def __init__(self, message):
        super().__init__(message); self.message = message

def parse(s):
    '''Expects s in form "<code> <name> <data>" 
    Calls an api function from send_api'''
    
    if len(s.split()) < 1: return 
    
    func_name = s.split()[0]
    func_args = ' '.join(s.split()[1:])

    if func_name not in API:
        frontend.error('Not a valid command.')
        return

    command = API[func_name]()
    try:
        func_args = API[func_name].parse(func_args)
        return command(*func_args)
    except ParseError as e:
        frontend.error(e.message)
    except ConnectionRefusedError as e:
        frontend.error(str(e))
    except GameInterface.GameError as e:
        frontend.error(e.message)

        
# The send thread
def send_loop():
    '''Listens for any command the user types and sends'''

    while True:
        time.sleep(0.05)
        user_cmd = input(frontend.message_prompt())
        r = parse(user_cmd)
        if r: break


if __name__ == '__main__':
    # read name and password
    myname = 'Default' + choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # Choose a random color
    frontend.set_user_color()

    receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    myip   = recv.get_ip()
    myport = recv.get_port(receiver)
    myaddr = (myip, myport)

    set_myname(myname)
    set_myaddr(myaddr)
    set_name(myname, myaddr)

    frontend.welcome()
    frontend.user_info(myname, addr_str(myaddr))
    frontend.commands()

    receiver_thread = threading.Thread(target=recv.receive_loop, args=[receiver])
    receiver_thread.daemon = True
    receiver_thread.start()

    send_loop()
