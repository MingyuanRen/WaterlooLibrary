from flask import Flask
from flask_sqlalchemy import SQLAlchemy

####### if anyone want to have debug log comment back the following lines
# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
####### DEBUG END

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from routes import *
from models import *

if __name__ == "__main__":
    app.run(port=8000, debug=False)
