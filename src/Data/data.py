from random import randint
from Encryption.encryption import sha_hash

MYADDR = None
MYNAME = None
MYPSWD = ''.join(chr(randint(ord('a'), ord('z'))) for i in range(128))

name_ip = {} # Mappings to keep track of named IP addresses. lets have addresses be unique
ip_name = {} # EXACT reverse mapping of name_ip... EXACT!!

def get_ip_port(name_or_addr):

  ip_port = name_or_addr if name_or_addr not in name_ip else name_ip[name_or_addr]
  if type(ip_port) is str:
    ip, port = ip_port.split(':')
  else:
    ip, port = ip_port
  return ip, port

def set_name(name, addr):
  global name_ip, name_ip

  # Keep each address unique
  if addr in ip_name:
    old_name = ip_name[addr]
    del ip_name[addr]
    del name_ip[old_name]

  ip_name[addr] = name 
  name_ip[name] = addr

def set_myname(name):
  global MYNAME
  MYNAME = name

def set_myaddr(addr):
  global MYADDR
  MYADDR = addr

def set_pswd(pswd):
  global MYPSWD
  MYPSWD = sha_hash(pswd)

def get_myname():
  return MYNAME

def get_myaddr():
  return MYADDR
  
def get_pswd():
  return MYPSWD

