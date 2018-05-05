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

        # Set right canvas.
        self.canvasright = Canvas(self.baseFrame, bg=colors['background'], highlightthickness=0)
        self.initializeCanvasRight()

        # Set left canvas.
        self.canvasleft = Canvas(self.baseFrame, bg=colors['transparent'], highlightthickness=0)
        self.initializeCanvasLeft()

        # place the target gap in the left canvas
        self.gaps = []
        # self.plotGap(0)

        # Place the speedsign
        self.speedsign = Label(self.baseFrame, bg=colors['background'], borderwidth=0)
        self.initializeSpeedsign()

        # Set Text
        self.text = Text(self.baseFrame, bg=colors['white'], borderwidth=0, highlightthickness=0, font=('Helvetica 16 bold'), height=1, width=4)
        self.initializeText()

        self.vehicles = []

    def initializeText(self):
        self.text.place(relx=num["canvas"]["place_x_sign"], rely=num["canvas"]["place_y_sign"], anchor=CENTER)
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
        geometry = "+" + str(num["canvas"]["place_x"]) + "+" + str(num["canvas"]["place_y"]) # -2500 en 700 voor grote tv
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

        self.speedsign.place(relx=num["canvas"]["place_x_sign"], rely=num["canvas"]["place_y_sign"], anchor=CENTER)

    def initializeCanvasRight(self):
        # Verplaats canvas naar rechts en naar beneden
        self.canvasright.place(relx=749/882, rely=286/580, anchor=E)
        self.canvasright.config(width=self.border.width() * 0.35, height=self.border.height() * 0.623)

    def initializeCanvasLeft(self):
        # Verplaats canvas naar rechts en naar beneden
        self.canvasleft.place(relx=134 / 882, rely=286 / 580, anchor=W)
        self.canvasleft.config(width=self.border.width() * 0.355, height=self.border.height() * 0.623)


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
        ycompensation = 30
        
        self.canvasleft.delete("all")
        self.update()
        if distance > self.canvasleft.winfo_height() / 2 - ycompensation:
            distance = self.canvasleft.winfo_height() / 2 - ycompensation
        elif distance < -self.canvasleft.winfo_height() / 2 - ycompensation:
            distance = -self.canvasleft.winfo_height() / 2 - ycompensation

        middle_x = self.canvasleft.winfo_width() / 2
        middle_y = self.canvasleft.winfo_height() / 2 - ycompensation - distance

        radius = 5

        x0 = middle_x - radius
        x1 = middle_x + radius
        y0 = middle_y - radius
        y1 = middle_y + radius

        self.gap = self.canvasleft.create_oval(x0, y0, x1, y1, fill=colors["truck"])
