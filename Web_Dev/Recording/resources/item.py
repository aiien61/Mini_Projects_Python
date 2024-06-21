import uuid  # auto generate id serial number
import logging

from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
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
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            logging.debug(e)
            abort(500, message='An error occurred while inserting the item.')

        return item
