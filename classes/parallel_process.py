import multiprocessing
multiprocessing.set_start_method('spawn')
from multiprocessing import Process
from udp.datamanager import *


class ParallelProcess(object):
    def __init__(self, hmi):
        self.repeat = True

        self.hmi = hmi
        self.hmi.show()
        self.socket = UDPSocket((servervalues['ip_address'], servervalues['port']))
        self.datamanager = DataManager(self.socket)

    def start(self):
        self.getData()
        #Process(target=self.getData).start()
        #Process(target=self.manageData).start()

    def getData(self):
        while self.repeat:
            data = self.socket.get_data()
            #data = self.socket.data
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
        self.hmi.setText(str(int(advisory_speed)))
