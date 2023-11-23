class CarsDB:
    def __init__(self):
        self.cars = {}
        self.spaces = 20

    def enter(self,car):
        self.cars[car.license_plate] = car

    def pay(self, license_plate, time):
        if license_plate in self.cars:
            self.cars[license_plate].pay(time)

    def tick(self):
        for l in self.cars:
            self.cars[l].tick()

    def remove(self,license_plate):
        del self.cars[license_plate]