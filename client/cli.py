import socket
import sys
import os
import time

# functions to handle and print an error message
def error_checking(message):
    print("Error:", message)

# function to check command is not empty
def handle_command(command):
    if not command:
        error_checking("Empty Command")
        return False
    return True

def main():
    # chekc if proper arguments are there
    if len(sys.argv) != 3:
        error_checking("Incorrect number of arguments")
        return
    # gather arguments and convert type if necessary
    SERVER_IP = sys.argv[1]
    PORT_NUM = sys.argv[2]
    try:
        PORT_NUM = int(PORT_NUM)
    except ValueError:
        error_checking("Invalid Port #")
        return

    # Bufer Size for sending data, must be same as server
    BUFF_SIZE = 65000 

    client_input = ""

    # Establish connection with server
    controller_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        controller_socket.connect((SERVER_IP, PORT_NUM))
    except Exception as e:
        error_checking(f"Connection failed: {e}")
        return

    # Client Loop
    while True:
        # opens new socket at beginning of loop
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((SERVER_IP, PORT_NUM))
        except Exception as e:
            error_checking(f"Connection failed: {e}")
            return
        
        # gather user input
        client_input = input("ftp>")
        if not handle_command(client_input):
            continue

        # send input to server
        client_socket.send(client_input.encode())
        # split command into tokens
        command = client_input.split()
        # execute proper case based off of input
        if command[0] == "get":
            if len(command) == 1:
                error_checking("Missing file name")
                continue
            get(client_socket=client_socket, file_name=command[1],BUFF_SIZE=BUFF_SIZE)
            client_socket.close()
        elif command[0] == "put":
            if len(command) == 1:
                error_checking("Missing file name")
                continue
            put(client_socket=client_socket, file_name=command[1],BUFF_SIZE=BUFF_SIZE)
            client_socket.close()

        elif command[0] == "ls":
            msg = client_socket.recv(1024)
            print(msg.decode(), end="")
            client_socket.close()
        elif client_input == 'quit':
            break
    # close connection
    print("  Goodbye")
    controller_socket.close()
    return

# get
def get(client_socket, file_name:str,BUFF_SIZE):
    print("  Getting " + file_name)
    # open file
    if not client_socket.recv(BUFF_SIZE) == b'not found':
        file = open(file_name, "wb")
        # recieve data from server
        while True:
            msg = client_socket.recv(BUFF_SIZE)
            file.write(msg)
            # if message is less than 1024 bytes, 
            if len(msg) < BUFF_SIZE:
                break
        file.close()
    else:
        print("  File not found in server")

# put    
def put(client_socket, file_name:str,BUFF_SIZE):
    print("  Sending:" + file_name)
    # open file if it exist
    if os.path.exists(file_name):
        client_socket.send(b'good')
        file = open(file_name, 'rb')
        while True:
            buf = file.read(BUFF_SIZE)
            time.sleep(0.05)
            # print("    sending packet")
            client_socket.send(buf)
            # print("    Packet sent")
            if len(buf) < BUFF_SIZE:
                break
        file.close()
    else:
        client_socket.send(b'not found')
        print("  File not found in client")

    

if __name__ == '__main__':
    main()