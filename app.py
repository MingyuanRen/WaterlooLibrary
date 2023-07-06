from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask import jsonify, request
from sqlalchemy.sql import text
from flask import abort
from flask import make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zimablue@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# user module
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    with db.engine.connect() as connection:
        result = connection.execute("INSERT INTO Users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
                (data['name'], data['email'], data['phone'], hashed_password))
        
    return jsonify({'message': 'New user created!'})


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

    return jsonify({'message': 'Login successful!'})

# Get user info by email
@app.route('/user', methods=['GET'])
def get_user():
    email = request.args.get('email')
    
    with db.engine.connect() as connection:
        result = connection.execute(text("SELECT name, email, phone FROM Users WHERE email = :email"), {'email': email})

    user = result.fetchone()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'name': user[0], 'email': user[1], 'phone': user[2]})


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
    search_params = request.args

    if not search_params:
        return jsonify({'message': 'You need to provide at least one search parameter'}), 400

    valid_search_params = ['title', 'author', 'isbn', 'genre']
    sql_query = "SELECT * FROM Books WHERE "
    sql_values = []

    for param in search_params:
        if param not in valid_search_params:
            return jsonify({'message': f'Invalid search parameter: {param}. Must be one of {valid_search_params}'}), 400

        sql_query += f"LOWER({param}) LIKE LOWER(%s) AND "
        sql_values.append("%" + search_params[param] + "%")

    # Remove the trailing 'AND ' from the query
    sql_query = sql_query[:-4]

    with db.engine.connect() as connection:
        result = connection.execute(sql_query, tuple(sql_values))
        books = [dict(row) for row in result.fetchall()]

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
        if not book or book['inventory'] <= 0:
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

        connection.execute(text("""
            INSERT INTO BorrowRecord (uid, ISBN, renewable, DateBorrowed, DateDue, DateReturned) 
            VALUES (:uid, :ISBN, :renewable, :DateBorrowed, :DateDue, :DateReturned)
        """), borrow_record)

    return jsonify({'message': 'Book borrowed successfully'})

@app.route('/books/return', methods=['POST'])
def return_book():
    data = request.get_json()

    if not data or 'uid' not in data or 'isbn' not in data:
        return jsonify({'message': 'You need to provide both user ID (uid) and ISBN of the book'}), 400

    uid = data['uid']
    isbn = data['isbn']

    with db.engine.connect() as connection:
        # Check if the user has borrowed the book
        borrow_record = connection.execute(text("""
            SELECT * FROM BorrowRecord 
            WHERE ISBN = :isbn AND uid = :uid AND DateReturned IS NULL
        """), {"isbn": isbn, "uid": uid}).fetchone()

        if not borrow_record:
            return jsonify({'message': 'No record found of this user borrowing this book'}), 400

        # Update the record to show that the book has been returned
        DateReturned = datetime.now()
        connection.execute(text("""
            UPDATE BorrowRecord 
            SET DateReturned = :DateReturned
            WHERE ISBN = :isbn AND uid = :uid AND DateReturned IS NULL
        """), {"DateReturned": DateReturned, "isbn": isbn, "uid": uid})

        # Increase the book inventory
        connection.execute(text("UPDATE Books SET inventory = inventory + 1 WHERE ISBN = :isbn"), {"isbn": isbn})

    return jsonify({'message': 'Book returned successfully'})


if __name__ == "__main__":
    app.run(port=8000, debug=True)