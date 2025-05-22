from app.status_codes import HTTP_200_OK,HTTP_201_CREATED,HTTP_202_ACCEPTED,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT,HTTP_404_NOT_FOUND ,HTTP_403_FORBIDDEN,HTTP_500_INTERNAL_SERVER_ERROR
from app.models.user_model import User
from flask import request,Blueprint,jsonify
import validators
from app.extensions import db


users = Blueprint("users",__name__,url_prefix="/api/v1/user")

@users.route("/register",methods=['POST'])
def register_user():
    data = request.json
    user_id = data.get('user_id')
    name =data.get('name')
    email =data.get('email')
    password =data.get('password')
    address = data.get('address')
    contact =data.get('contact')
    user_type = data.get('user_type')
    payment_details = data.get('payment_details')


    if not user_id or not name or not email or not password or not address or not contact or not user_type or not payment_details: 
        return jsonify({"Error":" All fields are required."}),HTTP_400_BAD_REQUEST
    
    
    try:
        new_user= User(
        user_id = user_id,
        name = name,
        email = email,
        password = password,
        address = address,
        contact = contact,
        user_type = user_type,
        payment_details = payment_details
        
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": f"{new_user} has been successfully created.",
            'user' :{
            'user_id': new_user.user_id,
            'name' :new_user.name,
            'email' :new_user.email,
            'password' :new_user.password,
            'address' :new_user.address,
            'contact' :new_user.contact,
            'user_type' :new_user.user_type,
            'payment_details':new_user.payment_details
                
            }
        }),HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}),HTTP_500_INTERNAL_SERVER_ERROR



@users.route("/user/<int:user_id>",methods =["GET"])
def get_user_by_id(user_id):
    data = request.json
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"Error":"User not found."})
    
    return jsonify({
        "message":"{user} has been succesfully updated.",
        "user":{
        'user_id': user.user_id,
            'name' :user.name,
            'email' :user.email,
            'password' :user.password,
            'address' :user.address,
            'contact' :user.contact,
            'user_type' :user.user_type,
            'payment_details':user.payment_details
                
        }
    }),HTTP_200_OK


@users.route("/update/<int:user_id>",methods=["PUT,PATCH"])
def update_user():
    data = request.json
    user = User.query.get(id)
    if not user:
        return jsonify({"Error":"User not found."})
   
    db.session.commit()

    return jsonify({
        "message":"{user} has been succesfully updated.",
        "user":{
           'user_id': user.user_id,
            'name' :user.name,
            'email' :user.email,
            'password' :user.password,
            'address' :user.address,
            'contact' :user.contact,
            'user_type' :user.user_type,
            'payment_details':user.payment_details
                 
        }
    }),HTTP_200_OK

# deleting all users
@users.route("/delete_all",methods =["DELETE"])
def delete_all():
    user = User.query.all()

    if not user:
        return jsonify({"Error":"User not found."}),HTTP_404_NOT_FOUND
    
    for user in users:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":"All users have been successfully deleted."}),HTTP_200_OK

    
    

