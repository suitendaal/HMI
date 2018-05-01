import json
from udp.udpsocket import UDPSocket
from udp.calculations import *


values = json.load(open('values/num.json'))
servervalues = values['server']['dspace']


class DataManager(object):

    def __init__(self):
        self.udp_socket = UDPSocket((servervalues['ip_address'], servervalues['port']))
        self.advisory_speed = None

    def start(self):
        repeat = True

        while repeat:
            data = self.udp_socket.get_data()
            vehicles, roads, variables = self.manageData(data)
            t_min, t_max = calculateTimeToIntersection(vehicles)
            self.advisory_speed = calculateAdvisorySpeed(vehicles, t_max)


    def manageData(self, data):
        # In matlab this function is called sort and vehicle convert

        vehicles = None
        roads = None
        variables = None

        # TODO: put data in classes

        return vehicles, roads, variables
