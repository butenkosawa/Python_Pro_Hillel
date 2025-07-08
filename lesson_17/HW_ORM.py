import psycopg
from dataclasses import dataclass
from datetime import date
from pprint import pprint as print


connection_payload = {
    'dbname': 'catering',
    'user': 'postgres',
    'password': 'uhtrekm86',
    'host': 'localhost',
    'port': 5432
}

class DatabaseConnection:
    def __enter__(self):
        self.conn = psycopg.connect(**connection_payload)
        self.cur = self.conn.cursor()
        return self
    
    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        
        self.cur.close()
        self.conn.close()
    
    def query(self, sql: str, params: tuple | None):
        self.cur.execute(sql, params or ())
        return self.cur.fetchall()


@dataclass
class User:
    name: str
    phone: str
    role: str
    id: int | None = None

    @classmethod
    def all(cls) -> list["User"]:
        """return all the users from `users` table"""

        with DatabaseConnection() as db:
            rows = db.query("SELECT name, phone, role, id FROM users", ())
            return [cls(*row) for row in rows]

    @classmethod
    def filter(cls, **filters) -> list["User"]:
        """return filtered users from `users` table"""

        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(f"SELECT name, phone, role, id FROM users WHERE {conditions}", values)
            
            return [cls(*row) for row in rows]
        
    @classmethod
    def get(cls, **filters) -> "User":
        """return filtered user from `users` table"""

        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            rows = db.query(f"SELECT name, phone, role, id FROM users WHERE {conditions}", values)
            name, phone, role, id = rows[0]

            return cls(name=name, phone=phone, role=role, id=id)

    def create(self) -> "User":
        with DatabaseConnection() as db:
            db.cur.execute(
                "INSERT INTO users (name, phone, role) VALUES (%s, %s, %s) RETURNING id",
                (self.name, self.phone, self.role)
            )
            # NOTE: actually bad practice to mutate `self` instance from here
            self.id = db.cur.fetchone()[0]
            
            return self

    def update(self, **payload) -> "User | None":
        fields = ", ".join([f"{key} = %s" for key in payload.keys()])
        values = tuple(payload.values())

        # ensure id exists
        if self.id is None:
            raise ValueError("Cannot update user without ID")
        
        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE users SET {fields} WHERE id = %s RETURNING id, name, phone, role",
                (*values, self.id)
            )
            
            row = db.cur.fetchone()

            if not row:
                return None
            else:
                _, name, phone, role = row
                self.name = name
                self.phone = phone
                self.role = role
            
            return self

    @classmethod
    def delete(cls, **filters):
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            db.cur.execute(f"DELETE FROM users WHERE {conditions} RETURNING id", values)

            return db.cur.fetchone() is not None


@dataclass
class Dish:
    name: str
    price: float
    id: int | None = None

    @classmethod
    def all(cls) -> list["Dish"]:
        with DatabaseConnection() as db:
            rows = db.query("SELECT name, price, id FROM dishes", ())
            return [cls(*row) for row in rows]

    @classmethod
    def filter(cls, **filters) -> list["Dish"]:
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())
        with DatabaseConnection() as db:
            rows = db.query(f"SELECT name, price, id FROM dishes WHERE {conditions}", values)
            return [cls(name=row[0], price=float(row[1]), id=row[2]) for row in rows]

    @classmethod
    def get(cls, **filters) -> "Dish":
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())
        with DatabaseConnection() as db:
            rows = db.query(f"SELECT name, price, id FROM dishes WHERE {conditions}", values)
            name, price, id = rows[0]
            return cls(name=name, price=float(price), id=id)

    def create(self) -> "Dish":
        with DatabaseConnection() as db:
            db.cur.execute(
                "INSERT INTO dishes (name, price) VALUES (%s, %s) RETURNING id",
                (self.name, self.price)
            )
            self.id = db.cur.fetchone()[0]
            return self

    def update(self, **payload) -> "Dish | None":
        fields = ", ".join([f"{key} = %s" for key in payload.keys()])
        values = tuple(payload.values())
        if self.id is None:
            raise ValueError("Cannot update dish without ID")
        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE dishes SET {fields} WHERE id = %s RETURNING id, name, price",
                (*values, self.id)
            )
            row = db.cur.fetchone()
            if not row:
                return None
            else:
                _, name, price = row
                self.name = name
                self.price = float(price)
            return self

    @classmethod
    def delete(cls, **filters):
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            db.cur.execute(f"DELETE FROM dishes WHERE {conditions} RETURNING id", values)

            return db.cur.fetchone() is not None


@dataclass
class Order:
    date: date
    total: float
    status: str
    user_id: int
    id: int | None = None

    @classmethod
    def all(cls) -> list["Order"]:
        with DatabaseConnection() as db:
            rows = db.query("SELECT date, total, status, user_id, id FROM orders", ())
            return [cls(date=row[0], total=float(row[1]), status=row[2], user_id=row[3], id=row[4]) for row in rows]

    @classmethod
    def filter(cls, **filters) -> list["Order"]:
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())
        with DatabaseConnection() as db:
            rows = db.query(f"SELECT date, total, status, user_id, id FROM orders WHERE {conditions}", values)
            return [
                cls(date=row[0], total=float(row[1]), status=row[2], user_id=row[3], id=row[4])
                for row in rows
            ]

    @classmethod
    def get(cls, **filters) -> "Order":
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())
        with DatabaseConnection() as db:
            rows = db.query(f"SELECT date, total, status, user_id, id FROM orders WHERE {conditions}", values)
            date_, total, status, user_id, id = rows[0]
            return cls(date=date_, total=float(total), status=status, user_id=user_id, id=id)

    def create(self) -> "Order":
        with DatabaseConnection() as db:
            db.cur.execute(
                "INSERT INTO orders (date, total, status, user_id) VALUES (%s, %s, %s, %s) RETURNING id",
                (self.date, self.total, self.status, self.user_id)
            )
            self.id = db.cur.fetchone()[0]
            return self

    def update(self, **payload) -> "Order | None":
        fields = ", ".join([f"{key} = %s" for key in payload.keys()])
        values = tuple(payload.values())
        if self.id is None:
            raise ValueError("Cannot update order without ID")
        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE orders SET {fields} WHERE id = %s RETURNING id, date, total, status, user_id",
                (*values, self.id)
            )
            row = db.cur.fetchone()
            if not row:
                return None
            else:
                _, date_, total, status, user_id = row
                self.date = date_
                self.total = float(total)
                self.status = status
                self.user_id = user_id
            return self

    @classmethod
    def delete(cls, **filters):
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            db.cur.execute(f"DELETE FROM orders WHERE {conditions} RETURNING id", values)

            return db.cur.fetchone() is not None


@dataclass
class OrderItem:
    order_id: int
    dish_id: int
    quantity: int
    id: int | None = None

    @classmethod
    def all(cls) -> list["OrderItem"]:
        with DatabaseConnection() as db:
            rows = db.query("SELECT order_id, dish_id, quantity, id FROM order_items", ())
            return [cls(*row) for row in rows]

    @classmethod
    def filter(cls, **filters) -> list["OrderItem"]:
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())
        with DatabaseConnection() as db:
            rows = db.query(f"SELECT order_id, dish_id, quantity, id FROM order_items WHERE {conditions}", values)
            return [
                cls(order_id=row[0], dish_id=row[1], quantity=row[2], id=row[3])
                for row in rows
            ]

    @classmethod
    def get(cls, **filters) -> "OrderItem":
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())
        with DatabaseConnection() as db:
            rows = db.query(f"SELECT order_id, dish_id, quantity, id FROM order_items WHERE {conditions}", values)
            order_id, dish_id, quantity, id = rows[0]
            return cls(order_id=order_id, dish_id=dish_id, quantity=quantity, id=id)

    def create(self) -> "OrderItem":
        with DatabaseConnection() as db:
            db.cur.execute(
                "INSERT INTO order_items (order_id, dish_id, quantity) VALUES (%s, %s, %s) RETURNING id",
                (self.order_id, self.dish_id, self.quantity)
            )
            self.id = db.cur.fetchone()[0]
            return self

    def update(self, **payload) -> "OrderItem | None":
        fields = ", ".join([f"{key} = %s" for key in payload.keys()])
        values = tuple(payload.values())
        if self.id is None:
            raise ValueError("Cannot update order item without ID")
        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE order_items SET {fields} WHERE id = %s RETURNING id, order_id, dish_id, quantity",
                (*values, self.id)
            )
            row = db.cur.fetchone()
            if not row:
                return None
            else:
                _, order_id, dish_id, quantity = row
                self.order_id = order_id
                self.dish_id = dish_id
                self.quantity = quantity
            return self

    @classmethod
    def delete(cls, **filters):
        keys = filters.keys()
        conditions = " AND ".join([f"{key} = %s" for key in keys])
        values = tuple(filters.values())

        with DatabaseConnection() as db:
            db.cur.execute(f"DELETE FROM order_items WHERE {conditions} RETURNING id", values)

            return db.cur.fetchone() is not None


# SELECT ALL USERS FROM USERS TABLE
# ---------------------------------
# users = User.all()
# print(users)

# FILTER USERS
# ---------------------------------
# users: list[User] = User.filter(role='USER', id=2)
# print(users)

# RETRIVE USER
# ---------------------------------
# user: User = User.get(id=3)
# print(user)

# CREATE USER
# ---------------------------------
# mark = User(name="Mark", phone="+380631116897", role='USER')
# print(f"Before creation: {mark}")
# 
# mark.create()
# print(f"After creation: {mark}")

# UPDATE USER
# ---------------------------------
# mark = User.get(name="Mark")
# mark.update(role="ADMIN")
# print(mark)

# DELETE USER
# ---------------------------------
# User.delete(id=3)
# print(User.all())


print(User.all())