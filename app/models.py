from . import db

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(128))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(8))

    def __init__(self, email, name, password, age, gender):
        self.email = email
        self.name = name
        self.password = password
        self.age = age
        self.gender = gender

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.email)
