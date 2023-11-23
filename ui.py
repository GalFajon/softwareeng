import tkinter as tk
from tkinter import ttk

import car

class UI:
    def __init__(self, db, staffdb):
        self.staff_logged_in = False

        self.r = tk.Tk()

        self.dbref = db
        self.staffdbref = staffdb

        self.left = tk.Frame(self.r)
        self.right = tk.Frame(self.r)
        self.r_up = tk.Frame(self.right)
        self.r_down = tk.Frame(self.right)

        # car status list
        self.lchoices = tk.StringVar(value=[])
        self.l = tk.Listbox(self.left, listvariable=self.lchoices, height=20, width=25)

        # parking place status window

        # user actions tabs
        self.tabs = ttk.Notebook(self.r_down)
        self.tab_man = ttk.Frame(self.tabs)
        self.tab_u = ttk.Frame(self.tabs)

        # user action buttons
        self.enter = tk.Button(self.tab_u, text="ENTER", command=self.create_enter_window)
        self.pay = tk.Button(self.tab_u, text="PAY", command=self.create_pay_window)
        self.exit = tk.Button(self.tab_u, text="EXIT", command=self.create_exit_window)

        # management action buttons
        self.login = tk.Button(self.tab_man, text="LOGIN", command=self.create_login_window)
        self.remove = tk.Button(self.tab_man, text="REMOVE", command=self.create_remove_window)

    def initialize(self):
        self.left.pack(side="left")
        self.right.pack(side="left")
        self.r_up.pack(side="top")
        self.r_down.pack(side="bottom")

        self.l.pack()

        self.tabs.add(self.tab_u,text="Customers")
        self.tabs.add(self.tab_man,text="Management staff")
        self.tabs.pack(expand=1,fill="both")

        self.enter.pack(side="left")
        self.pay.pack(side="left")
        self.exit.pack(side="left")

        self.login.pack(side="left")
        self.remove.pack(side="left")

        self.r.mainloop()

    # ENTER functions
    def enter_car(self):
        self.dbref.enter(car.Car(self.license_plate_val.get(),self.space_val.get()))
        self.update()

        self.enter_window.destroy()

    def create_enter_window(self):
        self.enter_window = tk.Toplevel(self.r)

        label = ttk.Label(self.enter_window, text='Enter license plate:')
        label.pack()

        self.license_plate_val = tk.StringVar()

        plate_entry = ttk.Entry(self.enter_window, textvariable=self.license_plate_val)
        plate_entry.pack()

        self.space_val = tk.IntVar()

        space_entry = ttk.Entry(self.enter_window, textvariable=self.space_val)
        space_entry.pack()

        enter = tk.Button(self.enter_window, text="ENTER", command=self.enter_car)
        enter.pack()

    # PAY functions
    def create_pay_window(self):
        self.pay_window = tk.Toplevel(self.r)

        label = ttk.Label(self.pay_window, text='Enter license plate:')
        label.pack()

        self.license_plate_val_pay = tk.StringVar()

        plate_entry = ttk.Entry(self.pay_window, textvariable=self.license_plate_val_pay)
        plate_entry.pack()

        self.pay_val = tk.IntVar()

        pay_entry = ttk.Entry(self.pay_window, textvariable=self.pay_val)
        pay_entry.pack()

        pay = tk.Button(self.pay_window, text="PAY", command=self.pay_car)
        pay.pack()

    def pay_car(self):
        if self.license_plate_val_pay.get() in self.dbref.cars:
            self.dbref.cars[self.license_plate_val_pay.get()].pay(self.pay_val.get())

        self.update()

    # EXIT functions
    def create_exit_window(self):
        self.exit_window = tk.Toplevel(self.r)

        label = ttk.Label(self.exit_window, text='Enter license plate:')
        label.pack()

        self.license_plate_val_exit = tk.StringVar()

        plate_entry = ttk.Entry(self.exit_window, textvariable=self.license_plate_val_exit)
        plate_entry.pack()

        pay = tk.Button(self.exit_window, text="EXIT", command=self.exit_car)
        pay.pack()

    def exit_car(self):
        if self.license_plate_val_exit.get() in self.dbref.cars:
            self.dbref.remove(self.license_plate_val_exit.get())

        self.update()

    # LOGIN functions
    def create_login_window(self):
        self.login_window = tk.Toplevel(self.r)

        label1 = ttk.Label(self.login_window, text='Username:')
        label1.pack()

        self.login_username = tk.StringVar()

        login_u_entry = ttk.Entry(self.login_window, textvariable=self.login_username)
        login_u_entry.pack()

        label2 = ttk.Label(self.login_window, text='Password:')
        label2.pack()

        self.login_password = tk.StringVar()

        login_p_entry = ttk.Entry(self.login_window, textvariable=self.login_password)
        login_p_entry.pack()

        pay = tk.Button(self.login_window, text="LOGIN", command=self.login_user)
        pay.pack()

    def login_user(self):
        if self.login_username.get() in self.staffdbref.credentials:
            l = self.staffdbref.login(self.login_username.get(), self.login_password.get())

            if l == True:
                self.staff_logged_in = True
            else:
                self.staff_logged_in = False

        self.login_window.destroy()

    # REMOVE functions
    def create_remove_window(self):
        self.remove_window = tk.Toplevel(self.r)

        label = ttk.Label(self.remove_window, text='Enter license plate:')
        label.pack()

        self.license_plate_val_remove = tk.StringVar()

        plate_entry = ttk.Entry(self.remove_window, textvariable=self.license_plate_val_remove)
        plate_entry.pack()

        pay = tk.Button(self.remove_window, text="REMOVE", command=self.remove_car)
        pay.pack()

    def remove_car(self):
        if self.license_plate_val_remove.get() in self.dbref.cars:
            if self.staff_logged_in and self.dbref.cars[self.license_plate_val_remove.get()].invalid:
                self.dbref.remove(self.license_plate_val_remove.get())

        self.update()


    def update(self):
        s = []

        for license_plate in self.dbref.cars:
            s.append(license_plate + " (time: " + str(self.dbref.cars[license_plate].timer) + ", paid: " + str(self.dbref.cars[license_plate].paid) +  ")")

        self.lchoices.set(s)