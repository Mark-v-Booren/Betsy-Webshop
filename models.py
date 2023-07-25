from peewee import Model, SqliteDatabase, ForeignKeyField, CharField, DecimalField, IntegerField, Check

# Replace 'your_database.db' with your actual database file name
db = SqliteDatabase('betsy_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField(max_length=100, unique=True)
    address = CharField(max_length=255)
    billing_info = CharField(max_length=100)

class Tag(BaseModel):
    name = CharField(max_length=50, unique=True)

class Product(BaseModel):
    name = CharField(max_length=100, unique=True)
    description = CharField(max_length=255)
    price_per_unit = DecimalField(max_digits=10, decimal_places=2, constraints=[Check('price_per_unit >= 0')])
    quantity_in_stock = IntegerField(constraints=[Check('quantity_in_stock >= 0')])
    tags = ForeignKeyField(Tag, backref='products', null=True)
    owner = ForeignKeyField(User, backref='products')

class Transaction(BaseModel):
    buyer = ForeignKeyField(User, backref='transactions')
    product = ForeignKeyField(Product, backref='transactions')
    quantity_purchased = IntegerField(constraints=[Check('quantity_purchased > 0')])

# Populate the test database with example data
def populate_test_database():
    # Create example tags
    tag1 = Tag.create(name='Electronics')
    tag2 = Tag.create(name='Music')
    tag3 = Tag.create(name='Books')
    tag4 = Tag.create(name='Star Wars')
    tag5 = Tag.create(name='Wood')
    tag6 = Tag.create(name='Comics')

    # Create example users
    user1 = User.create(name='ALex', address='Paris rua de la Nuit', billing_info='ING 002020202022020')
    user2 = User.create(name='Rocky', address='Amsterdam, Overtoom 123', billing_info='ABN AMRO 0303030303030')
    user3 = User.create(name='Storm van Ballegooij', address='New York , west-end 333', billing_info='Credit Card')
    user4 = User.create(name='Lisa Purple', address='Amstel, zoetermeer', billing_info='PayPal username :LALALA')

    # Create example products
    product1 = Product.create(name='Electric Guitar', description='Washburn 1992', price_per_unit=1000.00, owner=user1, quantity_in_stock=2, tags=tag2) 
    product2 = Product.create(name='T-Shirt', description='Cotton t-shirt', price_per_unit=20.00, quantity_in_stock=100, owner=user2, tags=tag2)
    product3 = Product.create(name='Python Crash Course', description='Python programming book', price_per_unit=30.00, owner=user1, quantity_in_stock=30, tags=tag3)
    product4 = Product.create(name='Yoda', description='Original Star Wars prop, 1983', price_per_unit=5.000, owner=user4, quantity_in_stock=1, tags=tag4)
    product5 = Product.create(name='Wooden Table', description='Log', price_per_unit=155.00, owner=user3, quantity_in_stock=5, tags=tag5)
    product6 = Product.create(name='Book of Frank', description='Jim woodrings: Franks adventures', price_per_unit=30.00, owner=user2, quantity_in_stock=3, tags=tag6)
    product7 = Product.create(name='Desktop', description='Cooler Master Gaming laptop 2020', price_per_unit=800.00, owner=user1, quantity_in_stock=2, tags=tag1)

    # Create example transactions
    transaction1 = Transaction.create(buyer=user1, product=product1, quantity_purchased=2)
    transaction2 = Transaction.create(buyer=user2, product=product2, quantity_purchased=3)
    transaction3 = Transaction.create(buyer=user1, product=product3, quantity_purchased=1)
    transaction4 = Transaction.create(buyer=user1, product=product4, quantity_purchased=1)
    transaction5 = Transaction.create(buyer=user1, product=product5, quantity_purchased=1)
    transaction6 = Transaction.create(buyer=user1, product=product6, quantity_purchased=2)
    transaction7 = Transaction.create(buyer=user1, product=product7, quantity_purchased=1)


if __name__ == "__main__":

    db.create_tables([User, Tag, Product, Transaction])

    # Populate the test database with example data
    populate_test_database()


        