from flask_restful import Resource
from models.group import GroupModel
from marshmallow import Schema, fields
from flask_apispec.views import MethodResource
from flask_apispec import doc, marshal_with


class GroupResponse(Schema):
    message = fields.String(required=True)
    name = fields.String(required=True)
    groups = fields.String(required=True)
    id = fields.String(required=False, dump_only=True)
    users = fields.String(required=False, dump_only=True)


class GroupRequest(Schema):
    name = fields.String(required=False, dump_only=True)


class Group(MethodResource, Resource):
    @doc(description='Here you can get information from a group.', tags=['Groups'])
    def get(self, name):
        group = GroupModel.find_by_name(name)
        if group:
            return group.json()
        return {'message': 'Group not found'}, 404

    @doc(description='Here you can create a group.', tags=['Groups'])
    @marshal_with(GroupResponse)
    def post(self, name):
        if GroupModel.find_by_name(name):
            return {'message': "A group with name '{}' already exists.".format(name)}, 400

        group = GroupModel(name)
        try:
            group.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {e}"}, 500

        return group.json(), 201

    @doc(description='Here you can delete a group.', tags=['Groups'])
    @marshal_with(GroupResponse)
    def delete(self, name):
        group = GroupModel.find_by_name(name)
        if group:
            group.delete_from_db()
            return {'message': 'Group deleted.'}
        return {'message': 'Group not found.'}, 404


class GroupList(MethodResource, Resource):
    @doc(description='Here you can get information from all group.', tags=['Groups'])
    def get(self):
        return {'groups': [x.json() for x in GroupModel.query.all()]}
