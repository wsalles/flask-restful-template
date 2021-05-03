from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from sources.db import db
from sources.security import authenticate, identify

from resources.people import People, PeopleList
from resources.user import UserRegister
from resources.group import Group, GroupList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'wallace.salles'
api = Api(app)
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identify)


@app.route('/')
def index():
    style = "border-color:black;border-style:solid;border-width:1px"
    routes = f"<table align=center><thead>"
    for url in app.url_map.iter_rules():
        routes += f'''
          <tr>
            <th><h3 align="left" style={style}>{url}</h3></th>
            <th><h3 align="left" style={style}>{url.methods}</h3></th>
          </tr>
    '''
    routes += "</thead></table>"
    return routes


api.add_resource(PeopleList, '/people')
api.add_resource(People, '/person/<name>')
api.add_resource(GroupList, '/groups')
api.add_resource(Group, '/group/<name>')
api.add_resource(UserRegister, '/register', '/register/<username>')

if "__main__" == __name__:
    app.run(host='0.0.0.0', port=5000)
