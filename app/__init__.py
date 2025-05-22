from flask import Flask
from app.extensions import db,migrate
from app.controllers.cart_controller import carts
from app.controllers.order_controller import orders
from app.controllers.product_controller import  products
from app.controllers.user_controller import users


#application factory function
def create_app():
    
    #app instance
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app,db)

    #registering models
    from app.models.cart_model import Cart
    from app.models.order_model import Order
    from app.models.product_model import Product
    from app.models.user_model import User
    
    # registering blue_prints

    app.register_blueprint(products)
    app.register_blueprint(carts)
    app.register_blueprint(users)
    app.register_blueprint(orders)

    



    @app.route("/")
    def home():
        return "Python Exam"
    
  
    
    

    return app

