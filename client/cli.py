import socket
import sys
import time

def main():

    if len(sys.argv) != 3:
        print("Incorrect number of arguments")
        return
    
    SERVER_IP = sys.argv[1]
    PORT_NUM = sys.argv[2]
    PORT_NUM = int(PORT_NUM)

    # Establish connection with server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT_NUM))

    client_input = ""

    # Client Loop
    while True:
        client_input = input("ftp>")
        client_socket.send(client_input.encode())

        command = client_input.split()
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

    print("  Goodbye")
    client_socket.close()
    return

def get(client_socket, file_name:str):
    print("  Getting " + file_name)
    file = open(file_name, "wb")
    while True:
        msg = client_socket.recv(1024)
        file.write(msg)
        if len(msg) < 1024:
            break
    file.close()
    
def put(client_socket, file_name:str):
    print("  Sending:" + file_name)
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