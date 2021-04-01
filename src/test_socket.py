import socket
import threading
import time
import sys
from random import randint
import frontend
import subprocess
import json

import user_info # not implemented


# error when user joins back in?
# "Could not find that address"

# when user leaves, EXEC 

class ParseError(Exception):
    def __init__(self, message):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        # Now for your custom code...
        self.message = message

# MESSAGES API

def get_ip_and_port(name_or_addr):
    address_str = name_or_addr if name_or_addr not in name_ip else name_ip[name_or_addr]
    try:
        ip, port = address_str.split(':')
    except ValueError:
        raise ParseError('Bad address or name.')
    
    return ip, port

def construct_packet(message={}, execute={}, data=''):
    global myname, myaddr
    d = {'msg': message,
         'exec': execute,
         'data': data,
         'metadata': {'ra': myaddr, 'name': myname}}
    return json.dumps(d)

def set_name(name, data):
    #'''SET - Remember address's name.\nSET <name> <address>'''
    global name_ip
    name_ip[name] = data

def MYNAME(name, *args):
    '''Gives you a new name.\nMYNAME <name>'''
    global myaddr, myname, name_ip
    del name_ip[myname]
    myname = name
    name_ip[name] = myaddr
    
def MYPSWD(new_password, *args):
    '''Gives you a new password.\nMYPSWD <password>'''
    global mypswd
    mypswd = new_password
    
    
def MSG(name, data):
    '''Send a message to a remembered name.\nMSG <name> <message>'''
    #data = frontend.user_color(data)
    
    ip, port = get_ip_and_port(name)
    
    message = {}
    message['text'] = data
    message['color'] = frontend.msg_color
    message['animation'] = True
    
    packet = construct_packet(message=message)
    netcat_thread = threading.Thread(target=send_packet, args=(ip, port, packet))
    netcat_thread.start()

def QUIT(*args):
    '''Quits.\nQUIT'''
    global user_exit, sender, receiver, send_lock
    frontend.goodbye()
    receiver.close()
    sender.close()
    try:
        send_lock.release()
    except RuntimeError:
        pass
    exit(0)

def EXEC(name, data):
    '''Execute a command on someone else's behalf.\nEXEC <name> <password> <command>'''
    
    # Parse
    ip, port = get_ip_and_port(name)
    data_args = data.split(' ')
    password_guess = data_args[0]
    exec_command   = ' '.join(data_args[1:])

    # Handle arguement errors
    if len(password_guess) == 0:
        frontend.error('Empty password.')
        return
    if len(exec_command) == 0:
        frontend.error('Empty command.')
        return

    # Construct packet contents
    message = {}
    message['text']      = '\b\b is trying to execute this command \"%s\"' % exec_command
    message['animation'] = False
    
    execute = {'pswd': password_guess, 'command': exec_command}
    
    packet  = construct_packet(message=message, execute=execute)

    # Send packet to address!
    netcat_thread = threading.Thread(target=send_packet, args=(ip, port, packet))
    netcat_thread.start()
    
    


API = [MSG, EXEC, MYNAME, MYPSWD, QUIT]


# Absolutley no parsing should be handled by API functions....
def parse(s):
    '''Expects s in form "<code> <name> <data>"  '''
    
    s_split = s.split()

    # Will raise NameError if code is wrong
    code = '' if len(s_split) < 1 else s_split[0]

    # Will raise IndexError args are too short
    name = '' if len(s_split) < 2 else s_split[1]

    # Additional args
    args = '' if len(s_split) < 3 else ' '.join(s_split[2:])

    
    # Run arbitrary function with the same name as code

    # Check to see if the code matches a func in the API
    if code not in map(lambda f: f.__name__, API):
        frontend.error('Not a valid command.')
        return

    command = eval(code)
    try:
        command(name, args)
    except ParseError as e:
        frontend.error(e.message)
    except ConnectionRefusedError as e:
        frontend.error(str(e))
        

# RECEIVE API
def on_receive_msg(sender_name, msg, metadata):
    # Add sender's name to my list of known names
    set_name(metadata['name'], metadata['ra'])
    
    frontend.on_received(sender_name, msg)

def on_receive_data(sender_name, msg, metadata):
    pass

def on_receive_exec(sender_name, msg, metadata):
    global myname, mypswd
    
    ip, port = metadata['ra'].split(':')

    
    send_back_msg = ''
    result = ''
    fail = True

    # Wrong password
    if msg['pswd'] != mypswd:
        send_back_msg = 'Wrong password!'
    else:
        send_back_msg = 'Correct password!'
        try:
            result = subprocess.check_output(msg['command'], shell=True).decode('utf-8')
        except:
            result = 'Process failed!'
            frontend.error(metadata['name'] + '\'s command failed!')
            print('> ') # move to frontend somehow
        fail = False

    message = {}
    message['text'] = frontend.command_output(myname, send_back_msg, result, fail=fail)

    packet = construct_packet(message=message)
    netcat_thread = threading.Thread(target=send_packet, args=(ip, port, packet))
    netcat_thread.start()


# Backend
def got_connection(conn, addr):
    global user_exit

    # Check continually for messages from specific IP socket
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            

            decoded = data.decode('utf-8')
            packet = json.loads(decoded)

            sender_name = packet['metadata']['name']
            
            for k, v in packet.items():
                # Skip if metadata key or no value from key
                if k == 'metadata' or not len(v): continue

                # Call the receive handler
                on_receive_func = eval('on_receive_%s' % k)
                on_receive_func(sender_name, v, packet['metadata'])
            

def find_port(s, port=1111):
    if port > 9999:
        raise ValueError('Port must be in [1111, 9999] (I think).')
    try:
        s.bind(("", port))
        return port
    except OSError:
        return find_port(s, port=port + 1)

'''
def send_packet(host, port, content):
    global sender, send_lock

    send_lock.acquire()
    try:
        sender.connect((host, int(port)))
    except OSError: # Already connected errr
        pass
        #send_lock.release()
        #return
    send_lock.release()

    send_lock.acquire()

    # Error is below somewhere
    try:
        sender.sendall(content.encode())
    except BrokenPipeError:
        frontend.error('Could not find that address.')
    except OSError:
        frontend.error('Could not find that address.')
    send_lock.release()
'''

def send_packet(host, port, content):
    
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sender.connect((host, int(port)))
        sender.sendall(content.encode())
        sender.shutdown(socket.SHUT_WR)
        sender.close()
    except ConnectionRefusedError:
        frontend.error('Could not find address.')
    except OSError:
        frontend.error('OS Error.')
    except ValueError:
        frontend.error('That ain\'t an address!')
        
        
    


def send():
    '''Listens for any command the user types and sends'''
    while True:
        time.sleep(0.15)
        send_packet = input(frontend.message_prompt())
        parse(send_packet)

if __name__ == '__main__':
    # read name and password
    myname = 'Default' + 'ABCDEFG'[randint(0, 6)]
    mypswd = ''.join(chr(randint(ord('a'), ord('z'))) for i in range(64))
    myaddr = ''
    
    # Mappings to keep track of named IP addresses
    name_ip = {}

    IP = socket.gethostbyname(socket.gethostname())

    exit_lock = threading.Lock()
    user_exit = False

    send_lock = threading.Lock()

    frontend.set_user_color()

    receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = find_port(receiver)
    myaddr = ':'.join((IP,str(port)))
    frontend.welcome()
    frontend.user_info(myname, myaddr)
    frontend.commands()

    set_name(myname, myaddr) # Add your own name to known names
        
    receiver.listen()

    sender_thread = threading.Thread(target=send)
    sender_thread.start()
        
    while True:
        try:
            conn, addr = receiver.accept()
            t = threading.Thread(target=got_connection, args=(conn, addr))
            t.start()
        except ConnectionAbortedError: # On quit
            break

    sender.close()
    receiver.close()
            
        
        

        

        










        
