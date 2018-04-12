from tkinter import *
import json


colors = json.load(open('values/colors.json'))
num = json.load(open('values/num.json'))

class HMIDrawer(Tk):

    def __init__(self):
        super().__init__()

        # Set base frame.
        self.baseFrame = Frame(self)
        self.initializeBase()

        # Set background label.
        self.backGround = Label(self.baseFrame, bg=colors['transparent'])
        self.initializeBackground()

        # Set vehicle canvas.
        self.canvas = Canvas(self.baseFrame, bg=colors['background'], highlightthickness=0,
                             width=num['canvas']['width'], height=num['canvas']['height'])
        self.initializeCanvas()
        self.vehicles = []



    def initializeBase(self):
        # Venster eromheen
        self.overrideredirect(True)

        # Plaats op beeldscherm
        self.geometry("+250+250")
        self.lift()

        # Altijd vooraan
        self.wm_attributes("-topmost", True)

        # Kan verplaatsen
        self.wm_attributes("-disabled", True)

        # Doorszichtig
        self.wm_attributes("-transparentcolor", colors['transparent'])

        # Pack base frame.
        self.baseFrame.pack()

    def initializeBackground(self):
        # Choose image
        self.image = PhotoImage(file='resources/platoontomtom_empty.png')

        # Add image to label
        self.backGround.configure(image=self.image)

        # Pack label
        self.backGround.pack()

    def initializeCanvas(self):
        # Verplaats canvas naar rechts en naar beneden
        self.canvas.place(x=num['canvas']['place_x'], y=num['canvas']['place_y'])


    def show(self):
        self.mainloop()

    def addVehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def addVehicles(self, vehicles):
        self.vehicles.extend(vehicles)