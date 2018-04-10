from tkinter import *


class HMIDrawer(Tk):

    def __init__(self):
        super().__init__()
        self.image = PhotoImage(file='resources/platoontomtom_empty1.png')
        self.label = Label(self, image=self.image, bg='white')
        self.vehicles = []

        self.initialize()

    def initialize(self):
        self.overrideredirect(True)
        self.geometry("+250+250")
        self.lift()
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-disabled", True)
        self.wm_attributes("-transparentcolor", "white")
        self.label.pack()

    def show(self):
        self.label.mainloop()

    def addVehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def addVehicles(self, vehicles):
        self.vehicles.extend(vehicles)