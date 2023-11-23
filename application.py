import tkinter as tk

import carsdb
import staffdb
import car
import ui

def update():
    db.tick()
    ui.update()
    ui.r.after(3000,update)

db = carsdb.CarsDB()
sdb = staffdb.StaffDB()

ui = ui.UI(db, sdb)
ui.r.after(3000,update)

ui.update()
ui.initialize()