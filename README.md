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


## Setting Up the Flask, MySQL

To connect Flask to MySQL, we use an ORM (Object-Relational Mapper) like SQLAlchemy along with a connection library like PyMySQL. 
This will allow Flask application to interact with MySQL database using Python code.

1.Install the necessary Python packages:

```bash
  pip install flask flask_sqlalchemy flask_cors pymysql
```

2. Flask application to connect to MySQL with something like this:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```

3. SQL SCHEMA
```sql
CREATE DATABASE library;

USE library;

CREATE TABLE IF NOT EXISTS Users (
    uid INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(10) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Books(
    ISBN VARCHAR(13) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    year_of_publication DATE,
    publisher VARCHAR(255),
    genre VARCHAR(50),
    inventory INT NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS MemberUsers(
    uid INT NOT NULL,
    mID INT PRIMARY KEY AUTO_INCREMENT,
    points INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    INDEX (uid),
    FOREIGN KEY(uid) REFERENCES Users(uid)
);

CREATE TABLE IF NOT EXISTS Gifts(
    item VARCHAR(255) PRIMARY KEY,
    point_need INT NOT NULL,
    inventory INT NOT NULL
);

CREATE TABLE IF NOT EXISTS BorrowRecord(
    rid INT PRIMARY KEY AUTO_INCREMENT,
    uid INT NOT NULL REFERENCES Users(uid),
    ISBN VARCHAR(13) NOT NULL REFERENCES Books(ISBN),
    renewable BOOLEAN NOT NULL,
    DateBorrowed DATE NOT NULL,
    DateDue DATE NOT NULL,
    DateReturned DATE
);

CREATE TABLE IF NOT EXISTS Reservation(
    uid INT NOT NULL REFERENCES MemberUsers(uid),
    ISBN VARCHAR(13) NOT NULL REFERENCES Books(ISBN),
    DateReserved DATE NOT NULL,
    ExpireDate DATE NOT NULL,
    PRIMARY KEY(uid, ISBN)
);

CREATE TABLE IF NOT EXISTS Redemption(
    uid INT NOT NULL REFERENCES MemberUsers(uid),
    item VARCHAR(255) NOT NULL REFERENCES Gifts(item),
    date Date NOT NULL,
    PRIMARY KEY(uid, item)
);
```

## How to Create Database 
1. Create library schema in MySQL server or MySQL Workbench
2. Change config for local database  
 Change Database config to your local machine in create_tables.py file
 app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://yourdbname:yourdbpassword@localhost/library'

3. run the following command
```bash
  python3 create_tables.py
```

## How to Load Sample Data and Update Tables
1. Create library schema in MySQL server or MySQL Workbench
2. Change config for local database  
 Change Database config to your local machine in update_tables.py file
 app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://yourdbname:yourdbpassword@localhost/library'

3. Change the sample data in update_tables.py file
4. Run the following command
```bash
  python3 update_tables.py
```
5. Verify Data(Using MySQL)
```bash
  SELECT * FROM users;
```

## How to Run the Application
after you set up the config for Flask, React, MySQL and done creating your local database,
Run the Flask server:

```bash
  flask run --port 8000
```

Run the React Frontend:

```bash
  cd frontend
  npm start
```

## Current Design of the GUI (To be Updated)
MainPage: The Main Page for our WaterlooLibrary Application

Register and Login Page: A secured register and login system for users.

User Page: A page showing the infomation of specific user including personal info, borrow record, reservation record and redemption(for MemberUser).

Search Book Page: A page showing a list/table of books with details (like ISBN, title, author, year of publication, publisher, inventory, price)
Search bar to filter the list by different criteria (like title, author, ISBN).

Admin Page: A page for Administrators to manage user info, books inventory(add or return).

Issue and Return Management: A system for checking books in and out, and updating the status of the books.

Adding Books Page: A page for Administrators to add books.

Updating User Info Page: A page for updating user's Info like email, phone number(only accessible for admin).

Redemption Page (To be Updated): A page for Redemption.

Fine Management (To be Updated): A page to track these, issue reminders, and process payments.

Reservations (To be Updated): A page allowing users to reserve books that are currently borrowed by others.

## Current Features

1. MainPage
![MainPage](assets/mainpage.png "MainPage")

### User

2. Register User
![registerpage](assets/registerpage.png "Register Page")

3. Login User
![LoginPage](assets/LoginPage.png "Login Page")

3. User Page(After Register or Login)
![UserInfo](assets/UserInfo.png "User Info")
which also contains User Profile page

4. User's Borrow Records
![BorrowRecordsExample](assets/BorrowRecordsExample.jpg "Borrow Records")

### Book
5. Search Books
![bookSearchPage](assets/bookSearchPage.jpg "Book Search Page")

6. Book Search Result(In which Page You can Select your ideal Books)
![bookSearchResult](assets/bookSearchResult.jpg "Book Search Result")

7. Borrow and Reserve Books
![Borrow Book](assets/borrowBook.jpg "Borrow Book")

![Reserve Book](assets/reserveBook.jpg "Reserve Book")


Sending post request to http://localhost:8000/books and using json object as body:
```bash
    {
        "isbn": "978-3-16-148410-0",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year_of_publication": "1925",
        "publisher": "Charles Scribner's Sons",
        "genre": "Novel",
        "inventory": 10,
        "price": 15.99
    }
```
You should be able to see this, if boos has been successfully added:
```bash
    {
        "message": "New book added!"
    }
```

4. Seach Book
Sending Get request to http://localhost:8000/books/search?title=Great and using params { "title" : "Great" }
In this Example, the keyword for title "Great" is used, currently we support ['title', 'author', 'isbn', 'genre'] as keyword(you can use mutiple of these for search)

You should be able to see all the books with title contains Great
```bash
[
    {
        "ISBN": "9783161484100",
        "author": "F. Scott Fitzgerald",
        "genre": "Novel",
        "inventory": 10,
        "price": "15.99",
        "publisher": "Charles Scribner's Sons",
        "title": "The Great Gatsby",
        "year_of_publication": "Thu, 01 Jan 1925 00:00:00 GMT"
    },
    {
        "ISBN": "9783161484110",
        "author": "F. Scott Fitzgerald",
        "genre": "Novel",
        "inventory": 6,
        "price": "15.99",
        "publisher": "Charles Scribner's Sons",
        "title": "The Great Gatsby",
        "year_of_publication": "Thu, 01 Jan 1925 00:00:00 GMT"
    }
]
```

5. Borrow Books
Sending Post request to http://localhost:8000/books/borrow and and using json object as body:
Suppose you are number 1 user, and you want to borrow The Great Gatsby which has 9783161484110 as isbn
```bash
    {
        "uid": "1",
        "isbn": "9783161484110"
    }
```
You should be able to see this json object as return if you borrow this book successfully
```bash
    {
        'message': 'Book borrowed successfully'
    }
```

## Sample SQL
-- All the queries in the test-sample.sql are been given using actual examples

-- The actuall implementation of the queries in the application includes changes on the actual values 
