from app.extensions import db
from datetime import datetime

# product class
class Product(db.Model):
    __tablename__="products"
    product_id =db.Column(db.Integer,nullable = False,unique = True,primary_key = True)
    name = db.Column(db.String(255),nullable = False)
    description = db.Column(db.String(255),nullable = True)
    price = db.Column(db.Integer,nullable=False)
    category =db.Column(db.String(255),nullable= False)
    stock_quantity = db.Column(db.Integer,nullable = False)


    def __init__(self,product_id,name,description,price,category,stock_quantity):
        super(Product,self).__init__()
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.stock_quantity = stock_quantity
    
    def __repr__(self):
        return f"Product {self.name}"