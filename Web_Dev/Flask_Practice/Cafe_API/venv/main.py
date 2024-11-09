from flask import Flask, jsonify, render_template, request
import werkzeug.exceptions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from typing import Set
import werkzeug
import random

'''
On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record
@app.route("/random", methods=['GET'])
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())

@app.route("/all", methods=['GET'])
def get_all_cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

@app.route("/search", methods=["GET"])
def search_cafe():
    location = request.args.get('loc')
    result = db.session.execute(db.select(Cafe).where(Cafe.location == location))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404

# HTTP POST - Create Record
@app.route('/add', methods=['POST'])
def add_new_cafe():
    boolean_fields: Set[str] = {'has_toilet', 'has_wifi', 'has_sockets', 'can_take_calls'}

    def str_to_boolean(value: str) -> bool:
        if value.lower() in {'yes', 'y', 'true', 't', '1'}:
            return True
        elif value.lower() in {'no', 'n', 'false', 'f', '0'}:
            return False
        else:
            return ValueError(f"{value} is not supported in boolean fields.")

    try:
        if request.method == 'POST':
            all_args = request.args.to_dict()
            for arg, value in all_args.items():
                if arg in boolean_fields:
                    all_args[arg] = str_to_boolean(value)
            new_cafe = Cafe(**all_args)
            db.session.add(new_cafe)
            db.session.commit()
    except Exception as e:
        return jsonify(error={'message': str(e)})
    else:
        return jsonify(response={'success': 'Successfully added the new cafe.'})

# HTTP PUT/PATCH - Update Record
@app.route('/update-price/<cafe_id>', methods=['PATCH'])
def update_price(cafe_id: int):
    try:
        cafe_to_update = db.get_or_404(Cafe, cafe_id)
        new_price = request.args.get('new_price')
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify({'success': 'Successfuly updated the price.'}), 200
    except werkzeug.exceptions.NotFound as e:
        # print(type(e))
        return jsonify(error={'Not Found': 'Sorry the cafe with that id was not found in the database.'}), 404


# HTTP DELETE - Delete Record
@app.route('/report-closed/<cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id: int):
    api_key: str = request.args.get('api_key')
    if api_key != 'TopSecretAPIKey':
        return jsonify(error={'Forbidden': "Sorry, that's not allowed. Make sure you have the correct api_key."}), 404
    
    try:
        cafe_to_delete = db.get_or_404(Cafe, cafe_id)
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(response={'success': "Successfully deleted the cafe."}), 200
    except werkzeug.exceptions.NotFound as e:
        return jsonify(error={'Not Found': 'Sorry the cafe with that id was not found in the database.'}), 404


if __name__ == '__main__':
    app.run(debug=True)
