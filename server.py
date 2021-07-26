import threading
import socket
import os

HOST = '127.0.0.1' #localhost
PORT = 9989

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print("Server listening")

clients = {}

def broadcast(message):
    for client in clients:
        client.send(message)

# handles client messages
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
            print(message)
        except:
            display_name = clients[client]
            del clients[client]
            client.close()
            broadcast(f'{display_name}, has left the chat'.encode('utf-8'))
            break

#initialises connections with clients
def receive():
    while True:
        client, address = server.accept()
        print(f"connected with client, address: {address}")

        client.send("Please choose a display name".encode('utf-8'))
        display_name = client.recv(1024).decode('utf-8')
        clients[client] = display_name
        print(f"display_name of the client is {display_name}!")
        broadcast(f"{display_name} has joined the chat!".encode('utf-8'))

        thread = threading.Thread(target = handle, args =(client,))
        thread.start()

def control():
    while True:
        userin = input()
        if userin =='quit':
            print("exiting server")
            os._exit(1) 
        elif userin == 'size' or userin == 'how many':
            print(len(clients))
        elif userin == 'users':
            for client in clients:
                print(clients[client])

receive_thread = threading.Thread(target = receive)
control_thread = threading.Thread(target = control)

receive_thread.start()
control_thread.start()

#receive method is MAIN method