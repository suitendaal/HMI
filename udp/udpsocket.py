import socket
import struct


class UDPSocket(socket.socket):

    def __init__(self, server_address):
        super().__init__(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind(server_address)
        self.data = None

    def get_data(self):
        (data, addr) = self.recvfrom(1024)
        values = []
        for i in range(0, len(data), 4):
            # Float is 4 bytes.
            values.append(struct.unpack('>f', data[i:i+4])[0])
        self.data = values
        return values
