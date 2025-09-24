from models import Restaurant, RestaurantPizza, Pizza
from app import app
from faker import Faker


class TestApp:
    '''Flask application in app.py'''

    def test_restaurants(self):
        """retrieves restaurants with GET request to /restaurants"""
        fake = Faker()
        restaurant1 = Restaurant.create(fake.name(), fake.address())
        restaurant2 = Restaurant.create(fake.name(), fake.address())

        restaurants = Restaurant.get_all()

        response = app.test_client().get('/restaurants')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        response_data = response.json
        assert [restaurant['id'] for restaurant in response_data] == [
            restaurant.id for restaurant in restaurants]
        assert [restaurant['name'] for restaurant in response_data] == [
            restaurant.name for restaurant in restaurants]
        assert [restaurant['address'] for restaurant in response_data] == [
            restaurant.address for restaurant in restaurants]
        for restaurant in response_data:
            assert 'restaurant_pizzas' not in restaurant

    def test_restaurants_id(self):
        '''retrieves one restaurant using its ID with GET request to /restaurants/<int:id>.'''

        fake = Faker()
        restaurant = Restaurant.create(fake.name(), fake.address())

        response = app.test_client().get(
            f'/restaurants/{restaurant.id}')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        response_data = response.json
        assert response_data['id'] == restaurant.id
        assert response_data['name'] == restaurant.name
        assert response_data['address'] == restaurant.address
        assert 'restaurant_pizzas' in response_data

    def test_returns_404_if_no_restaurant_to_get(self):
        '''returns an error message and 404 status code with GET request to /restaurants/<int:id> by a non-existent ID.'''

        response = app.test_client().get('/restaurants/0')
        assert response.status_code == 404
        assert response.content_type == 'application/json'
        assert response.json.get('error') == "Restaurant not found"

    def test_deletes_restaurant_by_id(self):
        '''deletes restaurant with DELETE request to /restaurants/<int:id>.'''

        fake = Faker()
        restaurant = Restaurant.create(fake.name(), fake.address())

        response = app.test_client().delete(
            f'/restaurants/{restaurant.id}')

        assert response.status_code == 204

        result = Restaurant.get_by_id(restaurant.id)
        assert result is None

    def test_returns_404_if_no_restaurant_to_delete(self):
        '''returns an error message and 404 status code with DELETE request to /restaurants/<int:id> by a non-existent ID.'''

        response = app.test_client().get('/restaurants/0')
        assert response.status_code == 404
        assert response.json.get('error') == "Restaurant not found"

    def test_pizzas(self):
        """retrieves pizzas with GET request to /pizzas"""
        fake = Faker()
        pizza1 = Pizza.create(fake.name(), fake.sentence())
        pizza2 = Pizza.create(fake.name(), fake.sentence())

        response = app.test_client().get('/pizzas')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        response_data = response.json

        pizzas = Pizza.get_all()

        assert [pizza['id'] for pizza in response_data] == [
            pizza.id for pizza in pizzas]
        assert [pizza['name'] for pizza in response_data] == [
            pizza.name for pizza in pizzas]
        assert [pizza['ingredients'] for pizza in response_data] == [
            pizza.ingredients for pizza in pizzas]
        for pizza in response_data:
            assert 'restaurant_pizzas' not in pizza

    def test_creates_restaurant_pizzas(self):
        '''creates one restaurant_pizzas using a pizza_id, restaurant_id, and price with a POST request to /restaurant_pizzas.'''

        fake = Faker()
        pizza = Pizza.create(fake.name(), fake.sentence())
        restaurant = Restaurant.create(fake.name(), fake.address())

        response = app.test_client().post(
            '/restaurant_pizzas',
            json={
                "price": 3,
                "pizza_id": pizza.id,
                "restaurant_id": restaurant.id,
            }
        )

        assert response.status_code == 201
        assert response.content_type == 'application/json'
        response_data = response.json
        assert response_data['price'] == 3
        assert response_data['pizza_id'] == pizza.id
        assert response_data['restaurant_id'] == restaurant.id
        assert response_data['id']
        assert response_data['pizza']
        assert response_data['restaurant']

    def test_400_for_validation_error(self):
        '''returns a 400 status code and error message if a POST request to /restaurant_pizzas fails.'''

        fake = Faker()
        pizza = Pizza.create(fake.name(), fake.sentence())
        restaurant = Restaurant.create(fake.name(), fake.address())

        # price not in 1..30
        response = app.test_client().post(
            '/restaurant_pizzas',
            json={
                "price": 0,
                "pizza_id": pizza.id,
                "restaurant_id": restaurant.id,
            }
        )

        assert response.status_code == 400
        assert response.json['errors'] == ["Price must be between 1 and 30"]

        response = app.test_client().post(
            '/restaurant_pizzas',
            json={
                "price": 31,
                "pizza_id": pizza.id,
                "restaurant_id": restaurant.id,
            }
        )

        assert response.status_code == 400
        assert response.json['errors'] == ["Price must be between 1 and 30"]
