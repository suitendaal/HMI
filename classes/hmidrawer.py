from tkinter import *
import json
import time
import os


root = os.getcwd()
colors = json.load(open(root + '\\values\\colors.json'))
num = json.load(open(root + '\\values\\num.json'))


class HMIDrawer(Tk):

    def __init__(self, level):
        super().__init__()

        # Set base frame.
        self.baseFrame = Frame(self)
        self.initializeBase()

        # Set background label, tom-tom image.
        self.backGround = Label(self.baseFrame, bg=colors['transparent'])
        self.initializeBackground()

        # Set right canvas.
        if level == 1:
            self.canvasright = Canvas(self.baseFrame, bg=colors['black'], highlightthickness=0)
        else:
            self.canvasright = Canvas(self.baseFrame, bg=colors['background'], highlightthickness=0)
        self.initializeCanvasRight(level)

        self.speedsign2 = Label(self.baseFrame, bg=colors['black'], fg=colors['white'], borderwidth=0)
        self.initializeSpeedsign2()

        self.speed = Text(self.baseFrame, bg=colors['white'], borderwidth=0, highlightthickness=0,
                          font=('Helvetica 16 bold'), height=1, width=3)
        self.initializeSpeed()

        if level == 1:
            return

        # Set left canvas.
        self.canvasleft = Canvas(self.baseFrame, bg=colors['transparent'], highlightthickness=0)
        self.initializeCanvasLeft()

        if level > 2:

            # Place the speedsign
            self.speedsign = Label(self.baseFrame, bg=colors['background'], borderwidth=0)
            self.initializeSpeedsign()

            # Set Text
            self.text = Text(self.baseFrame, bg=colors['white'], borderwidth=0, highlightthickness=0, font=('Helvetica 16 bold'), height=1, width=3)
            self.initializeText()

            self.vehicles = []

            self.mergingsign = Label(self.baseFrame, bg=colors['background'], borderwidth=0)
            self.initializeMergingSign()

            self.initializeError()
            self.startErrorTime = int(round(time.time() * 1000))

    def initializeText(self):
        self.text.place(relx=num["canvas"]["place_x_sign"]+0.01, rely=num["canvas"]["place_y_sign"], anchor=CENTER)
        standard_text = str(num['udp_data']['advisory_speed_variables']['advisory_speed'])
        self.text.insert(END, standard_text, "center")

    def initializeSpeed(self):
        self.speed.place(relx=num["canvas"]["place_x_speed"], rely=num["canvas"]["place_y_speed"], anchor=CENTER)
        standard_text = str(num['udp_data']['advisory_speed_variables']['advisory_speed'])
        self.speed.insert(END, standard_text, "center")

    def setText(self, text):
        self.text.delete(1.0, END)
        self.text.insert(END, text, "center")
        self.update()

    def show_speed(self, speed):
        self.speed.delete(1.0, END)
        self.speed.insert(END, speed, "center")
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

    def initializeSpeedsign2(self):
        # 2e image
        self.speedsignimage2 = PhotoImage(file='resources/speedo1.png')
        self.speedsignimage2 = self.speedsignimage2.zoom(1).subsample(3)
        # zoom the image
        self.speedsignimage2 = self.speedsignimage2.zoom(num["canvas"]["zoomlevel"][0]).subsample(
            num["canvas"]["zoomlevel"][1])
        self.speedsign2.configure(image=self.speedsignimage2)
        self.speedsign2.place(relx=num["canvas"]["place_x_mergingsign"], rely=num["canvas"]["place_y_sign"],
                              anchor=CENTER)

    def initializeCanvasRight(self, level):
        if level == 1:
            self.canvasright.place(relx=1/2, rely=286/580, anchor=CENTER)
            self.canvasright.config(width=self.border.width() * 0.723, height=self.border.height() * 0.623)
        else:
            # Verplaats canvas naar rechts en naar beneden
            self.canvasright.place(relx=749/882, rely=286/580, anchor=E)
            self.canvasright.config(width=self.border.width() * 0.35, height=self.border.height() * 0.623)

    def initializeCanvasLeft(self):
        # Verplaats canvas naar rechts en naar beneden
        self.canvasleft.place(relx=134 / 882, rely=286 / 580, anchor=W)
        self.canvasleft.config(width=self.border.width() * 0.355, height=self.border.height() * 0.623)

    def initializeError(self):
        self.errorimage = PhotoImage(file='resources/waarschuwingsbord.png')

        self.errorimage = self.errorimage.zoom(1)
        self.errorimage = self.errorimage.subsample(6)

        # zoom the image
        self.errorimage = self.errorimage.zoom(num["canvas"]["zoomlevel"][0])
        self.errorimage = self.errorimage.subsample(num["canvas"]["zoomlevel"][1])

        self.error = Label(self.baseFrame, bg=colors['background'], borderwidth=0)

        self.error.place(relx=num["canvas"]["place_x_error"], rely=num["canvas"]["place_y_error"], anchor=CENTER)

    def show(self):
        self.update()

    def addVehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def addVehicles(self, vehicles):
        self.vehicles.extend(vehicles)

    def hideGap(self):
        self.canvasleft.delete("all")
        self.update()

    def plotGap(self, distance, color):
        ycompensation = 30

        self.hideGap()

        distance = distance * 1.3

        if distance > self.canvasleft.winfo_height() / 2 - ycompensation:
            distance = self.canvasleft.winfo_height() / 2 - ycompensation
        elif distance < -self.canvasleft.winfo_height() / 2 - ycompensation:
            distance = -self.canvasleft.winfo_height() / 2 - ycompensation

        middle_x = self.canvasleft.winfo_width() / 2 - 33
        middle_y = self.canvasleft.winfo_height() / 2 - ycompensation - int(distance)

        width = 14
        length = 50

        x0 = middle_x - width / 2
        x1 = middle_x + width / 2
        y0 = middle_y - length / 2
        y1 = middle_y + length / 2

        self.gap = self.canvasleft.create_rectangle(x0, y0, x1, y1, fill=color)

    def initializeMergingSign(self):
        self.mergingImage = PhotoImage(file='resources/invoegbord.png')

        self.mergingImage = self.mergingImage.zoom(1)
        self.mergingImage = self.mergingImage.subsample(6)

        self.mergingsign.place(relx=num["canvas"]["place_x_mergingsign"], rely=num["canvas"]["place_y_mergingsign"],
                               anchor=CENTER)

    def showMergingCommand(self):
        self.mergingsign.configure(image=self.mergingImage)
        self.update()

    def hideMergingCommand(self):
        self.mergingsign.configure(image="")
        self.update()

    def showError(self):
        self.startErrorTime = int(round(time.time() * 1000))
        self.error.configure(image=self.errorimage)
        self.update()

    def hideError(self):
        current_time = int(round(time.time() * 1000))
        duration = current_time - self.startErrorTime
        max_error_duration = num['udp_data']['hmi_variables']['errorduration']
        if duration >= max_error_duration:
            self.error.configure(image="")
            self.update()

    def update(self):
        super().update_idletasks()
        super().update()
