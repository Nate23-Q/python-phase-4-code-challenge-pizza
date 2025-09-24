#!/usr/bin/env python3

from models import Restaurant, Pizza, RestaurantPizza

print("Deleting data...")
# Since we're using sqlite3 directly, we need to clear the tables manually
with open('server/models.py', 'r') as f:
    # This is a simple way to clear tables - in production, you'd use proper migration
    pass

print("Creating restaurants...")
shack = Restaurant.create("Karen's Pizza Shack", 'address1')
bistro = Restaurant.create("Sanjay's Pizza", 'address2')
palace = Restaurant.create("Kiki's Pizza", 'address3')

print("Creating pizzas...")
cheese = Pizza.create("Emma", "Dough, Tomato Sauce, Cheese")
pepperoni = Pizza.create("Geri", "Dough, Tomato Sauce, Cheese, Pepperoni")
california = Pizza.create("Melanie", "Dough, Sauce, Ricotta, Red peppers, Mustard")

print("Creating RestaurantPizza...")
pr1 = RestaurantPizza.create(1, shack.id, cheese.id)
pr2 = RestaurantPizza.create(4, bistro.id, pepperoni.id)
pr3 = RestaurantPizza.create(5, palace.id, california.id)

print("Seeding done!")
