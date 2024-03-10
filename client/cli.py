import socket
import sys
import time

def main():
    # chekc if proper arguments are there
    if len(sys.argv) != 3:
        print("Incorrect number of arguments")
        return
    # gather arguments and convert type if necessary
    SERVER_IP = sys.argv[1]
    PORT_NUM = sys.argv[2]
    PORT_NUM = int(PORT_NUM)

    # Establish connection with server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT_NUM))

    client_input = ""

    # Client Loop
    while True:
        # gather user input
        client_input = input("ftp>")
        # send input to server
        client_socket.send(client_input.encode())
        # split command into tokens
        command = client_input.split()
        # execute proper case based off of input
        if command[0] == "get":
            if len(command) == 1:
                print("Missing file name")
                continue
            get(client_socket=client_socket, file_name=command[1])
        elif command[0] == "put":
            if len(command) == 1:
                print("Missing file name")
                continue
            put(client_socket=client_socket, file_name=command[1])
        elif command[0] == "ls":
            msg = client_socket.recv(1024)
            print(msg.decode(), end="")
        elif client_input == 'quit':
            break
    # close connection
    print("  Goodbye")
    client_socket.close()
    return

# get
def get(client_socket, file_name:str):
    print("  Getting " + file_name)
    # open file
    file = open(file_name, "wb")
    # recieve data from server
    while True:
        msg = client_socket.recv(1024)
        file.write(msg)
        # if message is less than 1024 bytes, 
        if len(msg) < 1024:
            break
    file.close()
# put    
def put(client_socket, file_name:str):
    print("  Sending:" + file_name)
    # 
    file = open(file_name, 'rb')
    while True:
        buf = file.read(1024)
        time.sleep(0.05)
        # print("    sending packet")
        client_socket.send(buf)
        # print("    Packet sent")
        if len(buf) < 1024:
            break
    file.close()

    

if __name__ == '__main__':
    main()