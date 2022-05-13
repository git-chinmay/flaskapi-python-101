"""
To prevent error after deploying to Heroku as inside app.py we are using __name__ == "__main__"
It will not import db hence cause issues.
We also can not import from db import db on top with othere imports as it will cause circular error
Now change the uwsgi.ini to load the run file instead of app
"""
from db import db
from app import app
db.init_app(app) #Binding SQLAlchemy with our app

@app.before_first_request
def create_table():
    db.create_all()