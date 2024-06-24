from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    """
    Make a plain item schema without involving any relative store info in order to keep item table 
    schema simple.
    """
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    """
    Make a plain store schema without involving any relative item info in order to keep store table 
    schema simple.
    """
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class ItemSchema(PlainItemSchema):
    """
    Make item schema nested with store. Inherit plain item schema to load item schema and define 
    store_id and store columns.
    """
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    """
    Make store schema nested with item. Inherit plain store schema to load store schema and define 
    column items.
    """
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))
