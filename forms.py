from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Optional, NumberRange, URL, AnyOf

class AddPetForm(FlaskForm):
    '''Form for adding a new pet'''

    valid_species = ["cat", "dog", "porcupine", "lizard", "bird"]
    name = StringField("Pet Name",
                        validators=[InputRequired()])
    
    species = StringField("Species",
                        validators=[InputRequired(), AnyOf(values=valid_species)])
    photo_url = StringField("Photo URL",
                            validators=[Optional(), URL()])
    age = IntegerField("Age",
                        validators=[Optional(), NumberRange(min=0, max=30)])
    notes = TextAreaField("Notes",
                            validators=[Optional()])

class EditPetForm(FlaskForm):
    '''Form for editing info on a pet'''
    photo_url = StringField("Photo URL",
                            validators=[Optional(), URL()])
    notes = TextAreaField("Notes",
                            validators=[Optional()])
    available = BooleanField("Available")
