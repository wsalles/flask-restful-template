from flask_restful import Resource, reqparse
from models.people import PeopleModel
from sources.common import non_empty_value


class People(Resource):
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

    def get(self, name):
        person = PeopleModel.find_by_name(name)
        if person:
            return person.json()
        return {'message': 'Person not found'}, 404

    def post(self, name):
        if PeopleModel.find_by_name(name):
            return {'message': f"A person with name '{name}' already exists"}, 400

        data = People.parser.parse_args()

        person = PeopleModel(name, **data)

        try:
            person.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {e}"}, 500

        return person.json(), 201

    def delete(self, name):
        person = PeopleModel.find_by_name(name)
        if person:
            person.delete_from_db()
            return {'message': 'Person deleted.'}
        return {'message': 'Person not found.'}, 404

    def put(self, name):
        data = People.parser.parse_args()

        person = PeopleModel.find_by_name(name)

        if person:
            person.role = data['role']
            person.email = data['email']
        else:
            person = PeopleModel(name, **data)

        person.save_to_db()

        return person.json()


class PeopleList(Resource):
    def get(self):
        return {'people': list(map(lambda x: x.json(), PeopleModel.query.all()))}
