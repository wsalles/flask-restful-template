from sources.db import db


class PeopleModel(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    role = db.Column(db.String(80))
    email = db.Column(db.String(80))

    career_id = db.Column(db.Integer, db.ForeignKey('careers.id'))
    careers = db.relationship('CareerModel')

    def __init__(self, name, role, email, career_id):
        self.name = name
        self.role = role
        self.email = email
        self.career_id = career_id

    def json(self):
        return {'name': self.name, 'role': self.role, 'email': self.email}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
