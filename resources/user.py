from models.user import UserModel
from sources.common import non_empty_value
from flask_restful import Resource, reqparse
from marshmallow import Schema, fields
from flask_apispec.views import MethodResource
from flask_apispec import doc, use_kwargs, marshal_with


class UserResponse(Schema):
    message = fields.String(required=True)
    username = fields.String(required=True)
    group_id = fields.String(required=True)


class UserRequest(Schema):
    username = fields.String(required=False, dump_only=True)
    password = fields.String(required=True, format='password')
    group_id = fields.String(required=True)


class UserRegister(MethodResource, Resource):
    parser = reqparse.RequestParser()
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

    @doc(description='Here you can create a user to generate a token.', tags=['UserRegister'])
    @use_kwargs(UserRequest, location='json')
    @marshal_with(UserResponse)
    def post(self, username, **kwargs):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(username):
            return {"message": "A user with that username already exists"}, 400

        try:
            user = UserModel(username, data['password'], data['group_id'])

        except Exception as e:
            return {"message": f"An error occurred: {e}"}, 500

        user.save_to_db()

        return {"message": "User created successfully."}, 201

    @doc(description='Here you can update a user to generate a token.', tags=['UserRegister'])
    @use_kwargs(UserRequest, location='json')
    @marshal_with(UserResponse)
    def put(self, username, **kwargs):
        data = UserRegister.parser.parse_args()

        user = UserModel.find_by_username(username)

        try:
            if user:
                user.password = data['password']
                user.group_id = data['group_id']
            else:
                user = UserModel(username, **data)
        except Exception as e:
            return {"message": f"An error occurred: {e}"}, 500

        user.save_to_db()

        return user.json()

    @doc(description='Here you can delete a user to generate a token.', tags=['UserRegister'])
    def delete(self, username):
        user = UserModel.find_by_username(username)

        if user:
            user.delete_to_db()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404
