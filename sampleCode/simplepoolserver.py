import socket
import os
import multiprocessing


def send_message(s_socket, client_address):
    # Message to be sent to client
    message = 'Hi ' + client_address[0] + ':' + str(client_address[1]) + '. This is server ' + str(
        os.getpid())
    # Send message to client
    s_socket.sendto(str.encode(message), client_address)
    print('Sent to client: ', message)


if __name__ == "__main__":

    number_processes = 4
    # Initialise the pool
    pool = multiprocessing.Pool(number_processes)

    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Server application IP address and port
    server_address = '127.0.0.1'
    server_port = 10001

    # Buffer size
    buffer_size = 1024

    # Bind socket to port
    server_socket.bind((server_address, server_port))
    print('Server up and running at {}:{}'.format(server_address, server_port))

    while True:
        # Receive message from client
        data, address = server_socket.recvfrom(buffer_size)
        print('Received message \'{}\' at {}:{}'.format(data.decode(), address[0], address[1]))
        # Spawn a worker process asynchronously from the pool
        pool.apply_async(send_message, args=(server_socket, address,))
