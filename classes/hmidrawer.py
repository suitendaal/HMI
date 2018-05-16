from tkinter import *
import winsound
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
        self.text = Text(self.baseFrame, bg=colors['white'], borderwidth=0, highlightthickness=0, font=('Helvetica 16 bold'), height=1, width=3)
        self.initializeText()

        self.vehicles = []

        self.mergingsign = Label(self.baseFrame, bg=colors['background'], borderwidth=0)
        self.initializeMergingSign()

    def initializeText(self):
        self.text.place(relx=num["canvas"]["place_x_sign"]+0.01, rely=num["canvas"]["place_y_sign"], anchor=CENTER)
        standard_text = str(num['udp_data']['advisory_speed_variables']['advisory_speed'])
        self.text.insert(END, standard_text, "center")

    def setText(self, text):
        self.text.delete(1.0, END)
        self.text.insert(END, text, "center")
        self.update_idletasks()
        self.update()

    def initializeBase(self):
        # Venster eromheen weghalen
        self.overrideredirect(True)

        # Plaats op beeldscherm
        geometry = "+" + str(num["canvas"]["place_x"]) + "+" + str(num["canvas"]["place_y"]) # -2500 en 700 voor grote tv
        # geometry = "+" + str(400) + "+" + str(200)
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

        self.speedsignimage = self.speedsignimage.zoom(1)
        self.speedsignimage = self.speedsignimage.subsample(3)

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

    def hideGap(self):
        self.canvasleft.delete("all")
        self.update()

    def plotGap(self, distance):
        ycompensation = 30

        self.hideGap()

        distance = distance*1
        # TODO maak deze shit bois

        if distance > self.canvasleft.winfo_height() / 2 - ycompensation:
            distance = self.canvasleft.winfo_height() / 2 - ycompensation
        elif distance < -self.canvasleft.winfo_height() / 2 - ycompensation:
            distance = -self.canvasleft.winfo_height() / 2 - ycompensation

        middle_x = self.canvasleft.winfo_width() / 2 - 25
        middle_y = self.canvasleft.winfo_height() / 2 - ycompensation - distance

        radius = 5

        x0 = middle_x - radius
        x1 = middle_x + radius
        y0 = middle_y - radius
        y1 = middle_y + radius

        self.gap = self.canvasleft.create_oval(x0, y0, x1, y1, fill=colors["truck"])
        # self.gap = self.canvasleft.create_oval(20, 20, 40, 40, fill=colors["truck"])

    def initializeMergingSign(self):
        self.mergingImage = PhotoImage(file='resources/invoegbord.png')

        self.mergingImage = self.mergingImage.zoom(1)
        self.mergingImage = self.mergingImage.subsample(6)

        self.mergingsign.place(relx=num["canvas"]["place_x_mergingsign"], rely=num["canvas"]["place_y_mergingsign"],
                               anchor=CENTER)

    def showMergingCommand(self):
        self.mergingsign.configure(image=self.mergingImage)
        self.update_idletasks()
        self.update()

    def hideMergingCommand(self):
        self.mergingsign.configure(image="")
        self.update_idletasks()
        self.update()

    def showError(self):
        winsound.Beep(2000, 1000)

        self.errorimage = PhotoImage(file='resources/waarschuwingsbord.png')

        self.errorimage = self.errorimage.zoom(1)
        self.errorimage = self.errorimage.subsample(6)

        # zoom the image
        self.errorimage = self.errorimage.zoom(num["canvas"]["zoomlevel"][0])
        self.errorimage = self.errorimage.subsample(num["canvas"]["zoomlevel"][1])

        self.error.configure(image=self.errorimage)

        self.error.place(relx=num["canvas"]["place_x_error"], rely=num["canvas"]["place_y_error"], anchor=CENTER)
        self.error = Label(self.baseFrame, bg=colors['background'], borderwidth=0)

