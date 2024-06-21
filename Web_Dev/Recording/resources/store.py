import uuid  # auto generate id serial number
import logging

from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema

logging.basicConfig(level=logging.DEBUG)

blp = Blueprint('stores', __name__, description="Operations on stores")

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id: str):
        try:
            return stores[store_id]
        except KeyError as e:
            logging.debug(e)
            abort(404, message='Store not found.')
    
    def delete(self, store_id: str):
        try:
            del stores[store_id]
            return {'message': "Store deleted."}
        except KeyError as e:
            logging.debug(e)
            abort(404, message='Store not found.')

@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self): return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data: dict):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError as e:
            logging.debug(e)
            abort(400, message='A store with that name already exists.')
        except SQLAlchemyError as e:
            logging.debug(e)
            abort(500, message='An error occurred while inserting the store.')

        return store
