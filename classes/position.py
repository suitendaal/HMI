class Position:

    def __init__(self, pos_x, pos_y, direction):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = direction

    def getPosition(self):
        return [self.pos_x, self.pos_y]