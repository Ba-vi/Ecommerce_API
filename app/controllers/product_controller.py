from app.status_codes import HTTP_200_OK,HTTP_201_CREATED,HTTP_202_ACCEPTED,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT,HTTP_404_NOT_FOUND ,HTTP_403_FORBIDDEN,HTTP_500_INTERNAL_SERVER_ERROR
from app.models.product_model import Product
import validators
from flask import Blueprint,jsonify,request
from app.extensions import db

products = Blueprint("products",__name__,url_prefix="/api/v1/product")

@products.route("/register",methods =["POST"])
def register_product():
    data = request.json
    product_id = data.get('product_id')
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    category =data.get('category')
    stock_quantity = data.get('stock_quantity')

    if not product_id or not name or not description or not price or not category or not stock_quantity:
        return jsonify({"Error":"All fields are required."}),HTTP_400_BAD_REQUEST
    
    
    try:
        new_product =Product(
           product_id = product_id,
            name = name,
            description = description,
            price = price,
            category = category,
            stock_quantity = stock_quantity
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            "message":f" {new_product} has been successfully registered",
            "product" :{
            'product_id' :new_product.product_id,
            'name' : new_product.name,
            'description' :new_product.description,
            'price' :new_product.price,
            'category' : new_product.category,
            'stock_quantity' : new_product.stock_quantity
            }
        }),HTTP_201_CREATED
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error"+ str(e)}),HTTP_500_INTERNAL_SERVER_ERROR

@products.route("/product/<int:product_id>",methods =["GET"])
def get_product_by_id(product_id):
    data = request.json
    product = Product.query.filter_by(product_id=product_id).first()

    if not product:
        return jsonify({"Error":"product not found."}),HTTP_404_NOT_FOUND
    
    return jsonify({
        "message":"{product} has been succesfully updated.",
        "product":{
        'product_id': product.product_id,
            'name' :product.name,
            'email' :product.email,
            'password' :product.password,
            'address' :product.address,
            'contact' :product.contact,
            'product_type' :product.product_type,
            'payment_details':product.payment_details
                
        }
    }),HTTP_200_OK

@products.route("/update/<int:product_id>",methods =["PUT,PATCH"])
def product_update(product_id):
    data = request.json
    product = Product.query.filter_by(product_id = product_id)

    if not product:
        return jsonify({"Error":"Product not found."}),HTTP_404_NOT_FOUND
    
    
    db.session.commit()

    return jsonify({
        "message":"{product} has been successfully updated.",
        "product":{
         'product_id' :product.product_id,
            'name' : product.name,
            'description' :product.description,
            'price' :product.price,
            'category' : product.category,
            'stock_quantity' : product.stock_quantity
        }
    }),HTTP_200_OK

#deleting all products
@products.route("/delete_all",methods=["DELETE"])
def delete_all():
    data = request.json
    product = Product.query.all()

    if not product:
        return jsonify({"Error":"Product not found."}),HTTP_404_NOT_FOUND
    for product in products:
        db.session.delete(product)
        db.session.commit()

        return jsonify({f"Products have been successfully deleted."}),HTTP_200_OK
