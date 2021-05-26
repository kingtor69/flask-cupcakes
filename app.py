"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

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
    return render_template('home.html')

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

@app.route('/api/cupcakes', methods=['POST'])
def create_new_cupcake():

    cupcake = Cupcake(flavor=request.json['flavor'], size=request.json['size'], rating=request.json['rating'], image=request.json['image'])
    db.session.add(cupcake)
    db.session.commit()
    json_response = jsonify(cupcake=cupcake.serialize())
    return (json_response, 201)

