import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

import car

class UI:
    def __init__(self, db, staffdb):
        self.staff_logged_in = False

        self.r = tk.Tk()
        self.r.title("Parking garage")

        self.dbref = db
        self.staffdbref = staffdb

        self.left = tk.Frame(self.r)
        self.r_up = tk.Frame(self.r)
        self.r_down = tk.Frame(self.r)

        # car status list
        self.lchoices = tk.StringVar(value=[])
        self.l = tk.Listbox(self.left, listvariable=self.lchoices, height=20, width=25,state='disabled')

        # parking place status window

        # user actions tabs
        self.tabs = ttk.Notebook(self.r_down)
        self.tabs.bind("<<NotebookTabChanged>>", lambda _: self.update())

        self.tab_man = ttk.Frame(self.tabs)
        self.tab_u = ttk.Frame(self.tabs)

        # user action buttons
        self.enter = tk.Button(self.tab_u, text="ENTER", command=self.create_enter_window)
        self.pay = tk.Button(self.tab_u, text="PAY", command=self.create_pay_window)
        self.exit = tk.Button(self.tab_u, text="EXIT CAR", command=self.create_exit_window)

        # management action buttons
        self.login = tk.Button(self.tab_man, text="LOGIN", command=self.create_login_window)
        self.remove = tk.Button(self.tab_man, text="REMOVE CAR", command=self.create_remove_window)

        # parking display
        self.spaces = []
        self.space_labels = []
        self.images = []
        self.invalid_images = []
        self.empty = []

        for i in range(0,self.dbref.spaces):
            f = tk.Frame(self.r_up)

            self.space_labels.append(tk.Label(f, text=i, compound='top'))

            self.images.append(tk.PhotoImage(file='./images/car.png'))
            self.invalid_images.append(tk.PhotoImage(file='./images/car_invalid.png'))
            self.empty.append(tk.PhotoImage(file='./images/empty.png'))

            self.space_labels[len(self.space_labels) - 1]['image'] = self.empty[len(self.empty) - 1]
            self.space_labels[len(self.space_labels) - 1].pack()

            self.spaces.append(f)



    def initialize(self):
        self.r.grid_columnconfigure(0,weight=1)
        self.r.grid_rowconfigure(0,weight=1)
        self.r.grid_columnconfigure(1,weight=1)
        self.r.grid_rowconfigure(1,weight=1)

        self.left.grid(column=0,row=0,rowspan=2,columnspan=1,sticky='nesw')
        self.r_up.grid(column=1,row=0,columnspan=1,rowspan=1,sticky='nesw')
        self.r_down.grid(column=1,row=1,columnspan=1,rowspan=1,sticky='nesw')

        self.l.pack(fill='both',expand=True)

        self.tabs.add(self.tab_u,text="Customers")
        self.tabs.add(self.tab_man,text="Management staff")
        self.tabs.pack(expand=1,fill="both")

        self.tab_u.grid_rowconfigure(0,weight=1)
        self.tab_u.grid_columnconfigure(0,weight=1)
        self.tab_u.grid_columnconfigure(1,weight=1)
        self.tab_u.grid_columnconfigure(2,weight=1)

        self.tab_man.grid_rowconfigure(0,weight=1)
        self.tab_man.grid_columnconfigure(0,weight=1)
        self.tab_man.grid_columnconfigure(1,weight=1)

        self.enter.grid(column=0,row=0,sticky='nesw',padx=5, pady=5)
        self.pay.grid(column=1,row=0,sticky='nesw',padx=5, pady=5)
        self.exit.grid(column=2,row=0,sticky='nesw',padx=5, pady=5)

        self.login.grid(column=0,row=0,sticky='nesw',padx=5, pady=5)
        self.remove.grid(column=1,row=0,sticky='nesw',padx=5, pady=5)

        for i,f in enumerate(self.spaces):
            if i < 5:
                self.r_up.columnconfigure(int(i),weight=1)
            self.r_up.rowconfigure(int(i/5),weight=1)
            f.grid(column=int(i%5),row=int(i/5),columnspan=1,rowspan=1,sticky='nesw',padx=5, pady=5)

        self.r.mainloop()

    # Create subwindow
    def create_window(self):
        w = tk.Toplevel(self.r)
        w.minsize(200,250)
        w.transient(self.r)

        ws = self.r.winfo_screenwidth() # width of the screen
        hs = self.r.winfo_screenheight() # height of the screen
        x = (ws/2) - (200/2)
        y = (hs/2) - (150/2)

        w.geometry('%dx%d+%d+%d' % (200, 150, x, y))
        return w


    # ENTER functions
    def create_enter_window(self):
        self.enter_window = self.create_window()

        label = ttk.Label(self.enter_window, text='Enter license plate:')
        label.pack(padx=5,pady=5)

        self.license_plate_val = tk.StringVar()

        plate_entry = ttk.Entry(self.enter_window, textvariable=self.license_plate_val)
        plate_entry.pack(padx=5,pady=5)

        label2 = ttk.Label(self.enter_window, text='Space:')
        label2.pack(padx=5,pady=5)

        self.space_val = tk.IntVar()

        space_entry = ttk.Entry(self.enter_window, textvariable=self.space_val)
        space_entry.pack(padx=5,pady=5)

        enter = tk.Button(self.enter_window, text="ENTER", command=self.enter_car,width=10)
        enter.pack(padx=5,pady=5)

    def enter_car(self):
        if len(self.license_plate_val.get()) != 7 or self.license_plate_val.get() in self.dbref.cars:
            tkinter.messagebox.showerror("Error.","License plate number must contain 7 characters and must be unique.")
        elif self.space_val.get() >= self.dbref.spaces or self.space_val.get() < 0 or self.dbref.full[self.space_val.get()] == True:
            tkinter.messagebox.showerror("Error.","Space has to be empty and within the range allowed by the parking lot.")
        else:
            self.dbref.enter(car.Car(self.license_plate_val.get(),self.space_val.get()))
            self.update()

            self.enter_window.destroy()

    # PAY functions
    def create_pay_window(self):
        self.pay_window = self.create_window()

        label = ttk.Label(self.pay_window, text='Enter license plate:')
        label.pack(padx=5,pady=5)

        self.license_plate_val_pay = tk.StringVar()

        plate_entry = ttk.Entry(self.pay_window, textvariable=self.license_plate_val_pay)
        plate_entry.pack(padx=5,pady=5)

        label2 = ttk.Label(self.pay_window, text='Enter the amount of time:')
        label2.pack(padx=5,pady=5)

        self.pay_val = tk.IntVar()

        pay_entry = ttk.Entry(self.pay_window, textvariable=self.pay_val)
        pay_entry.pack(padx=5,pady=5)

        self.pin_val = tk.StringVar()

        label3 = ttk.Label(self.pay_window, text='Enter your credit card PIN:')
        label3.pack(padx=5,pady=5)

        pin_entry = ttk.Entry(self.pay_window, textvariable=self.pin_val)
        pin_entry.pack(padx=5,pady=5)

        pay = tk.Button(self.pay_window, text="PAY", command=self.pay_car,width=10)
        pay.pack(padx=5,pady=5)

    def pay_car(self):
        if len(self.pin_val.get()) != 4 or not self.pin_val.get().isnumeric():
            tkinter.messagebox.showerror("Error.","Incorrect credit card PIN format.")
        if self.license_plate_val_pay.get() not in self.dbref.cars:
            tkinter.messagebox.showerror("Error.","License plate number must be associated with a car already parked in the garage.")
        elif self.pay_val.get() <= 0:
            tkinter.messagebox.showerror("Error.","Can only buy a positive, nonzero amount of time.")
        else:
            self.dbref.cars[self.license_plate_val_pay.get()].pay(self.pay_val.get())

            self.pay_window.destroy()
            self.update()

    # EXIT functions
    def create_exit_window(self):
        self.exit_window = self.create_window()

        label = ttk.Label(self.exit_window, text='Enter license plate:')
        label.pack(padx=5,pady=5)

        self.license_plate_val_exit = tk.StringVar()

        plate_entry = ttk.Entry(self.exit_window, textvariable=self.license_plate_val_exit)
        plate_entry.pack(padx=5,pady=5)

        pay = tk.Button(self.exit_window, text="EXIT", command=self.exit_car,width=10)
        pay.pack(padx=5,pady=5)

    def exit_car(self):
        if self.license_plate_val_exit.get() not in self.dbref.cars:
            tkinter.messagebox.showerror("Error.","License plate number must be associated with a car already parked in the garage.")
        else:
            self.dbref.remove(self.license_plate_val_exit.get())

            self.exit_window.destroy()
            self.update()

    # LOGIN functions
    def create_login_window(self):
        self.login_window = self.create_window()

        label1 = ttk.Label(self.login_window, text='Username:')
        label1.pack(padx=5,pady=5)

        self.login_username = tk.StringVar()

        login_u_entry = ttk.Entry(self.login_window, textvariable=self.login_username)
        login_u_entry.pack(padx=5,pady=5)

        label2 = ttk.Label(self.login_window, text='Password:')
        label2.pack(padx=5,pady=5)

        self.login_password = tk.StringVar()

        login_p_entry = ttk.Entry(self.login_window, textvariable=self.login_password)
        login_p_entry.pack(padx=5,pady=5)

        pay = tk.Button(self.login_window, text="LOGIN", command=self.login_user, width=10)
        pay.pack(padx=5,pady=5)

    def login_user(self):
        if self.login_username.get() not in self.staffdbref.credentials:
            tkinter.messagebox.showerror("Error.","Username not in credentials database.")
        else:
            l = self.staffdbref.login(self.login_username.get(), self.login_password.get())

            if l == True:
                tkinter.messagebox.showinfo("Success!", "You are logged in.")
                self.staff_logged_in = True
                self.login_window.destroy()
            else:
                tkinter.messagebox.showerror("Error.","Wrong password.")
                self.staff_logged_in = False

    # REMOVE functions
    def create_remove_window(self):
        self.remove_window = self.create_window()

        label = ttk.Label(self.remove_window, text='Enter license plate:')
        label.pack(padx=5,pady=5)

        self.license_plate_val_remove = tk.StringVar()

        plate_entry = ttk.Entry(self.remove_window, textvariable=self.license_plate_val_remove)
        plate_entry.pack(padx=5,pady=5)

        pay = tk.Button(self.remove_window, text="REMOVE", command=self.remove_car,width=10)
        pay.pack(padx=5,pady=5)

    def remove_car(self):
        if self.license_plate_val_remove.get() not in self.dbref.cars:
            tkinter.messagebox.showerror("Error.", "License plate number must be associated with a car already parked in the garage.")
        elif not self.staff_logged_in:
            tkinter.messagebox.showerror("Error.", "Log in to perform this action.")
        elif not self.dbref.cars[self.license_plate_val_remove.get()].invalid:
            tkinter.messagebox.showerror("Error.", "Car being removed is not in an invalid state.")
        else:
            self.dbref.remove(self.license_plate_val_remove.get())

            self.update()
            self.remove_window.destroy()


    def update(self):
        s = []
        c_tab = self.tabs.tab(self.tabs.select(),'text')

        for i in range(0,self.dbref.spaces):
            self.space_labels[i]['image'] = self.empty[i]
            self.space_labels[i]['text'] = i

        for license_plate in self.dbref.cars:
            if self.staff_logged_in and c_tab == 'Management staff':
                s.append(license_plate + " (time: " + str(self.dbref.cars[license_plate].timer) + ", paid: " + str(self.dbref.cars[license_plate].paid) +  ")")
            else:
                s.append(license_plate + " (ticket paid for: " + str(self.dbref.cars[license_plate].paid_for) + ")")

            if self.dbref.cars[license_plate].invalid and self.staff_logged_in and c_tab == 'Management staff':
                self.space_labels[self.dbref.cars[license_plate].space]['image'] = self.invalid_images[self.dbref.cars[license_plate].space]
            else:
                self.space_labels[self.dbref.cars[license_plate].space]['image'] = self.images[self.dbref.cars[license_plate].space]

            self.space_labels[self.dbref.cars[license_plate].space]['text'] = license_plate


        self.lchoices.set(s)