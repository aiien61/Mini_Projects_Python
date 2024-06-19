import uuid  # auto generate id serial number
import logging
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import stores

logging.basicConfig(level=logging.DEBUG)

blp = Blueprint('stores', __name__, description="Operations on stores")

@blp.route('/store/<string:store_id>')
class Store(MethodView):
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
    def get(self): return {'stores': list(stores.values())}
    
    def post(self):
        store_data = request.get_json()
        if 'name' not in store_data:
            abort(400, message="Bad request. Ensure 'name' is included in teh JSON payload.")

        for store in stores.values():
            if store_data['name'] == store['name']:
                abort(400, message='Store already exists.')
        store_id = uuid.uuid4().hex
        store = {**store_data, 'id': store_id}
        stores[store_id] = store
        return store, 201
