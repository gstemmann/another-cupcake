from flask import Flask, request, redirect, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import Cupcake, db, connect_db
# from forms import AnimalForm
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolabar = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    all_cupcakes = [cupcake.serialize() for cupcake in  Cupcake.query.all()]
    return jsonify(all_cupcakes)


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    # new_cupcake = Cupcake(flavor=request.json['flavor'])
    data = request.json

    new_cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.to_dict())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake from data in request. Return updated data.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Delete cupcake and return confirmation message.

    Returns JSON of {message: "Deleted"}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")