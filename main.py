from tkinter import *


root = Tk()

photo = PhotoImage(file='resources/platoontomtom_empty.png')
label = Label(root, image=photo)
label.pack()

root.mainloop()
