from flask_restful import Resource, reqparse
from models.user import UserModel
from sources.common import non_empty_value


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=non_empty_value,
        required=True,
        help="This field cannot be blank"
    )
    parser.add_argument(
        'password',
        type=non_empty_value,
        required=True,
        help="This field cannot be blank"
    )
    parser.add_argument(
        'group_id',
        type=non_empty_value,
        default=1,
        help="This field cannot be black",
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'], data['group_id'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

    def put(self):
        data = UserRegister.parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        if user:
            user.password = data['password']
            user.group_id = data['group_id']
        else:
            user = UserModel(**data)

        user.save_to_db()

        return user.json()

    def delete(self, username):
        user = UserModel.find_by_username(username)

        if user:
            user.delete_to_db()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404
