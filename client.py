import socket
import threading

display_name = input("Choose a Display name: ")
HOST = '127.0.0.1' #localhost
PORT = 9989

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

#handles messages from server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'Please choose a display name':
                client.send(display_name.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f"{display_name}: {input()}"
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

receive_thread.start()
write_thread.start()