from udp.calculations import *
from classes.vehicle_STsoftware import *


values = json.load(open('values/num.json'))['udp_data']
server_values = values['server']['dspace']


class DataManager(object):

    def __init__(self, udp_socket):
        self.udp_socket = udp_socket
        self.vehicles = None
        self.roads = None
        self.variables = None
        self.advisory_speed = -1
        self.gap = None

        self.error = False

    def start(self, data):
        old_vehicles = self.vehicles
        old_gap = self.gap

        self.vehicles, self.roads, self.variables = self.manageData(data)
        if self.vehicles is not None and len(self.vehicles) > 1 and self.vehicles[0].disToInter() < 500 and \
                self.vehicles[0].position.ypos < 6.5:
                t_min, t_max = calculateTimeToIntersection(self.vehicles)
                self.gap, self.advisory_speed = calculateAdvisorySpeed(self.vehicles, t_max)
                self.error = checkIfError(old_vehicles, self.vehicles, old_gap, self.gap)
        else:
            self.gap = None
            self.advisory_speed = -1
            self.error = False

    def manageData(self, data):
        # In matlab this function is called sort and vehicle convert

        vehicles = None
        roads = None
        variables = None

        main_vehicle_variables = values['vehicle_values']['main_variables']
        vehicle_amount = values['vehicle_values']['vehicle_amount']
        vehicle_variables = values['vehicle_values']['vehicle_variables']

        # TODO: If roads or other variables are added, more code is needed

        main_vehicle_data = data[0:main_vehicle_variables]
        other_vehicles_data = data[main_vehicle_variables:main_vehicle_variables + (vehicle_amount * vehicle_variables)]

        main_vehicle = self.getMainVehicle(main_vehicle_data)
        other_vehicles = self.getOtherVehicles(other_vehicles_data, vehicle_variables)
        vehicles = [main_vehicle]
        vehicles.extend(other_vehicles)

        return vehicles, roads, variables

    def getMainVehicle(self, data):
        partnr = int(data[0])
        vehicle_type = Type(data[1], data[2])
        position = Position(data[3] + 2 - data[2] / 2, data[4], data[5], data[6], data[7])
        dynamics = Dynamics(data[8], data[9], data[10])
        vehicle = MainVehicle(partnr, vehicle_type, position, dynamics)
        return vehicle

    def getOtherVehicles(self, data, number):
        vehicles = []
        for i in range(0, len(data), number):
            vehicle_data = data[i:i+number]
            partnr = data[0]
            vehicle_type = Type(vehicle_data[1], vehicle_data[2])
            position = Position(vehicle_data[3], vehicle_data[4], vehicle_data[5], vehicle_data[6], vehicle_data[7])
            dynamics = Dynamics(vehicle_data[8], vehicle_data[9])
            vehicle = Vehicle(partnr, vehicle_type, position, dynamics)
            vehicles.append(vehicle)
        return vehicles
