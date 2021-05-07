from flask_restful import Resource, reqparse
from models.people import PeopleModel
from sources.common import non_empty_value
from sources.settings import AUTHORIZATION_HEADERS
from marshmallow import Schema, fields
from flask_apispec.views import MethodResource
from flask_apispec import doc, use_kwargs, marshal_with
from flask_jwt_extended import jwt_required


class PeopleResponse(Schema):
    message = fields.Raw(required=True)


class PeopleRequest(Schema):
    name = fields.String(required=False, dump_only=True)
    role = fields.String(required=True)
    email = fields.String(required=True)


class People(MethodResource, Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'role',
        type=non_empty_value,
        required=True,
        help="Everyone should have a role."
    )
    parser.add_argument(
        'email',
        type=non_empty_value,
        required=True,
        help="Everyone needs an email."
    )

    @doc(description='Here you can get information from a person.', tags=['People'])
    def get(self, name):
        person = PeopleModel.find_by_name(name)
        if person:
            return person.json()
        return {'message': 'Person not found'}, 404

    @doc(description='Here you can create a person.', tags=['People'])
    @use_kwargs(PeopleRequest, location='json')
    @marshal_with(PeopleResponse)
    def post(self, name, **kwargs):
        if PeopleModel.find_by_name(name):
            return {'message': f"A person with name '{name}' already exists"}, 400

        data = People.parser.parse_args()

        person = PeopleModel(name, **data)

        try:
            person.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {e}"}, 500

        return person.json(), 201

    @doc(description='Here you can update a person.', tags=['People'], params=AUTHORIZATION_HEADERS)
    @use_kwargs(PeopleRequest, location='json')
    @marshal_with(PeopleResponse)
    @jwt_required()
    def put(self, name, **kwargs):
        data = People.parser.parse_args()

        person = PeopleModel.find_by_name(name)

        if person:
            person.role = data['role']
            person.email = data['email']
        else:
            person = PeopleModel(name, **data)

        person.save_to_db()

        return person.json(), 201

    @doc(description='Here you can delete a person.', tags=['People'], params=AUTHORIZATION_HEADERS)
    @marshal_with(PeopleResponse)
    @jwt_required()
    def delete(self, name):
        person = PeopleModel.find_by_name(name)
        if person:
            person.delete_from_db()
            return {'message': 'Person deleted.'}
        return {'message': 'Person not found.'}, 404


class PeopleList(MethodResource, Resource):
    @doc(description='Here you can get information from everyone.', tags=['People'])
    def get(self):
        return {'people': [x.json() for x in PeopleModel.find_all()]}, 200
