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

                # Plot advisory speed.
                advisory_speed = self.datamanager.advisory_speed
                if advisory_speed < 0:
                    advisory_speed = 80
                self.showInHMI(advisory_speed)

                # Plot gap.
                distances = json.load(open('values/num.json'))['udp_data']['road_data']
                # print("[ time to inter" + str(gap.time_to_inter) + ", " + str(self.datamanager.vehicles[0].position.xpos) + ", " + str(distances['xpos_end_merginglane']))

                if self.datamanager.gap is not None and distances['xpos_start_merginglane'] < self.datamanager.vehicles[
                    0].position.xpos < distances['xpos_end_merginglane']:
                    print("update")
                    gap = Gap(0)
                    gap.rel_distance = 0
                    self.plotGap(gap)
                #     self.plotGap(self.datamanager.gap)

                # Show error.
                if self.level == 4 and self.datamanager.error:
                    self.showError()

    def showInHMI(self, advisory_speed):
        self.hmi.setText(str(advisory_speed))

    def showError(self):
        print("error")
        # self.hmi.showError()

    def plotGap(self, gap):
        self.hmi.plotGap(gap.xpos())
