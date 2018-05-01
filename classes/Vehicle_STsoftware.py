

class Vehicle(object):

    def __init__(self, partnr, type, position, dynamics):
        self.partnr = partnr
        self.type = type
        self.position = position
        self.dynamics = dynamics


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

    def __init__(self, velocity, distointer, lane, acc=None):
        self.velocity = velocity
        self.distointer = distointer
        self.lane = lane
        self.acc = acc


class MainVehicle(Vehicle):

    def __init__(self, partnr, type, position, dynamics):
        super(). __init__(partnr, type, position, dynamics)
        self.min_speed = 70 / 3.6
        self.max_acc = 5 / 3.6



