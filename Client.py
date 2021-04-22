import socket
import select
import sys
import threading
from tkinter import *

myClientSocket = socket.socket()
root = Tk()
root.geometry('500x300')
messages_frame = Frame(root, bg='green')
messages_frame.pack(side='top', fill='both', expand='yes')
input_frame = Frame(root, bg='red')
input_frame.pack(side='bottom', fill='both')
scroll_bar = Scrollbar(messages_frame, orient='vertical')
scroll_bar.pack(side='right', fill='y')
send_button = Button(input_frame, width=20, text='SEND')
send_button.pack(side='right')
input_box = Entry(input_frame, width=80)
input_box.pack(side='left')


def my_message_box(message):
    Label(messages_frame, text=message).pack(anchor='se', padx=5, pady=5)


def received_message_box(message):
    Label(messages_frame,text=message).pack(anchor='sw', padx=5, pady=5)


def receive_messages():
    while True:
        try:
            message = myClientSocket.recv(1024).decode()
            print(message)
            received_message_box(message)
        except:
            continue


def send_messages():
    while True:
        try:
            var = BooleanVar(False)
            send_button.configure(command=lambda: var.set(True))
            send_button.wait_variable(var)
            message = input_box.get()
            myClientSocket.send(bytes(message, 'utf-8'))
            my_message_box(message)
            input_box.delete(0, 'end')
        except:
            continue


def connect():
    myClientSocket.connect(('localhost', 9999))
    print('Welcome to the chat room!')
    threading.Thread(target=receive_messages).start()
    threading.Thread(target=send_messages).start()
    root.mainloop()

connect()
