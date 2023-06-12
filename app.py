from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zimablue@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    PhoneNumber = db.Column(db.String(20), nullable=False)
    Status = db.Column(db.Enum('Active', 'Inactive'), default='Active')

    def __init__(self, Name, Email, PhoneNumber, Status):
        self.Name = Name
        self.Email = Email
        self.PhoneNumber = PhoneNumber
        self.Status = Status

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = User(
        Name = data['name'],
        Email = data['email'],
        PhoneNumber = data['phone_number'],
        Status = 'Active'
    )

    db.session.add(new_user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(Email=data['email']).first()

    if user and bcrypt.check_password_hash(user.Password, data['password']):
        return {"message": "Logged in successfully"}, 200

    return {"message": "Invalid credentials"}, 400
