import rsa
import pickle
import hashlib

# Use chunks because:
# "RSA can only encrypt messages that are smaller than the key."
# "A 512-bit key can encode a 53-byte message"
chunk_size = 53

def lockandkey():
    '''Returns RSA lock and key pair'''
    return rsa.newkeys(512)

def encrypt(data, lock):    
    chunks = [data[x:x+chunk_size] for x in range(0, len(data), chunk_size)]
    chunks = [rsa.encrypt(x, lock) for x in chunks]
    return pickle.dumps(chunks) # Pickled onion!

def decrypt(data, key):
    chunks = pickle.loads(data)
    decrypted_chunks = [rsa.decrypt(x, key) for x in chunks]
    return b''.join(decrypted_chunks)

def sha_hash(pswd):
    return hashlib.sha224(pswd.encode('utf-8')).hexdigest()