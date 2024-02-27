from flask import Blueprint,jsonify,request
from model import User
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity,
)
from datetime import  timedelta


auth_bp = Blueprint('auth',__name__)

@auth_bp.post("/register")
def register_user():
    data = request.get_json()

    user = User.get_user_by_email(email=data.get("email"))

    if user is not None:
        return jsonify({"error": "User already exists"}), 409

    new_user = User(email=data.get("email"))

    new_user.set_password(password=data.get("password"))

    new_user.save()

    return jsonify({"message": "User created"}), 201


@auth_bp.post("/login")
def login_user():
    data = request.get_json()

    user = User.get_user_by_email(email=data.get("email"))

    if user and (user.check_password(password=data.get("password"))):
        access_token = create_access_token(identity=user.email, expires_delta=timedelta(minutes=1))
        refresh_token = create_refresh_token(identity=user.email)

        return (
            jsonify(
                {
                    "message": "Logged In ",
                    "tokens": {"access": access_token, 
                               "refresh": refresh_token},
                }
            ),
            200,
        )

    return jsonify({"error": "Invalid email or password"}), 400

@auth_bp.get('/hello')
@jwt_required()
def hello():
    current_user = get_jwt_identity()
    return jsonify(message=f'Hello, {current_user}!'), 200


@auth_bp.get("/refresh")
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)

    return jsonify({"access_token": new_access_token})
