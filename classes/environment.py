class Environment(object):

    def __init__(self, color):
        self.color = color

    def drawing(self, canvas, coord):
        return canvas.create_polygon(coord, fill=self.color)