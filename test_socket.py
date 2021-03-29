import socket
import threading

MYNAME = 'Thomas'
name_ip = {}

#PORT = 1111 # somtimes port is taken...
IP   = socket.gethostbyname(socket.gethostname())

allcons = set()

def got_connection(conn, addr):
    print("GOT CONNECTION FROM", str(addr))
    with conn:
        while True:
            data = conn.recv(1024)
            
            if not data:
                break
            
            print("GOT SOME DATA", addr, data)
            print(data.decode('utf-8'))
            
            
            for c in allcons:
                hdr = "Message from %s: "%str(addr)
                try:
                    c.sendall(hdr.encode("utf-8") + data)
                except IOError:
                    pass

def find_port(s, port=1111):
    if port > 9999:
        raise ValueError('Port must be in [1111, 9999] (I think).')
    try:
        s.bind(("", port))
        return port
    except OSError:
        return find_port(s, port=port + 1)

def SET(name, data):
    print('set called')
    name_ip[data] = name
    print(name_ip)


def netcat(host, port, content):
    #print('nc called...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096)
        if not data:
            break
        print(repr(data))
    s.close()
    #print('nc closed.')

def MSG(name, data):
    print('MSG called')
    ip, port = name_ip[name].split(':')
    netcat(ip, port, data)
    
def parse(s):
    # code name data
    s_split = s.split()
    code = s_split[0]
    name = s_split[1]
    data = ' '.join(s_split[2:])
    print(code, name, data)

    command = '%s(\'%s\', \'%s\')' % (code, name, data)
    exec(command)

    

def send():
    
    while True:
        
        send_msg = input('Send something: ')
        parse(send_msg)
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    port = find_port(s)
    host_address = ':'.join((IP,str(port)))
    print('Host: ', host_address)
    name_ip[MYNAME] = host_address # So i can talk to myself
    
    s.listen()
    while True:
        print('started thread 2')
        t2 = threading.Thread(target=send) #args=(conn, addr))
        t2.start()
        
        conn, addr = s.accept()
        allcons.add(conn)
        t = threading.Thread(target=got_connection, args=(conn, addr))
        t.start()

        

        










        
