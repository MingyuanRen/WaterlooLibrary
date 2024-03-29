from flask import jsonify, request, abort, make_response
from sqlalchemy.sql import text
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import text, select

from app import app, db
from models import User

CORS(app)

# user module
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    with db.engine.connect() as connection:
        result = connection.execute("INSERT INTO Users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
                                    (data['name'], data['email'], data['phone'], hashed_password))
        
    return jsonify({'message': 'New user created!'})

@app.route('/api/userinfo/account', methods=['POST'])
def getAccountInfo():
    data = request.get_json()
    if "email" not in data:
        return make_response(jsonify({'error': 'No Email is passed in from body'}), 401)
    
    userInfo = None
    try:
        statement = select(User).where(User.email == data["email"])
        with db.engine.connect() as connection:
            result = connection.execute(statement).fetchone()
            userInfo = dict(result._mapping)
            if userInfo is None:
                raise Exception()
    
    except:
        return make_response(jsonify({'error': 'User Not found'}), 401)
    
    return jsonify(userInfo)

@app.route('/api/userinfo/bookstatus', methods=['POST'])
def getBooks():
    data = request.get_json()
    print(data)
    if "uid" not in data:
        return make_response(jsonify({'error': 'No Uid is passed in from body'}), 401)

    booksData = []
    try:
        statement = "SELECT title, author, DateBorrowed, DateDue FROM BorrowRecord r LEFT JOIN Books b ON r.ISBN = b.ISBN LEFT JOIN Users u ON u.uid = r.uid  WHERE u.uid = %s AND DateReturned IS NULL"
        with db.engine.connect() as connection:
            result = connection.execute(statement, (data["uid"],)).fetchall()
            print("hello world")
            for record in result:
                booksData.append(dict(record._mapping))
            print(booksData)
            if not booksData:
                raise Exception()

    except Exception as e:
        print(e)

    return jsonify(booksData)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    with db.engine.connect() as connection:
        result = connection.execute("SELECT * FROM Users WHERE email = %s", (data['email'], ))
        user = result.fetchone()

        if not user:
            return make_response(jsonify({'error': 'User does not exist'}), 401)

        if not check_password_hash(user['password'], data['password']):
            return make_response(jsonify({'error': 'Invalid password'}), 401)

        # Check if the user is an administrator
        admin_result = connection.execute("SELECT * FROM Administrators WHERE uid = %s", (user['uid'], ))
        admin = admin_result.fetchone()
        print("is Admin", admin)
        # If the user is an admin, return an additional attribute in the response
        if admin:
            return jsonify({'message': 'Login successful!', 'is_admin': True})
        else:
            return jsonify({'message': 'Login successful!', 'is_admin': False})

@app.route('/user', methods=['GET'])
def get_user():
    email = request.args.get('email')
    
    with db.engine.connect() as connection:
        result = connection.execute(text("SELECT name, email, phone, uid FROM Users WHERE email = :email"), {'email': email})

    user = result.fetchone()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'name': user[0], 'email': user[1], 'phone': user[2], 'uid': user[3]})

# Book module
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    with db.engine.connect() as connection:
        result = connection.execute("INSERT INTO Books (ISBN, title, author, year_of_publication, publisher, genre, inventory, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                    (data['isbn'], data['title'], data['author'], data['year_of_publication'], data['publisher'], data['genre'], data['inventory'], data['price']))

    return jsonify({'message': 'New book added!'})

@app.route('/books/search', methods=['GET'])
def search_book():
    search_value = request.args.get('value')
    if not search_value:
        return jsonify({'message': 'You need to provide a search value'}), 400

    valid_search_params = ['title', 'author', 'isbn', 'genre']
    sql_query = "SELECT * FROM Books WHERE "

    for param in valid_search_params:
        sql_query += f"LOWER({param}) LIKE LOWER(" + "'%" + search_value + "%'" + ") OR "

    # Remove the trailing 'OR ' from the query
    sql_query = sql_query[:-3]

    with db.engine.connect() as connection:
        result = connection.execute(text(sql_query))
        columns = ["isbn", "title", "author", "year_of_publication", "publisher", "genre", "inventory", "price"]
        books = [dict(zip(columns, row)) for row in result.fetchall()]
        print(books)
    if not books:
        return jsonify({'message': 'No books found'}), 404

    return jsonify(books)

@app.route('/books/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()

    if not data or 'uid' not in data or 'isbn' not in data:
        return jsonify({'message': 'You need to provide both user ID (uid) and ISBN of the book'}), 400

    uid = data['uid']
    isbn = data['isbn']

    with db.engine.connect() as connection:
        # Check if the book is available
        book = connection.execute(text("SELECT * FROM Books WHERE ISBN = :isbn"), {"isbn": isbn}).fetchone()
        inventory = 6
        if not book or book[inventory] <= 0:
            return jsonify({'message': 'This book is not available'}), 400

        # Decrease the book inventory
        connection.execute(text("UPDATE Books SET inventory = inventory - 1 WHERE ISBN = :isbn"), {"isbn": isbn})

        # Record the borrowing operation
        DateBorrowed = datetime.now()
        DateDue = DateBorrowed + timedelta(days=14)  # Assuming the book is due in two weeks
        borrow_record = {
            "uid": uid,
            "ISBN": isbn,
            "renewable": True,  # Assuming the book can be renewed
            "DateBorrowed": DateBorrowed,
            "DateDue": DateDue,
            "DateReturned": None  # Setting DateReturned to None initially
        }

