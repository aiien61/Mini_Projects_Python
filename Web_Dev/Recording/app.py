from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        'name': 'My Store',
        'items': [
            {
                'name': 'Chair',
                'price': 15.99
            }
        ]
    }
]


@app.get('/store')  # http://127.0.0.1:5000/store
def get_all_store():
    return {'stores': stores}


@app.post('/store')
def create_store():
    request_data = request.get_json()
    new_store = {'name': request_data['name'], 'items':[]}
    stores.append(new_store)
    return new_store, 201


@app.post('/store/<string:name>/item')
def create_item(name: str):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {'name': request_data['name'], 'price': request_data['price']}
            store['items'].append(new_item)
            return new_item
    return {'message': f'Store({name}) not found'}, 404

@app.get('/store/<string:name>')
def get_store(name: str):
    for store in stores:
        if store['name'] == name:
            return store
    return {'message': f'Store({name}) not found'}, 404


@app.get('/store/<string:name>/item')
def get_item_in_store(name: str):
    for store in stores:
        if store['name'] == name:
            return {'items': store['items']}
    return {'message': f'Store({name}) not found'}, 404
