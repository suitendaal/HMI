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

        # Set background label, tom-tom image.
        self.backGround = Label(self.baseFrame, bg=colors['transparent'])
        self.initializeBackground()

        # Set vehicle canvas.
        self.canvas = Canvas(self.baseFrame, bg=colors['transparent'], highlightthickness=0)
        self.initializeCanvas()

        self.speedsign = Label(self.canvas, bg=colors['background'], borderwidth=0)
        self.initializeSpeedsign()

        # Set Text
        self.text = Text(self.canvas, bg=colors['white'], borderwidth=0, highlightthickness=0, font=("Helvetica", 15), height=1, width=3)
        self.initializeText()

        self.vehicles = []

    def initializeText(self):
        self.text.place(relx=0.9, rely=0.15, anchor=CENTER)
        self.text.insert(END, " hoi ")

    def setText(self, text):
        self.text.delete(1.0, END)
        self.text.insert(END, text)
        self.update_idletasks()
        self.update()

    def initializeBase(self):
        # Venster eromheen weghalen
        self.overrideredirect(True)

        # Plaats op beeldscherm
        geometry = "+" + str(num["canvas"]["place_x"]) + "+" + str(num["canvas"]["place_y"])
        self.geometry(geometry)
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
        self.border = PhotoImage(file='resources/platoontomtom_empty.png')

        # zoom the image
        self.border = self.border.zoom(num["canvas"]["zoomlevel"][0])
        self.border = self.border.subsample(num["canvas"]["zoomlevel"][1])

        # Add image to label
        self.backGround.configure(image=self.border)

        # Pack label
        self.backGround.pack()

    def initializeSpeedsign(self):
        # Choose image
        self.speedsignimage = PhotoImage(file='resources/snelheidsbord.png')

        # zoom the image
        self.speedsignimage = self.speedsignimage.zoom(num["canvas"]["zoomlevel"][0])
        self.speedsignimage = self.speedsignimage.subsample(num["canvas"]["zoomlevel"][1])

        self.speedsign.configure(image=self.speedsignimage)

        self.speedsign.place(relx=0.9, rely=0.16, anchor=CENTER)

    def initializeCanvas(self):
        # Verplaats canvas naar rechts en naar beneden
        self.canvas.place(relx=440.5/882, rely=286/580, anchor=CENTER)
        self.canvas.config(width=self.border.width() * 0.705, height=self.border.height() * 0.625)

    def show(self):
        self.update_idletasks()
        self.update()

    def addVehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def addVehicles(self, vehicles):
        self.vehicles.extend(vehicles)

    def showError(self):
        pass

    def plotGap(self, distance):
        pass