from udp.datamanager import *
from udp.udpsocket import *


class SpeedProgram(object):
    def __init__(self, hmi, level):
        self.repeat = True

        self.hmi = hmi
        self.hmi.show()

        self.level = level

        self.socket = UDPSocket((servervalues['ip_address'], servervalues['port']))
        self.datamanager = DataManager(self.socket)

    def start(self):
        self.getData()

    def getData(self):
        while self.repeat:
            data = self.socket.get_data()
            # data = self.socket.data
            if data is not None:
                self.datamanager.start(data)
                self.showInHMI(self.datamanager.advisory_speed)

    def manageData(self):
        while self.repeat:
            data = self.socket.data
            if data is not None:
                self.datamanager.start(data)
                self.showInHMI(self.datamanager.advisory_speed)

    def showInHMI(self, advisory_speed):
        self.hmi.setText(str(advisory_speed))
