from udp.datamanager import *
from udp.udpsocket import *
import time
import numpy as np


class SpeedProgram(object):
    def __init__(self, hmi, level):
        self.repeat = True

        self.hmi = hmi
        self.hmi.show()
        self.gap = None
        self.advisory_speeds = []

        self.level = level

        self.socket = UDPSocket((server_values['ip_address'], server_values['port']))
        self.datamanager = DataManager(self.socket)

    def start(self):
        self.getData()

    def getData(self):
        start_time = int(time.time() * 1000)
        while self.repeat:
            data = self.socket.get_data()
            current_time = int(time.time() * 1000)
            difference_time = current_time - start_time
            if data is not None and difference_time > 2000:
                start_time = int(time.time() * 1000)

                self.datamanager.start(data)

                # Plot advisory speed.
                advisory_speed = self.datamanager.advisory_speed
                if advisory_speed < 0:
                    advisory_speed = 80
                    self.showInHMI(advisory_speed)
                    self.advisory_speeds = []
                else:
                    self.advisory_speeds.append(advisory_speed)
                    if len(self.advisory_speeds) > 3:
                        self.advisory_speeds.pop(0)
                    self.showInHMI(int(np.mean(self.advisory_speeds)))

                # Plot gap.
                distances = json.load(open('values/num.json'))['udp_data']['road_data']

                if self.datamanager.gap is not None and distances['xpos_start_merginglane'] < self.datamanager.vehicles[
                    0].position.xpos < distances['xpos_end_merginglane']:
                    if self.datamanager.vehicles is not None and len(self.datamanager.vehicles) > 0 and self.datamanager.gap is not None:
                        main_vehicle = self.datamanager.vehicles[0]
                        gap = self.datamanager.gap
                        gap.rel_distance = gap.xpos() - main_vehicle.position.xpos
                        # self.plotGap(gap)

                        # Show if you are next to gap.
                        if abs(gap.rel_distance) < 8:
                            self.mergeCommand()
                        else:
                            self.hideMergeCommand()

                    # Show error.
                if self.level == 4 and self.datamanager.error:
                    self.showError()

    def showInHMI(self, advisory_speed):
        self.hmi.setText(str(advisory_speed))

    def mergeCommand(self):
        self.hmi.showMergingCommand()

    def hideMergeCommand(self):
        self.hmi.hideMergingCommand()

    def showError(self):
        print("error")
        self.hmi.showError()

    def plotGap(self, gap):
        self.hmi.plotGap(gap.rel_distance)
