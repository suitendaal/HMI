import socket
import struct

class UDPSocket(socket.socket):

    def __init__(self, server_adress):
        super().__init__(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_adress = 