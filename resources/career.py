from flask_restful import Resource
from models.career import CareerModel


class Career(Resource):
    def get(self, name):
        career = CareerModel.find_by_name(name)
        if career:
            return career.json()
        return {'message': 'Role not found'}, 404

    def post(self, name):
        if CareerModel.find_by_name(name):
            return {'message': "A role with name '{}' already exists.".format(name)}, 400

        career = CareerModel(name)
        try:
            career.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred: {e}"}, 500

        return career.json(), 201

    def delete(self, name):
        career = CareerModel.find_by_name(name)
        if career:
            career.delete_from_db()

        return {'message': 'Career deleted'}


class CareerList(Resource):
    def get(self):
        return {'careers': list(map(lambda x: x.json(), CareerModel.query.all()))}
