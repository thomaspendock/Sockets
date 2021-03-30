import socket
import threading
import time
import sys
from macColors import *
from random import randint

MYNAME = 'ME' # Used to identify ME as a name

# Mappings to keep track of named IP addresses
name_ip = {}
ip_name = {}

IP = socket.gethostbyname(socket.gethostname())

exit_lock = threading.Lock()
user_exit = False

msg_color = randint(17, 231)

def got_connection(conn, addr):
    global user_exit

    # Check continually for messages    
    with conn:

        while True:
            
            data = conn.recv(1024)
            if not data:
                break
            
            s_addr = addr[0]
            sender_name = s_addr if s_addr not in ip_name else ip_name[s_addr]
            print(sender_name+':', data.decode('utf-8'))
            
    

def find_port(s, port=1111):
    if port > 9999:
        raise ValueError('Port must be in [1111, 9999] (I think).')
    try:
        s.bind(("", port))
        return port
    except OSError:
        return find_port(s, port=port + 1)

def SET(name, data):
    #print('set called')
    name_ip[data] = name
    ip_name[name.split(':')[0]] = data
    #print(name_ip)


def netcat(host, port, content):
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender.connect((host, int(port)))
    sender.sendall(content.encode())
    sender.shutdown(socket.SHUT_WR)
    while True:
        data = sender.recv(4096)
        if not data:
            break
    sender.close()

def send_msg(host, port, content):
    global sender

    try:
        sender.connect((host, int(port)))
    except OSError: # Already connected errr
        pass
        
    sender.sendall(content.encode())
    

def MSG(name, data):
    ip, port = name_ip[name].split(':')

    netcat_thread = threading.Thread(target=send_msg, args=(ip, port, data))
    netcat_thread.start()

def QUIT():
    global user_exit, sender, receiver
    print(fg('Goodbye.', index=196))
    receiver.close()
    exit(0)
    
def parse(s):
    if s.lower() == 'q':
        QUIT()

        
    # s = code name data
    s_split = s.split()
    if len(s_split) < 3:
        print('Not a valid command.')
        return
    
    code = s_split[0]
    name = s_split[1]
    data = ' '.join(s_split[2:])
    data = fg(data, index=msg_color)

    # Run arbitrary function with the same name as code
    command = '%s(\'%s\', \'%s\')' % (code, name, data)
    exec(command)

    

def send():
    '''Listens for any command the user types and sends'''
    while True:
        time.sleep(0.15)
        send_msg = input('> ')#input('Send something: ')
        
        parse(send_msg)

def border(s, w, h, s_width=None, rgb=None, index=256):
    s_lines  = s.split('\n')
    if s_lines[-1] == '': s_lines = s_lines[:-1]
    s_height = len(s_lines)
    if not s_width:
        s_width = len(s_lines[0])
    verti_border = bg(' '*2, rgb=rgb, index=index)
    horiz_border = bg((' ' * s_width) + 2 * (w+1) * verti_border, rgb=rgb, index=index)

    border_s = ''
    
    border_s += horiz_border + '\n'
    
    for i in range(h):
        border_s += verti_border
        border_s += ' ' * (w * 4 + s_width)
        border_s += verti_border + '\n'

    for i in range(s_height):
        border_s += verti_border
        border_s += ' ' * (w * 2)
        border_s += s_lines[i]
        border_s += ' ' * (w * 2)
        border_s += verti_border + '\n'
    
    for i in range(h):
        border_s += verti_border
        border_s += ' ' * (w * 4 + s_width)
        border_s += verti_border + '\n'
    
    border_s += horiz_border + '\n'

    return border_s, s_width + 4 * w + 4
    
    

def welcome():
    '''Prints welcome and info'''
    welcome_msg  = '---===<<<( WELCOME )>>>===---'
    b1, rw = border(welcome_msg, 1, 1, index=237)
    b2, rw = border(b1, 0, 0, rw, index=243)
    b3, rw = border(b2, 0, 0, rw, index=247)
    print(b3)

    your_address = bg('Your address: ' + host_address, rgb=(0,3,3))
    print(your_address)
    print('')

    command_color = 117
    comment_color = 115
    commands =  fg('Commands:\n', index=command_color)
    commands += fg('------------------------------------------------------------\n', index=243)
    commands += fg('SET <address> <name>       ', index=command_color)
    commands += fg('# Remembers address\'s name\n', index=comment_color)
    commands += fg('MSG <name> <message/data>  ', index=command_color)
    commands += fg('# Send data to the remembered name\n', index=comment_color)
    commands += fg('q                          ', index=command_color)
    commands += fg('# quit\n', index=comment_color)

    print(commands)

    print('')
 
receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

port = find_port(receiver)
host_address = ':'.join((IP,str(port)))
welcome()
name_ip[MYNAME] = host_address # So i can talk to myself
ip_name[IP] = MYNAME
    
receiver.listen()

sender_thread = threading.Thread(target=send)
sender_thread.start()
    
while True:

    #exit_lock.acquire()
    #if user_exit: break
    #exit_lock.release()

    try:
        conn, addr = receiver.accept()
        t = threading.Thread(target=got_connection, args=(conn, addr))
        t.start()
    except ConnectionAbortedError:
        break
    
    
        
        
sender.close()
receiver.close()
        
        
        

        

        










        
