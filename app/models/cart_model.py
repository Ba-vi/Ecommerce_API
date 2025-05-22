from app.extensions import db
from datetime import datetime


#cart class
class Cart(db.Model):
    
    __tablename__="carts"
    cart_id = db.Column(db.Integer,primary_key = True,unique = True,nullable = False)
    quantity = db.Column(db.Integer,nullable = False)
    date_added = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
    
    
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id",ondelete="CASCADE"))
    product_id = db.Column(db.Integer,db.ForeignKey("products.product_id",ondelete="CASCADE"))
    
    
    
    def __init__(self,cart_id,quantity,date_added,user_id,product_id):
        super(Cart,self).__init__()
        self.cart_id = cart_id
        self.quantity = quantity
        self.date_added =date_added
        # self.user_id = user_id
        # self.product_id = product_id

    def __repr__(self):
        return f"Cart {self.cart_id}"


