class Car:
    def __init__(self, license_plate, space):
        self.paid = False
        self.invalid = False

        self.license_plate = license_plate.upper()
        self.space = space

        self.timer = 10
        self.paid_for = 0

    def pay(self, time):
        if not self.paid:
            self.timer = time
        else:
            self.timer += time

        self.invalid = False
        self.paid = True
        self.paid_for = self.timer


    def tick(self):
        self.timer -= 1

        if self.timer <= 0:
            self.timer = 0
            self.invalid = True