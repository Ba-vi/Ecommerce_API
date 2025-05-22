from app.extensions import db
from datetime import datetime


#Order class
class Order(db.Model):
    
    __tablename__="order"
    order_id=db.Column(db.Integer,nullable = False ,primary_key =True, unique=True)
    total_amount = db.Column(db.Integer,nullable = False)
    shipping_address = db.Column(db.String(255),nullable = False)
    order_status = db.Column(db.String(255),nullable = False)
    order_date = db.Column(db.DateTime,default= datetime.now)

    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id",ondelete="CASCADE"))

    def __init__(self,order_id,total_amount,shipping_address,order_status,order_date):
        super(Order,self).__init__()

        self.order_id = order_id
        self.total_amount = total_amount
        self.shipping_address = shipping_address
        self.order_status = order_status
        self.order_date = order_date
    def __repr__(self):
        return f"Order {self.order_status}"
