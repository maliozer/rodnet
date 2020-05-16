import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog

def on_click():
    canvas.itemconfig(image_id, image=image2)


root = tk.Tk()

canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()


button = tk.Button(root, text="Change", command=on_click)
button.pack()


image1 = tk.PhotoImage(file="./images/inzva_logo.png")


image_id = canvas.create_image(0, 0, anchor='nw', image=image1)



filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("png files", "*.png"),("all files", "*.*")))
image2 = ImageTk.PhotoImage(Image.open(filename))


root.mainloop()