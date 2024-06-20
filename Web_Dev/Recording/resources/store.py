import uuid  # auto generate id serial number
import logging

from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from db import stores
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
        for store in stores.values():
            if store_data['name'] == store['name']:
                abort(400, message='Store already exists.')
        store_id = uuid.uuid4().hex
        store = {**store_data, 'id': store_id}
        stores[store_id] = store
        return store, 201
