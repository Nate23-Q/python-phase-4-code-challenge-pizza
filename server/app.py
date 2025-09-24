#!/usr/bin/env python3
from models import Restaurant, RestaurantPizza, Pizza, init_db
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

app = Flask(__name__)
app.json.compact = False

api = Api(app)

# Initialize the database
init_db()

class RestaurantsResource(Resource):
    def get(self):
        restaurants = Restaurant.get_all()
        return [r.to_dict() for r in restaurants]

class RestaurantByID(Resource):
    def get(self, id):
        restaurant = Restaurant.get_by_id(id)
        if restaurant:
            restaurant_pizzas = RestaurantPizza.get_by_restaurant_id(id)
            result = restaurant.to_dict()
            result['restaurant_pizzas'] = [rp.to_dict() for rp in restaurant_pizzas]
            return result
        return {"error": "Restaurant not found"}, 404

    def delete(self, id):
        restaurant = Restaurant.get_by_id(id)
        if restaurant:
            Restaurant.delete_by_id(id)
            return "", 204
        return {"error": "Restaurant not found"}, 404

class PizzasResource(Resource):
    def get(self):
        pizzas = Pizza.get_all()
        return [p.to_dict() for p in pizzas]

class RestaurantPizzasResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            restaurant_pizza = RestaurantPizza.create(
                data['price'],
                data['restaurant_id'],
                data['pizza_id']
            )
            return restaurant_pizza.to_dict(), 201
        except ValueError as e:
            return {"errors": [str(e)]}, 400

api.add_resource(RestaurantsResource, '/restaurants')
api.add_resource(RestaurantByID, '/restaurants/<int:id>')
api.add_resource(PizzasResource, '/pizzas')
api.add_resource(RestaurantPizzasResource, '/restaurant_pizzas')

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
