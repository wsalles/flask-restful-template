from sources.db import db
from sources import settings
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from sources.security import authenticate, identify
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from resources.people import People, PeopleList
from resources.user import UserRegister
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


# URI to generate token in /auth
jwt = JWT(app, authenticate, identify)


# Routes
api.add_resource(PeopleList, '/people')
api.add_resource(People, '/person/<name>')
api.add_resource(GroupList, '/groups')
api.add_resource(Group, '/group/<name>')
api.add_resource(UserRegister, '/register/<username>')

# Feeds the Swagger
docs.register(PeopleList)
docs.register(People)
docs.register(GroupList)
docs.register(Group)
docs.register(UserRegister)


if "__main__" == __name__:
    app.run(host='0.0.0.0', port=5000)
