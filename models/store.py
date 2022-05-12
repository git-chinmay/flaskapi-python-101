from db import db

#db.Model is going to tell SQLalchemy that ItemModel is going to be used by it
class StoreModel(db.Model):
    # Telling SQLAlchemy about our db details where these models data will be stored
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    #The reason using lazy is to tell SQLALchemy not to create itemobjects for each item tied to store id
    #which is bad performance in case huge item list
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        #when use lazy='dynamic self.items no longer a list instead its now a query builder so all() to fetch everything
        return {"name":self.name,"items":[item.json() for item in self.items.all()]}
    
    @classmethod
    def find_by_store_name(cls, name):
        return StoreModel.query.filter_by(name=name).first()

    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()