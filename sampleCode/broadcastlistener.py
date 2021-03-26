import socket


if __name__ == '__main__':
    # Listening port
    BROADCAST_PORT = 61425

    # Local host information
    MY_HOST = socket.gethostname() # Name of my PC
    MY_IP = socket.gethostbyname(MY_HOST)

    # Create a UDP socket
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set the socket to broadcast and enable reusing addresses
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind socket to address and port
    listen_socket.bind((MY_IP, BROADCAST_PORT))

    print("Listening to broadcast messages")

    while True:
        data, addr = listen_socket.recvfrom(1024)
        if data:
            print("Received broadcast message:", data.decode())
