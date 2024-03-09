import socket
import sys
import os
import time

def main():

    if len(sys.argv) != 2:
        print("Incorrect number of arguments")
        return

    # Gather Port Number
    PORT_NUM = sys.argv[1]
    PORT_NUM = int(PORT_NUM)

    SERVER_IP = "127.0.0.1"

    # Set up sever, tcp, ip is local host, 100 connection queue
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, PORT_NUM))
    server_socket.listen(100)
    server_socket.settimeout(500)
    # Server Loop
    while True:
        print("Waiting for Client")

        client_socket, client_info = server_socket.accept()

        # Loop to handle client
        while True:
            print("  Waiting for command")
            data = client_socket.recv(1024)
            print("  Recieved Command")
            data = data.decode()

            # get tokens from command line
            command = data.split()
            if data == 'quit':
                break
            elif command[0] == "get":
                if len(command) == 1:
                    print("  Missing file name")
                    continue
                print("  " + command[1])
                get(client_socket=client_socket,file_name=command[1])
            elif command[0] == "put":
                if len(command) == 1:
                    print("  Missing file name")
                    continue
                put(client_socket=client_socket, file_name=command[1])
            elif command[0] == "ls":
                print("  Recieved command ls")
                ls(client_socket=client_socket)
                print("  Finished ls request")
            else:
                print("  Command not found")

        client_socket.close()
    
def get(client_socket, file_name:str):
    print("    Starting get: " + file_name)
    file = open(file_name, "rb")
    while True:
        # print("    Sending packet")
        buf = file.read(1024)
        time.sleep(0.005)
        client_socket.send(buf)
        if len(buf) < 1024:
            break
    file.close()
    print("    Complete")

def put(client_socket, file_name:str):
    print("    Starting put: " + file_name)
    file = open(file_name, "wb")
    while True:
        # print("    Recieveing packet")
        msg = client_socket.recv(1024)
        # print("      got it")
        file.write(msg)
        if len(msg) < 1024:
            break 
    file.close()
    print("    Complete put")

def ls(client_socket):
    print("    Starting ls")
    file_list = os.listdir()
    output = ''
    for file in file_list:
        if file != 'serv.py':
            output += "  "
            output += file
            output += '\n'
    client_socket.send(output.encode())
    print("    ls sent")
    
if __name__ == '__main__':
    main()