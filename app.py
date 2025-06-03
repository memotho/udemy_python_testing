import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, JWTError

from starter_code.security import authenticate, identity
from starter_code.resources.item import Item, ItemList
from starter_code.resources.store import Store, StoreList
from starter_code. resources.user import UserRegister

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'dan123'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # this allows to call /auth endpoint
 
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')


@app.errorhandler(JWTError)
def auth_error(err):
    return jsonify({'message': 'Could not authorize. Did you include a valid Authorization header?'}), 401

if __name__ == '__main__':
    from starter_code.db import db

    db.init_app(app)

    """if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()"""

    app.run(port=5000)
