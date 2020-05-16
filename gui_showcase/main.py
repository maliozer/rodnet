from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

gui = Tk()

gui.title('RODNET | Inzva AI Project Showcase v0.1')

#logo var en son ekleriz yorumda kalabilir
logo_image_path = Image.open('./images/inzva_logo.png')
inzva_logo = ImageTk.PhotoImage(logo_image_path)
inzva_logo_label = Label(image=inzva_logo).pack()

#window size
gui.geometry("800x600")

#title
rodnet_label = Label(gui, text="RODNET Robust Object Detection Beta Showcase: ",font=("Helvetica", 12)).pack()

def open():
    global predicted_image
    gui.filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("png files", "*.png"),("all files", "*.*")))
    
    if(gui.filename):
        print(gui.filename) #image path on local pc
        #call predictor with (gui.filename)

        #get predicted photo file path show as below
        #image_path = Image.open(prediction(gui.filename))

        image_path = Image.open(gui.filename)
        predicted_image = ImageTk.PhotoImage(image_path)
        my_image_label = Label(image=predicted_image).pack()
    else:
        print("No selection")

open_label = Label(gui, text="Select the image: ").pack()
open_button = Button(gui, text="Open File", command=open).pack()

gui.mainloop()