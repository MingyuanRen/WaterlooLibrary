from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    PhoneNumber = db.Column(db.String(15), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Status = db.Column(db.String(10), nullable=False, default='Active')

class Book(db.Model):
    __tablename__ = 'books'

    BookID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255))
    Author = db.Column(db.String(255))
    Genre = db.Column(db.String(255))
    ISBN = db.Column(db.String(13))
    PublicationDate = db.Column(db.Date)
    AvailabilityStatus = db.Column(db.Enum('Available', 'Checked Out', 'Reserved'), default='Available')
