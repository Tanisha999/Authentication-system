import os
from flask import Flask
from extensions import db,jwt
from model import User
from auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'key'
    app.config['JWT_SECRET_KEY'] = 'secret_key'
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp,url_prefix='/auth')

    with app.app_context():
        db.create_all()
        print('database')
   


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)