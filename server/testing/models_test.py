import pytest
from models import Restaurant, Pizza, RestaurantPizza
from faker import Faker


class TestRestaurantPizza:
    '''Class RestaurantPizza in models.py'''

    def test_price_between_1_and_30(self):
        '''requires price between 1 and 30.'''

        pizza = Pizza.create(Faker().name(), "Dough, Sauce, Cheese")
        restaurant = Restaurant.create(Faker().name(), 'Main St')

        restaurant_pizza_1 = RestaurantPizza.create(1, restaurant.id, pizza.id)
        restaurant_pizza_2 = RestaurantPizza.create(30, restaurant.id, pizza.id)

    def test_price_too_low(self):
        '''requires price between 1 and 30 and fails when price is 0.'''

        pizza = Pizza.create(Faker().name(), "Dough, Sauce, Cheese")
        restaurant = Restaurant.create(Faker().name(), 'Main St')

        with pytest.raises(ValueError):
            restaurant_pizza = RestaurantPizza.create(0, restaurant.id, pizza.id)

    def test_price_too_high(self):
        '''requires price between 1 and 30 and fails when price is 31.'''

        pizza = Pizza.create(Faker().name(), "Dough, Sauce, Cheese")
        restaurant = Restaurant.create(Faker().name(), 'Main St')

        with pytest.raises(ValueError):
            restaurant_pizza = RestaurantPizza.create(31, restaurant.id, pizza.id)
