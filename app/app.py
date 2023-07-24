from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zimablue@localhost/library'
# if using docker volumn
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zimablue@db:3306/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from routes import *
from models import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)

