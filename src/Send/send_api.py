import threading
import subprocess

from Frontend import frontend
from Data.data import get_myname, get_myaddr, get_ip_port, set_name, set_myname, set_pswd, get_pswd
from Send.send import send, set_data, set_code
from Receive import recv
from Encryption.encryption import sha_hash



class ParseError(Exception):
    def __init__(self, message):
        super().__init__(message); self.message = message

class APIFunc(object):

     @staticmethod 
     def grammar():
          return 'null grammar'

     @classmethod
     def parse(cls, string):
          args   = string.split()
          tokens = cls.grammar().split()[1:] # Ignore the function name token
          last_element = lambda i: i == len(tokens) - 1

          # Wat the fak
          try:
               result = [' '.join(args[i:]) if last_element(i) else args[i] for i in range(len(tokens))]
          except IndexError:
               raise ParseError('Not enough arguements!')

          return tuple(result)

     @staticmethod
     def __call__(string):
          raise Exception('Unimplemented!')
          
     @staticmethod
     def on_recv(data, metadata):
          pass

     @staticmethod 
     def description():
          return 'null description'

class MSG(APIFunc):

     @staticmethod 
     def grammar():
          return 'MSG <recipient> <message>'

     @staticmethod
     def __call__(recipient, message, **kwargs):

          myname = get_myname()
          myaddr = get_myaddr()
          ip, port = get_ip_port(recipient)

          packet = {}
          message_packet = {'text': message, 'animation': True, 'color': frontend.msg_color}
          for k,v in kwargs.items(): message_packet[k] = v

          set_data(packet, message_packet)
          set_code(packet, MSG.__name__)

          t = threading.Thread(target=send, args=(packet, ip, port))
          t.start()

     @staticmethod
     def on_recv(data, metadata):
          set_name(metadata['name'], metadata['ra'])
          frontend.on_received(metadata['name'], data)

     @staticmethod 
     def description():
          return 'Send a message to an address or remembered name.'

class MYNAME(APIFunc):

     @staticmethod 
     def grammar():
          return 'MYNAME <name>'
     
     @staticmethod
     def __call__(name):
          set_myname(name)
          set_name(name, get_myaddr())
     
     @staticmethod 
     def description():
          return 'Gives you a new name.'

class QUIT(APIFunc):

     @staticmethod 
     def grammar():
          return 'QUIT'

     @classmethod
     def parse(cls, string):
          return tuple()
     
     @staticmethod
     def __call__(*args):
          frontend.goodbye()
          return 1 # Return 1 to exit
     
     @staticmethod 
     def description():
          return 'Quits the program.'

class MYPSWD(APIFunc):

     @staticmethod 
     def grammar():
          return 'MYPSWD <password>'
     
     @staticmethod
     def __call__(password):
          set_pswd(password)
     
     @staticmethod 
     def description():
          return 'Gives you a new password.'

class EXEC(APIFunc):

     @staticmethod 
     def grammar():
          return 'EXEC <name> <password> <command>'

     @staticmethod
     def __call__(name, password, command):
          ip, port = get_ip_port(name)

          # Handle arguement errors
          if len(password) == 0:
               raise ParseError('Empty password.')
          if len(command) == 0:
               raise ParseError('Empty command.')

          exec_packet = {}
          exec_data = {'pswd': sha_hash(password), 'command': command}
          set_data(exec_packet, exec_data)
          set_code(exec_packet, EXEC.__name__)

          # Send packet to address!
          t = threading.Thread(target=send, args=(exec_packet, ip, port))
          t.start()

     @staticmethod
     def on_recv(data, metadata):
          set_name(metadata['name'], metadata['ra'])
          sender_name = metadata['name']
          ip, port    = metadata['ra']
          #alert = '\b\b is trying to execute this command \"%s\"' % msg['command']

          # Wrong password
          if data['pswd'] != get_pswd():
               send_back_msg = 'Wrong password!'
          else:
               send_back_msg = 'Correct password!'
               try:
                    send_back_msg = 'Showing output...\n'
                    send_back_msg += subprocess.check_output(data['command'], shell=True).decode('utf-8')
               except:
                    send_back_msg = 'Process failed!'
                    frontend.error(metadata['name'] + '\'s command failed!')
                    frontend.new_carrot()
          
          MSG()(sender_name, send_back_msg, animation=False)

     @staticmethod 
     def description():
          return 'Execute a command on someone else\'s behalf.'

# Registered API functions
API = {} # MSG, QUIT, MYNAME, MYPSWD, EXEC

def register(api_func):
     global API
     API[api_func.__name__] = api_func

for x in [MSG, QUIT, MYNAME, MYPSWD, EXEC]:
     register(x)


"""
def MYNAME(name, *args):
    '''Gives you a new name.\nMYNAME <name>'''
    set_myname(name)
    set_name(name, get_myaddr())

def MSG(name, data, **kwargs):
    
    
    myname = get_myname()
    myaddr = get_myaddr()
    
    ip, port = get_ip_port(name)
    
    packet = {}
    message = {'text': data, 'animation': True, 'color': frontend.msg_color}
    for k,v in kwargs.items(): message[k] = v

    set_data(packet, message)
    set_recv_handler(packet, recv.on_receive_msg)

    t = threading.Thread(target=send, args=(packet, ip, port))
    t.start()


def QUIT(*args):
    '''Quits.\nQUIT'''
    frontend.goodbye()
    return 1 # Return 1 to exit


def MYPSWD(new_password, *args):
    '''Gives you a new password.\nMYPSWD <password>'''
    set_pswd(new_password)


def EXEC(name, data):
    '''Execute a command on someone else's behalf.\nEXEC <name> <password> <command>'''

    # Parse...
    ip, port = get_ip_port(name)
    data_args = data.split(' ')
    password_guess = data_args[0]
    exec_command   = ' '.join(data_args[1:])

    # Handle arguement errors
    if len(password_guess) == 0:
        frontend.error('Empty password.'); return
    if len(exec_command) == 0:
         frontend.error('Empty command.'); return

    exec_packet = {}
    exec_data = {'pswd': sha_hash(password_guess), 'command': exec_command}
    set_data(exec_packet, exec_data)
    set_recv_handler(exec_packet, recv.on_receive_exec)

    # Send packet to address!
    netcat_thread = threading.Thread(target=send, args=(exec_packet, ip, port))
    netcat_thread.start()

def PLAY(name, data):
    '''Open a game with someone.\nPLAY <name> <game> <args>'''
    global myaddr
    
    ip, port = get_ip_and_port(name)

    split_data = data.split()
    game_type  = split_data[0]
    game_args  = split_data[1:]
    game_module = '%sClass.%s' % (game_type, game_type)
    game_class = eval(game_module)
    game = game_class([myaddr, ip+':'+port], *game_args)

    # Create the game on my end
    active_games[ip+':'+port] = game

    # Send the PLAY to other
    game_packet = {'object': game}
    packet = construct_packet(game=game_packet, use_pickle=True)
    netcat_thread = threading.Thread(target=send_packet, args=(ip, port, packet))
    netcat_thread.start()

def MOVE(name, data):
    '''Make a move in an opened game.\nMOVE <name> <args>'''
    global myaddr, myname
    
    ip, port = get_ip_and_port(name)
    addr = ip+':'+port
    if addr not in active_games:
        raise GameInterface.GameError('Not in a game with %s.' % name)

    game = active_games[addr]

    args = data.split()
    result = game.move(myaddr, *args)

    # Check game over
    #message = {}
    winner = game.winner()
    if winner:
        game_name = type(game).__name__
        del active_games[addr]
        opponent_message = frontend.game_over(myaddr==winner, game_name, myname, name)
        #message['text'] = opponent_message

    # Display the game
    print(game)
    
    # Send results back to opponent
    game_packet = {'object': game}
    packet = construct_packet(game=game_packet, use_pickle=True)
    netcat_thread = threading.Thread(target=send_packet, args=(ip, port, packet))
    netcat_thread.start()
"""

