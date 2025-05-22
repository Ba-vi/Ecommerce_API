from app.extensions import db
from datetime import datetime

#user class
class User(db.Model):

    __tablename__="users"
    user_id = db.Column(db.Integer,nullable = False,unique =True,primary_key = True)
    name = db.Column(db.String(200),nullable = False)
    email = db.Column(db.String(255),nullable = False)
    password = db.Column(db.String(50),nullable = False)
    address = db.Column(db.String(50),nullable = False)
    contact = db.Column(db.Integer,nullable = False)
    user_type = db.Column(db.String(100),nullable = False)
    payment_details = db.Column(db.String(255),nullable = False)


    def __init__(self,user_id,name,email,password,address,contact,user_type,payment_details):
        super(User,self).__init__()
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.contact = contact
        self.user_type = user_type
        self.payment_details = payment_details

    def __repr__(self):
        return f"User {self.name}"