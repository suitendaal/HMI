from tkinter import *


class HMIDrawer(Tk):

    def __init__(self):
        super().__init__()
        self.baseFrame = Frame(self)

        self.image = PhotoImage(file='resources/platoontomtom_empty1.png')
        self.label = Label(self.baseFrame, image=self.image, bg='white')
        self.vehicles = []

        self.initialize()

    def initialize(self):
        # Venster eromheen
        # self.overrideredirect(True)

        # Plaats op beeldscherm
        self.geometry("+250+250")
        self.lift()

        # Altijd vooraan
        self.wm_attributes("-topmost", True)

        # Kan verplaatsen
        # self.wm_attributes("-disabled", True)

        # Doorszichtig
        self.wm_attributes("-transparentcolor", "white")

        # Laat label zien in tk
        self.label.pack()

        self.baseFrame.pack()

    def show(self):
        self.mainloop()

    def addVehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def addVehicles(self, vehicles):
        self.vehicles.extend(vehicles)