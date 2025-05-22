from flask import Blueprint,request,jsonify
from app.extensions import db
from app.models.cart_model import Cart
from app.status_codes import HTTP_200_OK,HTTP_201_CREATED,HTTP_202_ACCEPTED,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT,HTTP_404_NOT_FOUND ,HTTP_403_FORBIDDEN,HTTP_500_INTERNAL_SERVER_ERROR


# cart blueprint
carts = Blueprint("carts",__name__,url_prefix ="/api/v1/cart")

#creating a new cart
@carts.route("/register",methods=['POST'])
def register_cart():
    data = request.json
    cart_id = data.get('cart_id')
    quantity = data.get('quantity')
    date_added =data.get('date_added')
    user_id = data.get('user_id')
    product_id = data.get('product_id')

    if not cart_id or not quantity or not date_added:
        return jsonify({"Error":"All fields are required."}),HTTP_400_BAD_REQUEST
    
    if not user_id:
        return jsonify({"Error":"Enter the user_id."}),HTTP_400_BAD_REQUEST
    
    if not product_id:
        return jsonify({"Error":"Enter the product_id."}),HTTP_400_BAD_REQUEST
    
    try:
        #creating a new cart
        new_cart = Cart(
            cart_id = cart_id,
            quantity = quantity,
            date_added =date_added,
            user_id = user_id,
            product_id =product_id
        )

        db.session.add(new_cart)
        db.session.commit()

        return jsonify({
               "message":f"{new_cart} has been created successfully ",
               "cart":{
                "cart_id" : new_cart.cart_id,
                "quantity" : new_cart.quantity,
                "date_added": str(new_cart.date_added),
                "user_id" : new_cart.user_id,
                "product_id" : new_cart.product_id
            }
        }),HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
#getting all carts    
@carts.route("/",methods=["GET"])
def get_all_carts():
    data = request.json
    cart = Cart.query.all()

    cart_list=[{

              "cart_id" : cart.cart_id,
                "quantity" : cart.quantity,
                "date_added": str(cart.date_added),
                "user_id" : cart.user_id,
                "product_id" : cart.product_id
    }]
    return jsonify({"cart":cart_list}),HTTP_200_OK
    

#updating  cart by id
@carts.route("/<int:id>",methods =["GET"])
def get_cart_by_id(cart_id):
    data = request.json
    cart = Cart.query.filter_by(cart_id=cart_id).first()

    if not cart:
        return jsonify({"Error":"Cart not found."}),HTTP_404_NOT_FOUND
    
    return jsonify({
        "message":"{cart} has been succesfully updated.",
        "cart":{
                "cart_id" : cart.cart_id,
                "quantity" : cart.quantity,
                "date_added": str(cart.date_added),
                "user_id" : cart.user_id,
                "product_id" : cart.product_id
        }
    }),HTTP_200_OK

#deleting cart by id
@carts.route("/delete/<int:cart_id>",methods =["DELETE"])
def delete_cart(cart_id):
    cart = Cart.query.get(cart_id)

    if not cart:
        return jsonify({"Error":"Cart not found."}),HTTP_404_NOT_FOUND
    
    db.session.delete(cart)
    db.session.commit()

    return jsonify({
        "message":f"{cart.cart_id} has been deleted successfully. ",
               "cart":{
                "cart_id" : cart.cart_id,
                "quantity" : cart.quantity,
                "date_added": str(cart.date_added),
                "user_id" : cart.user_id,
                "product_id" : cart.product_id
            }
    }),HTTP_200_OK

#deleting all carts
@carts.route("/delete_all",methods=["DELETE"])
def delete_all_carts():
    carts=Cart.query.all()
    if not carts:
        return jsonify({"Error":"No carts found."}),HTTP_404_NOT_FOUND
    for cart in carts:
        db.session.delete(cart)
        db.session.commit()
    return jsonify({"message":"All carts have been deleted successfully."}),HTTP_200_OK

