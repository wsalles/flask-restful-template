from models.user import UserModel
from sources.common import non_empty_value
from sources.settings import BLACKLIST, AUTHORIZATION_HEADERS
from flask_restful import Resource, reqparse
from marshmallow import Schema, fields
from flask_apispec.views import MethodResource
from flask_apispec import doc, use_kwargs, marshal_with
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

parser = reqparse.RequestParser()
parser.add_argument(
    'username',
    type=non_empty_value,
    required=False,
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


class UserResponse(Schema):
    message = fields.Raw(required=True)
    username = fields.String(required=True)
    group_id = fields.String(required=True)
    access_token = fields.String(required=False)
    refresh_token = fields.String(required=False)


class UserRequest(Schema):
    username = fields.String(required=False, dump_only=True)
    password = fields.String(required=True, format='password')
    group_id = fields.String(required=True)


class UserAuthRequest(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True, format='password')


class UserRegister(MethodResource, Resource):
    @doc(description='Here you can create a user to generate a token.', tags=['Users'])
    @use_kwargs(UserRequest, location='json')
    @marshal_with(UserResponse)
    def post(self, username, **kwargs):
        data = parser.parse_args()

        if UserModel.find_by_username(username):
            return {"message": "A user with that username already exists"}, 400

        try:
            user = UserModel(username, data['password'], data['group_id'])

        except Exception as e:
            return {"message": f"An error occurred: {e}"}, 500

        user.save_to_db()

        return {"message": "User created successfully."}, 201

    @doc(description='Here you can update a user to generate a token.', tags=['Users'])
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

        return {"message": "User updated successfully."}, 201

    @doc(description='Here you can delete a user to generate a token.', tags=['Users'])
    @marshal_with(UserResponse)
    def delete(self, username):
        user = UserModel.find_by_username(username)

        if user:
            user.delete_from_db()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404


class User(MethodResource, Resource):
    @doc(description='Here you can get information from user.', tags=['Users'])
    def get(self, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @doc(description='Here you can deleted a user.', tags=['Users'])
    @marshal_with(UserResponse)
    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        user.delete_from_db()

        return {'message': 'User deleted'}, 200


class UserLogin(MethodResource, Resource):
    @doc(description='Here you can login passing the token in the header.', tags=['Users'])
    @use_kwargs(UserAuthRequest, location='json')
    @marshal_with(UserResponse)
    def post(self, **kwargs):
        data = parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200

        return {"message": "Invalid credentials. Please, try again"}, 401


class UserLogout(MethodResource, Resource):
    @jwt_required()
    @doc(description='Here you can logout passing the token in the header.', tags=['Users'],
         params=AUTHORIZATION_HEADERS)
    @use_kwargs(UserAuthRequest, location='json')
    @marshal_with(UserResponse)
    def post(self):
        token = get_jwt()['jti']
        BLACKLIST.add(token)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(MethodResource, Resource):
    @jwt_required(refresh=True)
    @doc(description='Here you can get the token refresh.', tags=['Users'], params=AUTHORIZATION_HEADERS)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
