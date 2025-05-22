from flask import request,jsonify,Blueprint
from app.models.order_model import Order
from app.status_codes import HTTP_200_OK,HTTP_201_CREATED,HTTP_202_ACCEPTED,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT,HTTP_404_NOT_FOUND ,HTTP_403_FORBIDDEN,HTTP_500_INTERNAL_SERVER_ERROR
import validators
from app.extensions import db

orders = Blueprint("orders",__name__,url_prefix="/api/v1/order")

@orders.route("/register",methods=['POST'])
def register_order():
    data= request.json
    order_id = data.get('order_id')
    total_amount = data.get('total_amount')
    shipping_address = data.get('shipping_address')
    order_status =data.get('order_status')
    order_date = data.get('order_date')


    #validations
    if not order_id or not total_amount or not shipping_address or not order_status or not order_date:
        return jsonify({"Error":"All fields are required."}),HTTP_400_BAD_REQUEST
    
   
    try:
        #create new_order
        new_order = Order(
             order_id = order_id,
            total_amount = total_amount,
            shipping_address =shipping_address,
            order_status= order_status,
            order_date =order_date

        )
        db.session.add(new_order)
        db.session.commit()

        return jsonify({
            "message":f"{new_order} has been successfully made.",
            "order":{
            
                "order_id" : new_order.order_id,
                "total_amount" : new_order.total_amount,
                "shipping_address" :new_order.shipping_address,
                "order_status": new_order.order_status,
                "order_date" :new_order.order_date          
      
            }
        }),HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}),HTTP_500_INTERNAL_SERVER_ERROR


#getting order by id   
@orders.route("/order/<int:order_id>",methods =["GET"])
def get_order_id(order_id):
    data = request.json
    order = Order.query.filter_by(order_id=order_id).first()

    if not order:
        return jsonify({"Error":"order not found."})
    
    return jsonify({
        "message":f"{order.order_id} has been succesfully updated.",
        "order":{
        'order_id': order.order_id,
            'name' :order.name,
            'email' :order.email,
            'password' :order.password,
            'address' :order.address,
            'contact' :order.contact,
            'order_type' :order.order_type,
            'payment_details':order.payment_details
                
        }
    }),HTTP_200_OK

#updating order by id
@orders.route("/update/<int:order_id>",methods=["PUT,PATCH"])
def update_order(order_id):
    data=request.json
    # get order by id
    order = Order.query.filter_by(order_id =order_id).first()
    
    if not order:
        return jsonify({"Error":"Order not found"}),HTTP_404_NOT_FOUND
    
    db.session.commit()

    return jsonify({
        "message":"{order} has been updated.",
        "order":{
              "order_id" : order.order_id,
                "total_amount" : order.total_amount,
                "shipping_address" :order.shipping_address,
                "order_status": order.order_status,
                "order_date" :order.order_date          
      
        }

    }),HTTP_200_OK

@orders.route("/delete/<int:order_id>",methods =["DELETE"])

def delete_order(order_id):
    
    # get order by id
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({"Error":"Order not found"}),HTTP_404_NOT_FOUND
    
    db.session.delete(order)
    db.session.commit()

    return jsonify({
        "message":f"{order.order_id} has been deleted.",
        "order":{
              "order_id" : order.order_id,
                "total_amount" : order.total_amount,
                "shipping_address" :order.shipping_address,
                "order_status": order.order_status,
                "order_date" :order.order_date          
      
        }

    }),HTTP_200_OK

# delete all orders
@orders.route("/delete_all",methods=["DELETE"])
def delete_all():
    data = request.json
    order = Order.query.all()

    if not order in orders:
        return jsonify({"Error":"Order not found."})
    
    for order in orders:
        db.session.delete(order)
        db.session.commit()
        return jsonify({f"All orders have been successfully deleted."})

       

       

    
    



