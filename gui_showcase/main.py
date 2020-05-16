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
canvas = Canvas(gui, width=800, height=500)
canvas.pack()

#title
rodnet_label = Label(gui, text="RODNET Robust Object Detection Beta Showcase: ",font=("Helvetica", 12)).pack()

def change(image_new):
    canvas.itemconfig(image_id, image=image_new)
    

def open():
    global predicted_image
    gui.filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("png files", "*.png"),("all files", "*.*")))
    
    if(gui.filename):
        global image2
        print(gui.filename) #image path on local pc
        #call predictor with (gui.filename)
        image2_open = Image.open(gui.filename)
        w = int(image2_open.width * 0.5)
        h = int(image2_open.height * 0.5)
        print(w,h)
        image2_open = image2_open.resize((w,h), Image.ANTIALIAS)

        image2 = ImageTk.PhotoImage(image2_open)
        
        #update canvas
        change(image2)

    else:
        print("No selection")


image_showcase = PhotoImage(file="./images/rodnet_logo.png")
image_id = canvas.create_image(0, 0, anchor='nw', image=image_showcase)


open_label = Label(gui, text="Select the image: ").pack()
open_button = Button(gui, text="Open File", command=open).pack()

gui.mainloop()