import sqlite3
from contextlib import contextmanager

DATABASE = 'app.db'

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS pizzas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ingredients TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS restaurant_pizzas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                price INTEGER NOT NULL,
                restaurant_id INTEGER NOT NULL,
                pizza_id INTEGER NOT NULL,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants (id) ON DELETE CASCADE,
                FOREIGN KEY (pizza_id) REFERENCES pizzas (id) ON DELETE CASCADE
            )
        ''')
        conn.commit()

class Restaurant:
    def __init__(self, id=None, name=None, address=None):
        self.id = id
        self.name = name
        self.address = address

    @classmethod
    def create(cls, name, address):
        with get_db() as conn:
            cursor = conn.execute('INSERT INTO restaurants (name, address) VALUES (?, ?)', (name, address))
            conn.commit()
            return cls(cursor.lastrowid, name, address)

    @classmethod
    def get_all(cls):
        with get_db() as conn:
            cursor = conn.execute('SELECT * FROM restaurants')
            return [cls(*row) for row in cursor.fetchall()]

    @classmethod
    def get_by_id(cls, id):
        with get_db() as conn:
            cursor = conn.execute('SELECT * FROM restaurants WHERE id = ?', (id,))
            row = cursor.fetchone()
            return cls(*row) if row else None

    @classmethod
    def delete_by_id(cls, id):
        with get_db() as conn:
            conn.execute('DELETE FROM restaurants WHERE id = ?', (id,))
            conn.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }

class Pizza:
    def __init__(self, id=None, name=None, ingredients=None):
        self.id = id
        self.name = name
        self.ingredients = ingredients

    @classmethod
    def create(cls, name, ingredients):
        with get_db() as conn:
            cursor = conn.execute('INSERT INTO pizzas (name, ingredients) VALUES (?, ?)', (name, ingredients))
            conn.commit()
            return cls(cursor.lastrowid, name, ingredients)

    @classmethod
    def get_all(cls):
        with get_db() as conn:
            cursor = conn.execute('SELECT * FROM pizzas')
            return [cls(*row) for row in cursor.fetchall()]

    @classmethod
    def get_by_id(cls, id):
        with get_db() as conn:
            cursor = conn.execute('SELECT * FROM pizzas WHERE id = ?', (id,))
            row = cursor.fetchone()
            return cls(*row) if row else None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }

class RestaurantPizza:
    def __init__(self, id=None, price=None, restaurant_id=None, pizza_id=None):
        self.id = id
        self.price = price
        self.restaurant_id = restaurant_id
        self.pizza_id = pizza_id

    @classmethod
    def create(cls, price, restaurant_id, pizza_id):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")
        with get_db() as conn:
            cursor = conn.execute('INSERT INTO restaurant_pizzas (price, restaurant_id, pizza_id) VALUES (?, ?, ?)', (price, restaurant_id, pizza_id))
            conn.commit()
            return cls(cursor.lastrowid, price, restaurant_id, pizza_id)

    @classmethod
    def get_by_restaurant_id(cls, restaurant_id):
        with get_db() as conn:
            cursor = conn.execute('''
                SELECT rp.*, r.name as restaurant_name, r.address as restaurant_address,
                       p.name as pizza_name, p.ingredients as pizza_ingredients
                FROM restaurant_pizzas rp
                JOIN restaurants r ON rp.restaurant_id = r.id
                JOIN pizzas p ON rp.pizza_id = p.id
                WHERE rp.restaurant_id = ?
            ''', (restaurant_id,))
            rows = cursor.fetchall()
            return [cls(*row[:4]) for row in rows]

    def to_dict(self):
        with get_db() as conn:
            cursor = conn.execute('''
                SELECT r.name as restaurant_name, r.address as restaurant_address,
                       p.name as pizza_name, p.ingredients as pizza_ingredients
                FROM restaurants r, pizzas p
                WHERE r.id = ? AND p.id = ?
            ''', (self.restaurant_id, self.pizza_id))
            row = cursor.fetchone()
            if row is None:
                return {
                    'id': self.id,
                    'price': self.price,
                    'restaurant_id': self.restaurant_id,
                    'pizza_id': self.pizza_id,
                    'restaurant': None,
                    'pizza': None
                }
            return {
                'id': self.id,
                'price': self.price,
                'restaurant_id': self.restaurant_id,
                'pizza_id': self.pizza_id,
                'restaurant': {
                    'id': self.restaurant_id,
                    'name': row['restaurant_name'],
                    'address': row['restaurant_address']
                },
                'pizza': {
                    'id': self.pizza_id,
                    'name': row['pizza_name'],
                    'ingredients': row['pizza_ingredients']
                }
            }
