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

        # Set Text
        self.text = Text(self.canvas, bg=colors['background'], borderwidth=0, highlightthickness=0, font=("Helvetica", 80), height=1, width=3)
        self.initializeText()

        self.vehicles = []

    def initializeText(self):
        self.text.place(relx=0.75, rely=0.5, anchor=CENTER)
        self.text.insert(END, " hoi ")

    def setText(self, text):
        self.text.delete(1.0, END)
        self.text.insert(END, text)
        self.update_idletasks()
        self.update()

    def initializeBase(self):
        # Venster eromheen
        # self.overrideredirect(True)

        # Plaats op beeldscherm
        self.geometry("-4100+750")
        self.lift()

        # Altijd vooraan
        self.wm_attributes("-topmost", True)

        # Kan verplaatsen
        # self.wm_attributes("-disabled", True)

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
        self.canvas.place(x=-1, y=-4, relx=0.5, rely=0.5, anchor=CENTER)

    def show(self):
        self.update_idletasks()
        self.update()

    def addVehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def addVehicles(self, vehicles):
        self.vehicles.extend(vehicles)