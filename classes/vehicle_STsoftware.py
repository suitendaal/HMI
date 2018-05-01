

class Vehicle(object):

    def __init__(self, partnr, vehicletype, position, dynamics):
        self.partnr = partnr
        self.type = vehicletype
        self.position = position
        self.dynamics = dynamics

        self.time_to_inter = None
        self.time_to_inter_front = None
        self.time_to_inter_back = None

    def timeToInter(self):
        self.time_to_inter = self.dynamics.dis_to_inter / self.dynamics.velocity
        self.time_to_inter_front = (self.dynamics.dis_to_inter - self.type.carlength / 2) / self.dynamics.Velocity
        self.time_to_inter_back = (self.dynamics.dis_to_inter + self.type.carlength / 2) / self.dynamics.Velocity


class Type(object):

    def __init__(self, cartype, carlength):
        self.cartype = cartype
        self.carlength = carlength


class Position(object):

    def __init__(self, xpos, ypos, heading):
        self.xpos = xpos
        self.ypos = ypos
        self.heading = heading


class Dynamics(object):

    def __init__(self, velocity, dis_to_inter, lane, acc=None):
        self.velocity = velocity
        self.dis_to_inter = dis_to_inter
        self.lane = lane
        self.acc = acc


class MainVehicle(Vehicle):

    def __init__(self, partnr, vehicletype, position, dynamics):
        super(). __init__(partnr, vehicletype, position, dynamics)
        self.min_speed = 70 / 3.6
        self.max_acc = 5 / 3.6



