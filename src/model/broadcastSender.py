import socket
import ipaddress


def broadcast(ip, port, broadcast_message):
    # Create a UDP socket
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Send message on broadcast address
    broadcast_socket.sendto(str.encode(broadcast_message), (ip, port))
    broadcast_socket.close()


if __name__ == '__main__':
    SUBNETMASK = "255.255.255.0"
    BROADCAST_PORT = 61425
    IP_ADRESS_OF_THIS_PC = socket.gethostbyname(socket.gethostname())
    net = ipaddress.IPv4Network(IP_ADRESS_OF_THIS_PC + '/' + SUBNETMASK, False)
    BROADCAST_IP = net.broadcast_address.exploded

    # Send broadcast message
    message = IP_ADRESS_OF_THIS_PC + ' sent a broadcast'
    broadcast(BROADCAST_IP, BROADCAST_PORT, message)
