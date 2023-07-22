from flask import Flask, render_template, redirect, request
from sqlalchemy import text 
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'My secret key'

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def show_homepage():
    '''Shows the homepage, where every pet in the DB is listed.''' 
    pets = Pet.query.all()
    return render_template("base.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    '''Handles both rendering the add_pet form and processing
    the data upon submit. Adds a new pet to the DB'''
    form = AddPetForm()
    if form.validate_on_submit():
        #Using **form.data to unpack the form data as keyword args 
        new_pet = Pet(**form.data)
        db.session.add(new_pet)
        db.session.commit()
        return redirect("/")
    else:
        return render_template('add_pet.html', form=form)

@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet_info(pet_id):
    '''Does one of 2 things: 1: Shows the pet info page for a specific pet.
                       2: Handles the processing of the edit_info form
                       on said page'''
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet) #Form is prefilled with pet's data, if present
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        return redirect("/")
    else:
        return render_template("pet_info.html", pet=pet, form=form)