# Waterloo Library Management System

This project is a database-driven application for managing a library. It uses MySQL as the database, Flask as the back-end server, and React for the front-end user interface.

## Prerequisites

You need to have the following installed:

- Python 3.8 or newer
- MySQL Server 8.0 or newer
- React and npm

## Setting Up the Database

1. Start the MySQL server on your machine.

2. Open MySQL Workbench (or connect to your MySQL server through the terminal) and run the following commands to create the necessary tables for the application:


## Setting Up the Flask Server, Create and Load database to Flask 

To connect Flask to MySQL, we use an ORM (Object-Relational Mapper) like SQLAlchemy along with a connection library like PyMySQL. 
This will allow Flask application to interact with MySQL database using Python code.

1.Install the necessary Python packages:

```bash
  pip install flask flask_sqlalchemy flask_cors pymysql
```

2.Run the Flask server:

```bash
  export FLASK_APP=app.py  # On Windows use `set FLASK_APP=app.py`
  flask run
```
3. Flask application to connect to MySQL with something like this:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```
4.  In Flask representing tables in the database:
For Example:
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return '<User %r>' % self.name
```
And if you want to create a new user:
```python
@app.route('/create_user')
def create_user():
    new_user = User(name='John', email='john@example.com')
    db.session.add(new_user)
    db.session.commit()
    return 'New user has been created.'
```
Insert sample data:
```python
    new_user = User(name='John', email='john@example.com')
    db.session.add(new_user)
    db.session.commit()
    return 'New user has been created.'
```

5. SQL SCHEMA
```sql
CREATE DATABASE LibraryDB;

USE LibraryDB;

CREATE TABLE Books (
    BookID INT PRIMARY KEY,
    Title VARCHAR(255),
    Author VARCHAR(255),
    Genre VARCHAR(255),
    ISBN VARCHAR(13),
    PublicationDate DATE,
    AvailabilityStatus ENUM('Available', 'Checked Out', 'Reserved')
);

CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255),
    PhoneNumber VARCHAR(15),
    Status ENUM('Active', 'Inactive')
);

CREATE TABLE BorrowingRecords (
    RecordID INT PRIMARY KEY,
    UserID INT,
    BookID INT,
    DateBorrowed DATE,
    DueDate DATE,
    DateReturned DATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
);

CREATE TABLE Reservations (
    ReservationID INT PRIMARY KEY,
    UserID INT,
    BookID INT,
    DateReserved DATE,
    ExpirationDate DATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
);

CREATE TABLE Fines (
    FineID INT PRIMARY KEY,
    UserID INT,
    Amount DECIMAL(8, 2),
    DatePaid DATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
