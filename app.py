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
    """create a brand new cupcake from JSON request"""
    cupcake = Cupcake(flavor=request.json['flavor'], size=request.json['size'], rating=request.json['rating'], image=request.json['image'])
    db.session.add(cupcake)
    db.session.commit()
    json_response = jsonify(cupcake=cupcake.serialize())
    return (json_response, 201)

@app.route('/api/cupcakes/<int:id>', methods="PATCH")
def update_cupcake(id):
    """make changes to existing cupcake via API PATCH frequest"""
    cupcake = Cupcake.query.get_or_404(id)
    try:
        db.session.query(Cupcake).filter_by(id=id).update(request.json)
        print('------------------the fancy way he taught us')
    except:
        cupcake.flavor=request.json.get('flavor', todo.flavor)
        cupcake.rating=request.json.get('rating', todo.rating)
        cupcake.size=request.json.get('size', todo.size)
        cupcake.image=request.json.get('image', todo.image)
        print('------------------the safer way he taught us')

    # TODO: above looks like the thing that worked on the todos, but it's giving me 500
    # below did the same thing

    # cupcake.flavor=request.json['flavor'], cupcake.flavor
    # cupcake.rating=request.json['rating'], cupcake.rating
    # cupcake.size=request.json['size'], cupcake.size
    # cupcake.image=request.json['image'], cupcake.image
    # db.session.add(cupcake)
    # print('-------the way I suspect SQLAlchemy wants me to do it')
    
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """delete cupcake specified in API call from the database or return 404 if specification is invalid"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(deleted=id)
