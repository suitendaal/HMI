# import matlab.engine as me
# from classes.hmiDrawer import HMIDrawer
#
#
# if __name__ == '__main__':
#     hmiDrawer = HMIDrawer()
#     hmiDrawer.draw()

from tkinter import *


root = Tk()

photo = PhotoImage(file='resources/platoontomtom_empty.png')
label = Canvas(root, image=photo)
label.pack()

root.mainloop()