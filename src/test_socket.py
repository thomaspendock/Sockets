import socket
import threading
import time
import sys
from random import randint
import frontend


# MESSAGES API
def SET(name, data):
    '''SET - Remember address's name.\nSET <name> <address>'''
    name_ip[name] = data
    ip_name[data.split(':')[0]] = name


def MSG(name, data):
    '''MSG - Send a message to a remembered name.\nMSG <name> <message>'''
    data = frontend.user_color(data)
    try:
        ip, port = name_ip[name].split(':')
    except KeyError:
        raise KeyError

    netcat_thread = threading.Thread(target=send_msg, args=(ip, port, data))
    netcat_thread.start()

def QUIT(*args):
    '''QUIT - Quits.\nQUIT'''
    global user_exit, sender, receiver
    frontend.goodbye()
    receiver.close()
    exit(0)



API = [SET, MSG, QUIT, EXEC]

def parse(s):
    '''Expects s in form "<code> <name> <data>"  '''
    
    s_split = s.split()
    code = '' if len(s_split) < 1 else s_split[0]
    name = '' if len(s_split) < 2 else s_split[1]
    data = '' if len(s_split) < 3 else ' '.join(s_split[2:])
    
    # Run arbitrary function with the same name as code
    command = '%s(\'%s\', \'%s\')' % (code, name, data)
    try:
        exec(command)
    except NameError:
        frontend.error('Not a valid command.')
    except KeyError:
        frontend.error('Unknown name.')


# Backend
def got_connection(conn, addr):
    global user_exit

    # Check continually for messages from specific IP socket
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            s_addr = addr[0]
            sender_name = s_addr if s_addr not in ip_name else ip_name[s_addr]
            frontend.on_received(sender_name, data.decode('utf-8'))
            

def find_port(s, port=1111):
    if port > 9999:
        raise ValueError('Port must be in [1111, 9999] (I think).')
    try:
        s.bind(("", port))
        return port
    except OSError:
        return find_port(s, port=port + 1)
    
def send_msg(host, port, content):
    global sender

    try:
        sender.connect((host, int(port)))
    except OSError: # Already connected errr
        pass
        
    sender.sendall(content.encode())


def send():
    '''Listens for any command the user types and sends'''
    while True:
        time.sleep(0.15)
        send_msg = input(frontend.message_prompt())
        parse(send_msg)

if __name__ == '__main__':
    MYNAME = 'ME' # Used to identify ME as a name

    # Mappings to keep track of named IP addresses
    name_ip = {}
    ip_name = {}

    IP = socket.gethostbyname(socket.gethostname())

    exit_lock = threading.Lock()
    user_exit = False

    frontend.set_user_color()

    receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = find_port(receiver)
    host_address = ':'.join((IP,str(port)))
    frontend.welcome()
    frontend.user_info(host_address)
    frontend.commands()

    name_ip[MYNAME] = host_address # So i can talk to myself
    ip_name[IP] = MYNAME
        
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
            
        
        

        

        










        
