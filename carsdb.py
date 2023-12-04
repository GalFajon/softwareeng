class CarsDB:
    def __init__(self):
        self.cars = {}

        self.spaces = 10
        self.full = [False for i in range(0,self.spaces)]

    def enter(self,car):
        if len(car.license_plate) == 7 and car.space >= 0 and car.space < self.spaces and self.full[car.space] == False:
            self.full[car.space] = True
            self.cars[car.license_plate] = car
        else:
            raise Exception("License plate must be 7 characters long and not already in the parking garage.")

    def pay(self, license_plate, time, pin):
        if license_plate in self.cars and time > 0 and pin.isnumeric() and len(pin) == 4:
            self.cars[license_plate].pay(time)
        else:
            raise Exception("License plate has to be 7 characters long and in the garage and the time paid for must be larger than zero. The input pin must be a numeric string of 4 characters.")

    def tick(self):
        for l in self.cars:
            self.cars[l].tick()

    def remove(self,license_plate):
        if license_plate in self.cars:
            self.full[self.cars[license_plate].space] = False
            del self.cars[license_plate]
        else:
            raise Exception("License plate has to be inside of the garage in order for it to be removed.")