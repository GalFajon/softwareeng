import unittest

import carsdb
import car
import staffdb

paydb = carsdb.CarsDB()
paydb.enter(car.Car('TEST123',0))

class TestApplication(unittest.TestCase):
    # CAR ENTRY
    def test_entry1(self):
        db = carsdb.CarsDB()

        with self.assertRaises(Exception):
            db.enter(car.Car('',-1))

    def test_entry2(self):
        db = carsdb.CarsDB()

        with self.assertRaises(Exception):
            db.enter(car.Car('',10))

    def test_entry3(self):
        db = carsdb.CarsDB()

        with self.assertRaises(Exception):
            db.enter(car.Car('',0))

    def test_entry4(self):
        db = carsdb.CarsDB()

        with self.assertRaises(Exception):
            db.enter(car.Car('TEST123',-1))

    def test_entry5(self):
        db = carsdb.CarsDB()

        with self.assertRaises(Exception):
            db.enter(car.Car('TEST123',10))

    def test_entry6(self):
        db = carsdb.CarsDB()

        db.enter(car.Car('TEST123',0))

        self.assertTrue('TEST123' in db.cars)
        self.assertTrue(db.full[0])

    def test_entry7(self):
        db = carsdb.CarsDB()

        with self.assertRaises(Exception):
            db.enter(car.Car('TEST1234',-1))

    def test_entry8(self):

        with self.assertRaises(Exception):
            db.enter(car.Car('TEST1234',10))

    def test_entry9(self):
        db = carsdb.CarsDB()

        with self.assertRaises(Exception):
            db.enter(car.Car('TEST1234',0))

    # CAR PAYMENT
    def test_pay1(self):
        with self.assertRaises(Exception):
            paydb.pay('TEST222',-1,'')

    def test_pay2(self):
        with self.assertRaises(Exception):
            paydb.pay('TEST222',-1,'12345')

    def test_pay3(self):
        with self.assertRaises(Exception):
            paydb.pay('TEST222',-1,'1234')

    def test_pay4(self):
        with self.assertRaises(Exception):
            paydb.pay('TEST222',1,'')

    def test_pay5(self):
        with self.assertRaises(Exception):
            paydb.pay('TEST222',1,'12345')

    def test_pay6(self):
        with self.assertRaises(Exception):
            paydb.pay('TEST222',1,'1234')

    def test_pay7(self):
        with self.assertRaises(Exception):
            paydb.pay('TEST123',-1,'')

    def test_pay8(self):
        with self.assertRaises(Exception):
            paydb.pay('TEST123',-1,'12345')

    def test_pay9(self):
        with self.assertRaises(Exception):
            paydb.pay('TEST123',-1,'1234')

    def test_pay10(self):
        with self.assertRaises(Exception):
            paydb.pay('TEST123',1,'')

    def test_pay11(self):
        with self.assertRaises(Exception):
            paydb.pay('TEST123',1,'12345')

    def test_pay12(self):
        paydb.pay('TEST123',1,'1234')
        self.assertTrue(paydb.cars['TEST123'].paid)

    # REMOVE CAR
    def test_remove1(self):
        db = carsdb.CarsDB()
        db.enter(car.Car('TEST123', 0))

        self.assertTrue('TEST123' in db.cars)

        db.remove('TEST123')

        self.assertTrue('TEST123' not in db.cars)

    def test_remove2(self):
        db = carsdb.CarsDB()

        with self.assertRaises(Exception):
            db.remove('TEST123')

    # LOGIN
    def test_login(self):
        sdb = staffdb.StaffDB()

        self.assertTrue(sdb.login('admin','admin'))
        self.assertFalse(sdb.login('','admin'))
        self.assertFalse(sdb.login('admin',''))
        self.assertFalse(sdb.login('',''))

if __name__ == '__main__':
    unittest.main()