import socket
import pickle
import threading
import hashlib

#from pyngrok import ngrok

from Send import send
from Send import send_api
from Encryption import encryption
from Data.data import set_name, get_pswd
from Frontend import frontend


def get_port(s, port=1111):
    if port > 9999:
        raise ValueError('Port must be in [1111, 9999] (I think).')
    try:
        s.bind(("", port))
        return str(port)
    except OSError:
        return get_port(s, port=port + 1)

def get_ip():
    return socket.gethostbyname(socket.gethostname())


# =============================== RECEIVE API =============================== #
"""
def on_receive_msg(data, metadata):
    # Add sender's name to my list of known names
    set_name(metadata['name'], metadata['ra'])
    frontend.on_received(metadata['name'], data)

def on_receive_exec(msg, metadata):
    set_name(metadata['name'], metadata['ra'])
    sender_name = metadata['name']
    ip, port    = metadata['ra']

    send_back_msg = ''
    fail = True

    alert = '\b\b is trying to execute this command \"%s\"' % msg['command']

    # Wrong password
    if msg['pswd'] != get_pswd():
        send_back_msg = 'Wrong password!'
    else:
        send_back_msg = 'Correct password!'
        try:
            send_back_msg = 'Showing output...\n'
            send_back_msg += subprocess.check_output(msg['command'], shell=True).decode('utf-8')
        except:
            send_back_msg = 'Process failed!'
            frontend.error(metadata['name'] + '\'s command failed!')
            frontend.new_carrot()

    send_api.MSG(sender_name, send_back_msg, animation=False)
    #message = {}
    #message['text'] = frontend.command_output(myname, send_back_msg, result, fail=fail)
    #packet = construct_packet(message=message)
    #netcat_thread = threading.Thread(target=send_packet, args=(ip, port, packet))
    #netcat_thread.start()
"""

# ========================================================================== #

def recv_lock_request(lock_req_data, metadata):
    lock, key = encryption.lockandkey()
    packet = {}
    data = {'lock': lock}
    send.set_metadata(packet, metadata)
    send.set_code(packet, 'empty for now')
    send.set_data(packet, data)
    return packet, key

def receive_parse(data):
    '''Returns recv_handler,data,metadata'''
    packet    = pickle.loads(data)
    func_name = send.get_code(packet)
    sent_data = send.get_data(packet)
    metadata  = send.get_metadata(packet)

    return func_name, sent_data, metadata

def got_connection(conn, addr):

    # Check continually for messages from specific IP socket
    with conn:
        decrypt_key = None

        # First reply to the encrypt lock request
        while not decrypt_key:
            data = conn.recv(4096)
            if not data: break

            _, sent_data, metadata = receive_parse(data)
            result, decrypt_key = recv_lock_request(sent_data, metadata)
            conn.sendall(pickle.dumps(result))
            break

        # Then wait for any other general messages
        while True:
            data = conn.recv(4096)
            if not data: continue
            
            decrypted_data = encryption.decrypt(data, decrypt_key)
            func_name, sent_data, metadata = receive_parse(decrypted_data)
            recv_func = send_api.API[func_name].on_recv
            result = recv_func(sent_data, metadata)
            if result: conn.sendall(pickle.dumps(result))
            break

def receive_loop(receiver):
    
    # Listen for any incoming messages
    receiver.listen()

    while True:
        try:
            # Wait for any incoming connections
            conn, addr = receiver.accept()

            # Handle the connection
            t = threading.Thread(target=got_connection, args=(conn, addr))
            t.start()
        except ConnectionAbortedError: # On quit
            break
    
    receiver.close()









def on_receive_game(game_packet, metadata):
    global myname, myaddr
    
    set_name(metadata['name'], metadata['ra'])
    
    ra = metadata['ra']
    sender_name = metadata['name']

    game_object = game_packet['object']
    game_name = type(game_object).__name__

    # Check if opponent one the game
    winner = game_object.winner()
    if winner:
        del active_games[ra]
        print('')
        print(game_object)
        frontend.game_over(myaddr==winner, game_name, myname, sender_name)
        frontend.new_carrot()
        return
    
    # New game
    if ra not in active_games:
        message = {'text': "\b\b has challenged you in %s!" % game_name}
        message['text'] += '\n' + str(game_object) + '\n'
        game_object.set_turn(myaddr)
        
    # Old game, receiving a new move
    else:
        message = {'text': "\b\b has made their move in %s!" % game_name}
        message['text'] += '\n' + str(game_object) + '\n'

    frontend.on_received(sender_name, message)
    active_games[ra] = game_object
    
