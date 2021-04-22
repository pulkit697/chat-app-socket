from socket import *
import threading

myServerSocket = socket()
myServerSocket.bind(('', 9999))
client_sockets = []
client_names = []


def remove_from_room(client_socket):
    if client_socket in client_sockets:
        client_sockets.remove(client_socket)


def broadcast(message):
    print(message)
    for client_socket in client_sockets:
        client_socket.send(bytes(message, 'utf-8'))


def broadcast_to_others(_client_socket, message):
    for client_socket in client_sockets:
        if client_socket != _client_socket:
            try:
                client_socket.send(message)
            except:
                client_socket.close()
                remove_from_room(client_socket)


def create_client_thread(client_socket, client_addr):
    client_socket.send(bytes('Server: Welcome to the chat room!', 'utf-8'))
    while True:
        print('listening for ' + str(client_socket))
        message = client_socket.recv(1024).decode()
        if message:
            print(str(client_socket) + ': ' + message)
            broadcast_to_others(client_socket,message)


def connect():
    myServerSocket.listen(100)
    while True:
        client_socket, client_address = myServerSocket.accept()
        broadcast(str(client_address) + ' has joined!')
        client_sockets.append(client_socket)
        client_thread = threading.Thread(target=create_client_thread, args=(client_socket, client_address))
        client_thread.start()


connect()
