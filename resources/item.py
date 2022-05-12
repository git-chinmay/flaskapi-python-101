from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel

#Create a item resource
class Item(Resource):

    # The Parser now belongs to the Item class not to any specific method
    # Parsing <price> field while sending
    parser = reqparse.RequestParser()    
    parser.add_argument(
        'price',
        type = float,
        required = True,
        help = "This field can not be left blank."
    )

    parser.add_argument(
        'store_id',
        type = int,
        required = True,
        help = "Every item must have a store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() #bcz now its no more retunring dictionary, instead its an object now
        return {"message":"Item does not exist."}, 404

    def post(self, name):

        #Return a message if an item already exist
        if ItemModel.find_by_name(name):
            return {"message": f"The item {name} already exists."}, 400

      
        request_data = Item.parser.parse_args()
        #new_item = ItemModel(name, request_data['price'], request_data['store_id']) or
        new_item = ItemModel(name, **request_data)
        
        #Insert new data into database
        try:
            new_item.save_to_db()
        except:
            return {"message":"An error occured while inserting an item."}, 500 #internal server error


        return new_item.json(), 201 #201 code for successfull creation, 202= accepted, 200= server response is ok

    #we can put jwt auth here
    def delete(self, name):
        #Delete an iteam from database
        # connection = sqlite3.connect("database.db")
        # cursor = connection.cursor()
        # query = "DELETE FROM items where name=?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        # return f"Item {name} deleted."

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return f"Item {name} deleted."

    #we can put jwt auth here
    def put(self, name):
        data = Item.parser.parse_args()  
        item = ItemModel.find_by_name(name)
        #updated_item = ItemModel(name, data['price'])

        if item:
            item.price = data['price']
        else:
            #item = ItemModel(name, data['price'], data['store_id']) or
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        # items = []
        # connection = sqlite3.connect("database.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # for item in result:
        #     items.append({"name":item[0], "price":item[1]})
        # connection.close()
        #Replacing with SQLAlchemy

        return {"items":[item.json() for item in ItemModel.query.all()]}
