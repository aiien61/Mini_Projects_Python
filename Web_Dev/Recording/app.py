import uuid
import logging
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.get('/store')  # http://127.0.0.1:5000/store
def get_all_store():
    return {'stores': list(stores.values())}


@app.post('/store')
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, 'id': store_id}
    stores[store_id] = store
    return store, 201


@app.post('/item')
def create_item(name: str):
    item_data = request.get_json()
    if item_data['store_id'] not in stores:
        return abort(404, message='Store not found')

    item_id = uuid.uuid4().hex
    item = {**item_data, 'id': item_id}
    items[item_id] = item

    return item, 201

@app.get('/item')
def get_all_items():
    return {'items': list(items.values())}


@app.get('/store/<string:name>')
def get_store(store_id: str):
    try:
        return stores[store_id]
    except KeyError as e:
        logging.debug(e)
        return abort(404, message='Store not found')


@app.get('/item/<string:item_id>')
def get_item(item_id: int):
    try:
        return items[item_id]
    except KeyError as e:
        logging.debug(e)
        return abort(404, message='Item not found')
