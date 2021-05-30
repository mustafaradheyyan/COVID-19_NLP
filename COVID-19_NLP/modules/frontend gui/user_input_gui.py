from tkinter import *

def Close():
    Window.destroy()

def handle_click(event):
    print("The button was clicked!")

    button = Button(text="Click me!")

    button.bind("<Button-1>", handle_click)

class Window():
    def __init__(self):
        self.window = Tk()
        self.window.geometry("200x100")

        submit_button = Button(self.window, text = "Submit", command = self.Close)
        submit_button.pack(pady = 20)

        self.window.mainloop()

    def Close(self):
        self.window.destroy()

def create_user_input_gui():
    border_effects = {
    "flat": FLAT,
    "sunken": SUNKEN,
    "raised": RAISED,
    "groove": GROOVE,
    "ridge": RIDGE,}

    Window = Tk()

    frame1 = Frame(master=window, width=200, height=100, bg="red")
    frame1.pack(fill=BOTH, side=LEFT, expand=True)

    frame2 = Frame(master=window, width=100, bg="yellow")
    frame2.pack(fill=BOTH, side=LEFT, expand=True)

    frame3 = Frame(master=window, width=50, bg="blue")
    frame3.pack(fill=BOTH, side=LEFT, expand=True)

    #window.mainloop()

    for relief_name, relief in border_effects.items():
        frame = Frame(master=window, relief=relief, borderwidth=5)
        frame.pack(side=LEFT)
        label = Label(master=frame, text=relief_name)
        label.pack()

    #window.mainloop()

    window = Tk()
    greeting = Label(
    text="Hello, Tkinter",
    fg="white",
    bg="black",
    width=10,
    height=10
)
    button = Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)
        

    entry1 = Entry(fg="yellow", bg="blue", width=50)
    entry2 = Entry(fg="yellow", bg="green", width=50)
    entry3 = Entry(fg="black", bg="yellow", width=50)
    entry4 = Entry(fg="yellow", bg="brown", width=50)
    entry5 = Entry(fg="yellow", bg="gray", width=50)

    entry1.pack()
    entry2.pack()
    entry3.pack()
    entry4.pack()
    entry5.pack()

    button.pack()
    greeting.pack()
    window.mainloop()

    start_date,  = entry1.get()
    end_date = entry2.get()
    search_term = entry3.get()
    number_of_pubs_per_month = entry4.get()
    number_of_tweets_per_month = entry5.get()

