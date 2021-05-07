from sources.db import db
from sources import settings
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_apispec.extension import FlaskApiSpec
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from resources.people import People, PeopleList
from resources.user import User, UserRegister, UserLogin, UserLogout, TokenRefresh
from resources.group import Group, GroupList

app = Flask(__name__)
app.secret_key = 'wallace.salles'
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config.update({
    'APISPEC_SPEC': APISpec(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': settings.SWAGGER_API_URL,   # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': settings.SWAGGER_UI_URL  # URI to access UI of API Doc
})

api = Api(app)
docs = FlaskApiSpec(app)
db.init_app(app)


# If not, create all tables in the database
@app.before_first_request
def create_tables():
    db.create_all()


# JWT Config
app.config['JWT_SECRET_KEY'] = 'wallace'
app.config['JWT_BLACKLIST_ENABLED'] = True                        # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
jwt = JWTManager(app)                                             # URI to generate token in /login


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in settings.BLACKLIST


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'message': 'Ops! The token has expired',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token; Make sure to insert the correct HEADER",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({
        "description": "The token is not fresh. Please, try to refresh it via /refresh",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "description": "Your token has been revoked by someone",
        'error': 'token_revoked'
    }), 401

# JWT configuration ends


# Routes
api.add_resource(People, '/people')
api.add_resource(People, '/person/<name>')
api.add_resource(GroupList, '/groups')
api.add_resource(Group, '/group/<name>')
api.add_resource(UserRegister, '/register/<username>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

# Feeds the Swagger
docs.register(PeopleList)
docs.register(People)
docs.register(GroupList)
docs.register(Group)
docs.register(User)
docs.register(UserRegister)
docs.register(UserLogin)
docs.register(TokenRefresh)
docs.register(UserLogout)


if "__main__" == __name__:
    app.run(host='0.0.0.0', port=5000)
