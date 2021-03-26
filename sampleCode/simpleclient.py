import socket

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server application IP address and port
server_address = '127.0.0.1'
server_port = 10001

# Buffer size
buffer_size = 1024

# Message sent to server
message = 'Hi server!'

try:
    # Send data to server
    client_socket.sendto(message.encode(), (server_address, server_port))
    print('Sent to server: ', message)

    # Receive response from server
    print('Waiting for response...')
    data, server = client_socket.recvfrom(buffer_size)
    print('Received message from server: ', data.decode())

finally:
    client_socket.close()
    print('Socket closed')
