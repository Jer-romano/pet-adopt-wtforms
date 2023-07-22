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
    pets = Pet.query.all()
    return render_template("base.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        new_pet = Pet(name=name, species=species, photo_url=photo,
        age=age, notes=notes)
        db.session.add(new_pet)
        db.session.commit()
        return redirect("/")
    else:
        return render_template('add_pet.html', form=form)

@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet_info(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        return redirect("/")
    else:
        return render_template("pet_info.html", pet=pet, form=form)