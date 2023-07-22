from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Pet(db.Model):
    '''A model for an entry in our pets table'''
    __tablename__ = "pets"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String(30),
                        nullable=False)
    species = db.Column(db.String(30),
                        nullable=False)
    photo_url = db.Column(db.String(400))

    age = db.Column(db.Integer)

    notes = db.Column(db.String(400))
    available = db.Column(db.Boolean, 
                            nullable=False,
                            default=True)

    def __init__(self, **kwargs):
        #Exclude the 'csrf_token' key from the kwargs
        kwargs.pop('csrf_token', None)
        super().__init__(**kwargs)