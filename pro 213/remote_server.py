import socket
from  threading import Thread
from pynput.mouse import Button, Controller
from screeninfo import get_monitors
from pynput.keyboard import Key, Controller

SERVER = None
PORT = 8000
IP_ADDRESS = input("Enter your computer IP ADDR : ").strip()
#IP_ADDRESS = "192.168.0.111"
screen_width = None
screen_height = None

keyboard = Controller()

def getDeviceSize():
    global screen_width
    global screen_height
    for m in get_monitors():
        screen_width = int(str(m).split(",")[2].strip().split('width=')[1])
        screen_height = int(str(m).split(",")[3].strip().split('height=')[1])

def recvMessage(client_socket):
    global keyboard

    while True:
        try:
            message = client_socket.recv(2048).decode()
            if(message):
                new_message  = eval(message)
                #Press and release space
               
                keyboard.press(message)
                keyboard.release(message)
                print(message)           
        
        except Exception as error:
            pass

def acceptConnections():
    global SERVER
    while True:
        client_socket, addr = SERVER.accept()
        print(f"Connection established with {client_socket} : {addr}")
        thread1 = Thread(target = recvMessage, args=(client_socket,))
        thread1.start()


def setup():
    print("\n\t\t\t\t\t*** Welcome To Remote Mouse ***\n")
    global SERVER
    global PORT
    global IP_ADDRESS
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(10)
    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...\n")
    getDeviceSize()
    acceptConnections()

setup()
