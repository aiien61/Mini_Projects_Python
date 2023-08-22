import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)

## Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


## Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    return jsonify(cafe=random.choice(all_cafes).to_dict())


@app.route("/all")
def get_all_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def get_cafe_by_location():
    location = request.args.get("loc").title()
    result = db.session.execute(db.select(Cafe).where(Cafe.location==location))
    all_cafes = result.scalars().all()
    if not all_cafes:
        not_found_message = "Sorry, we don't have cafe at that location."
        return jsonify(error={"Not found": not_found_message}), 404
    else:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def post_cafe():
    boolean_fields = {'has_toilet', 'has_wifi',
                      'has_sockets', 'can_take_calls'}

    def _str_to_bool(value: str):
        if value.lower() in {'t', 'true', 'y', 'yes', '1'}:
            return True
        elif value.lower() in {'f', 'false', 'n', 'no', '0'}:
            return False
        else:
            raise ValueError(f"'{value}' is not supported in boolean fields")
    try:
        all_args = request.args.to_dict()
        for name, value in all_args.items():
            if name in boolean_fields:
                all_args[name] = _str_to_bool(value)

        new_cafe = Cafe(**all_args)
        db.session.add(new_cafe)
        db.session.commit()
    except IntegrityError as err_msg:
        return jsonify(error={"fail": err_msg})
    else:
        return jsonify(response={"success": "Successfully added the new cafe"})


## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id: int):
    err_msg = {
        "400": {"Bad Request": "Sorry the provided price format is not correct."},
        "404": {"Not Found": "Sorry a cafe with that id was not found in the database."}
    }

    def validate_price_format(value: str):
        if value[0] not in {'£', '$'}:
            raise ValueError("400")
        
        if isinstance(float(value[1:]), float):
            return True
        else:
            raise ValueError("400")

    try:
        validate_price_format(request.args.get("new_price"))
        cafe_to_update = db.session.get(Cafe, cafe_id)
        if cafe_to_update:
            cafe_to_update.coffee_price = request.args.get("new_price")
            db.session.commit()
        else:
            raise ValueError("404")

    except ValueError as err_code:
        return jsonify(error=err_msg.get(str(err_code)))
    else:
        return jsonify(response={"success": "Successfully updated the price"})


## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
