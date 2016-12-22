import time

from app.application import Application
from model.customer import Customer


class Litecart:
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def init_fixtures(self):
        self.app = Application()

    def destroy_fixtures(self):
        self.app.quit()

    def get_customer_ids(self):
        return self.app.get_customer_ids()

    def new_valid_customer(self):
        return Customer(firstname="Adam", lastname="Smith", phone="+0123456789",
                        address="Hidden Place", postcode="12345", city="New City",
                        country="US", zone="KS",
                        email="adam%s@smith.me" % int(round(time.time()*1000)),
                        password="qwerty")

    def register_customer(self, customer):
        self.app.register_new_customer(customer)
