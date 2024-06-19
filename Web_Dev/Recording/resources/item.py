import uuid  # auto generate id serial number
import logging
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import items,stores

blp = Blueprint('Items', __name__, description='Operations on items')

@blp.route('/item/<string:item_id>')
class Item(MethodView):
    def get(self, item_id: str):
        try:
            return items[item_id]
        except KeyError as e:
            logging.debug(e)
            abort(404, message='Item not found.')

    def delete(self, item_id: str):
        try:
            del items[item_id]
            return {'message': "Item deleted."}
        except KeyError as e:
            logging.debug(e)
            abort(404, message='Item not found.')

    def put(self, item_id: str):
        item_data = request.get_json()
        if 'price' not in item_data or 'name' not in item_data:
            abort(400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload.")

        try:
            item: dict = items[item_id]
        except KeyError as e:
            logging.debug(e)
            abort(404, message='Item not found.')
        else:
            item |= item_data
            return item


@blp.route('/item')
class ItemList(MethodView):
    def get(self): return {'items': list(items.values())}

    def post(self):
        item_data = request.get_json()
        if (
            'price' not in item_data
            or 'store_id' not in item_data
            or 'name' not in item_data
        ):
            abort(
                400,
                message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload."
            )

        for item in items.values():
            if (
                item['name'] == item['name']
                and item_data['store_id'] == item['store_id']
            ):
                abort(400, message='Item already exists.')

        if item_data['store_id'] not in stores:
            abort(404, message='Store not found.')

        item_id = uuid.uuid4().hex
        item = {**item_data, 'id': item_id}
        items[item_id] = item

        return item
