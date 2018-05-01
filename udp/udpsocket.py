import socket
import struct


class UDPSocket(socket.socket):

    def __init__(self, server_address):
        super().__init__(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind(server_address)
        self.data = None

    def get_data(self):
        (data, addr) = self.recvfrom(1024)
        data = struct.unpack('d', data)
        self.data = data
        return data
