"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
# from forms import AddCupcakeForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "very_secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db (app)

@app.route('/')
def load_home_page():
    """ load home page """
    cupcakes = Cupcake.query.all()
    # form = AddCupcakeForm()
    # if form.validate_on_submit():
        # I just realized how weird this is going to be to mix with jQuery... I"m saving this for further learning
    return render_template('home.html', cupcakes=cupcakes)

################ api routes
@app.route('/api/cupcakes')
def return_all_cupcakes():
    """return info on all cupcakes in the database"""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:id>')
def single_cupcake_into(id):
    """return info on cupcake of designated ID, return 404 if there is no cupcake with that ID"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_new_cupcake():
    """create a brand new cupcake from JSON request"""
    cupcake = Cupcake(flavor=request.json['flavor'], size=request.json['size'], rating=request.json['rating'], image=request.json['image'])
    db.session.add(cupcake)
    db.session.commit()
    json_response = jsonify(cupcake=cupcake.serialize())
    return (json_response, 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """make changes to existing cupcake via API PATCH frequest"""
    cupcake = Cupcake.query.get_or_404(id)
    # I don't know if there's any validity to doing this try/except block. It seemed to me the "try" method would be faster on larger records so it might be worth trying it
    try:
        db.session.query(Cupcake).filter_by(id=id).update(request.json)
        print('------------------the fancy way he taught us')
    except:
        cupcake.flavor=request.json.get('flavor', cupcake.flavor)
        cupcake.rating=request.json.get('rating', cupcake.rating)
        cupcake.size=request.json.get('size', cupcake.size)
        cupcake.image=request.json.get('image', cupcake.image)
        print('------------------the safer way he taught us')

    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """delete cupcake specified in API call from the database or return 404 if specification is invalid"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(deleted=id)
