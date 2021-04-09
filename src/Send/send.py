import socket
import pickle
import time
import random



from Send.send_api import *
from Encryption import encryption
from Compression import compression

from Data.data import get_myname, get_myaddr
from Receive import recv

# State graph

DATAKEY = 'data'
CODEKEY = 'code'
METADATA = 'metadata'


def set_data(packet, data):
    packet[DATAKEY] = data
    return packet

def set_code(packet, code):
    packet[CODEKEY] = code
    return packet

def set_metadata(packet, metadata):
    packet[METADATA] = metadata
    return packet

def get_data(packet):
    return packet[DATAKEY]

def get_code(packet):
    return packet[CODEKEY]

def get_metadata(packet):
    return packet[METADATA]

def gen_request_id():
    return str(time.time()) + str(random.random())

def construct_packet(packet, encrypt_lock=None):
    global MYADDR, MYNAME

    if DATAKEY not in packet or CODEKEY not in packet:
        raise ValueError('No data or recv handler')

    packet[METADATA] = { 'ra': get_myaddr(), 'name': get_myname() }
    byte_data = pickle.dumps(packet) # Second pickle... pickled onion?
    
    if encrypt_lock: 
        byte_data = encryption.encrypt(byte_data, encrypt_lock)
    
    return byte_data

def send_lock_request(host, port):
    '''Asks host:port for an ecryption key'''
    packet = {}
    set_data(packet, None)
    set_code(packet, send_lock_request.__name__)
    lock_request_packet = construct_packet(packet)
    return lock_request_packet

def send(dict_packet, host, port):
    '''Sends content (bytes) to host:port'''
    
    # Open the connection
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender.connect((host, int(port)))

    # Send the request for the encryption lock
    lock_request_packet = send_lock_request(host, port)
    sender.sendall(lock_request_packet)

    # Wait for a lock response
    encrypt_lock = None
    while True:
        data = sender.recv(4096)
        if not len(data): continue

        # Parse the lock reply
        _, reply_data, metadata = recv.receive_parse(data)
        encrypt_lock = reply_data['lock']

        # Encrypt and send the actual message
        tosend = construct_packet(dict_packet, encrypt_lock=encrypt_lock)
        tosend = compression.compress(tosend)

        sender.sendall(tosend)
        break

    # Close the connection
    sender.shutdown(socket.SHUT_WR)
    sender.close()