from db import db

#db.Model is going to tell SQLalchemy that ItemModel is going to be used by it
class ItemModel(db.Model):
    # Telling SQLAlchemy about our db details where these models data will be stored
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name":self.name,"price":self.price}
    
    @classmethod
    def find_by_name(cls, name):
        #connection = sqlite3.connect("database.db")
        #cursor = connection.cursor()
        #query = "SELECT * FROM items WHERE name=?"
        #result = cursor.execute(query, (name,))
        #row = result.fetchone()
        #connection.close()
        #if row:
        #    return cls(*row)
        ## The above entire thing can be replaced by one line in SQLAlchemy
        return ItemModel.query.filter_by(name=name).first() #Here <qury> is coming from <db.Model>

    
    def save_to_db(self):

        #Insert new item into database
        # connection = sqlite3.connect("database.db")
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()
        db.session.add(self)
        db.session.commit()

    
    def delete_from_db(self):
        #Update an item into database
        # connection = sqlite3.connect("database.db")
        # cursor = connection.cursor()
        # query = "UPDATE items SET price=? WHERE name=?"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()
        db.session.delete(self)
        db.session.commit()