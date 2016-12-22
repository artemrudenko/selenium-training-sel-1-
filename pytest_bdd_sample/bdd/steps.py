import time
from pytest_bdd import given, when, then
from model.customer import Customer


@given("a customer list")
def get_customer_ids(app):
    return app.get_customer_ids()


@given("a valid customer")
def new_valid_customer():
    return Customer(firstname="Adam", lastname="Smith", phone="+0123456789",
                    address="Hidden Place", postcode="12345", city="New City",
                    country="US", zone="KS",
                    email="adam%s@smoth.me" % int(round(time.time()*1000)),
                    password="qwerty")


@when("I register the customer")
def register_customer(app, new_valid_customer):
    app.register_new_customer(new_valid_customer)


@then("new customer list contains all elements of the old customer list and a new element")
def verify_customer_registration(app, get_customer_ids):
    old_ids = get_customer_ids
    new_ids = app.get_customer_ids()

    assert all(l in new_ids for l in old_ids)
    assert len(new_ids) == len(old_ids) + 1
