from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_store_name(name)
        if store:
            return store.json()
        return {"message":f"Store {name} does not exist."}, 404

    def post(self,name):
        store = StoreModel.find_by_store_name(name)
        if store:
            return {"message":f"{name} already exist."}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message":"Error occured while creating the store."}, 500

        return store.json()

    def delete(self, name):
        store = StoreModel.find_by_store_name(name)
        if store:
            store.delete_from_db()
        return {"message":f"{name} deleted."}


class StoreLists(Resource):
    def get(self):
        return {"stores":[store.json() for store in StoreModel.query.all()]}