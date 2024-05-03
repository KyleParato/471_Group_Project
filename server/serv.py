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
    # check arguments
    if len(sys.argv) != 2:
        error_checking("Incorrect number of arguments")
        return

    # Gather and convert Port Number
    PORT_NUM = sys.argv[1]
    try:
        PORT_NUM = int(PORT_NUM)
    except ValueError:
        error_checking("Invalid Port #")
        return

    # Default server IP
    SERVER_IP = "127.0.0.1"

    # Buffer Size for sending data, must be same size as client
    BUFF_SIZE = 65000

    # Set up sever, tcp, ip is local host, 100 connection queue, add a timeout
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, PORT_NUM))
    server_socket.listen(100)
    server_socket.settimeout(500)

    # Server Loop
    # print statements can be removed, added to show process
    while True:
        print("Waiting for Client")

        # accept client conection
        try:
            controller_socket, controller_info = server_socket.accept()
        except socket.timeout:
            error_checking("Error.")
            continue

        # Loop to handle client
        while True:
            # accepts each new data socket
            try:
                client_socket, client_info = server_socket.accept()
            except socket.timeout:
                error_checking("Socket timeout occurred.")
                continue

            # wait for client command
            print("  Waiting for command")
            try:
                data = client_socket.recv(1024)
            except Exception as e:
                error_checking(f"  Error receiving command: {e}")
                break
            if not data:
                break
            print("  Recieved Command")

            command = data.decode().strip()
            if not handle_command(command):
                continue

            # get tokens from client command
            command = command.split()
            # hand command line logic
            # quit case
            if command[0] == 'quit':
                break
            # get case
            elif command[0] == "get":
                if len(command) == 1:
                    error_checking("  Missing file name")
                    continue
                print("  " + command[1])
                get(client_socket=client_socket,file_name=command[1],BUFF_SIZE=BUFF_SIZE)
                client_socket.close()
            # put case
            elif command[0] == "put":
                if len(command) == 1:
                    error_checking("  Missing file name")
                    continue
                put(client_socket=client_socket, file_name=command[1],BUFF_SIZE=BUFF_SIZE)
                client_socket.close()
            # list case
            elif command[0] == "ls":
                print("  Recieved command ls")
                ls(client_socket=client_socket)
                print("  Finished ls request")
                client_socket.close()
            # not a valid command
            else:
                error_checking("Command not found")
        # close connection when finished with client
        controller_socket.close()
    
# get
def get(client_socket, file_name:str,BUFF_SIZE):
    print("    Starting get: " + file_name)
    # open file if the file exists in the server
    if os.path.exists(file_name):
        client_socket.send(b'good')
        file = open(file_name, "rb")
        # read file in 1024 bytes and send to client
        while True:
            print("    Sending packet")
            buf = file.read(BUFF_SIZE)
            time.sleep(0.05)
            client_socket.send(buf)
            # if buffer is empty, file is completley read
            if len(buf) < BUFF_SIZE:
                break
        # close file
        file.close()
        print("    Complete")
    else:
        client_socket.send(b'not found')
        print("    File not found in server")

# put
def put(client_socket, file_name:str,BUFF_SIZE):
    print("    Starting put: " + file_name)
    # open file
    if not client_socket.recv(BUFF_SIZE) == b'not found':
        file = open(file_name, "wb")
        # wait for packets from client, write to file
        while True:
            print("    Recieveing packet")
            msg = client_socket.recv(BUFF_SIZE)
            print("      got it")
            file.write(msg)
            # if recieved message is less than 1024, end of file
            if len(msg) < BUFF_SIZE:
                break 
        # close file and exit
        file.close()
        print("    Complete put")
    else:
        print("    File not found in client")
# list
def ls(client_socket):
    print("    Starting ls")
    # gather files from current directory
    file_list = os.listdir()
    output = ''
    # send all files to client unless it is the server file (in one string) 
    for file in file_list:
        if file != 'serv.py':
            output += "  "
            output += file
            output += '\n'
    client_socket.send(output.encode())
    print("    ls sent")
    
if __name__ == '__main__':
    main()