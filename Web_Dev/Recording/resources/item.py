import uuid  # auto generate id serial number
import logging

from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from db import items,stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint('Items', __name__, description='Operations on items')

@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
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

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_id: str, item_data: dict):
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
    @blp.response(200, ItemSchema(many=True))
    def get(self): return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data: dict):
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