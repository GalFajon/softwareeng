class CarsDB:
    def __init__(self):
        self.cars = {}

        self.spaces = 10
        self.full = [False for i in range(0,self.spaces)]

    def enter(self,car):
        if len(car.license_plate) == 7 and car.space < self.spaces and self.full[car.space] == False:
            self.full[car.space] = True
            self.cars[car.license_plate] = car

    def pay(self, license_plate, time):
        if license_plate in self.cars:
            self.cars[license_plate].pay(time)

    def tick(self):
        for l in self.cars:
            self.cars[l].tick()

    def remove(self,license_plate):
        self.full[self.cars[license_plate].space] = False
        del self.cars[license_plate]