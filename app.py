from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zimablue@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# user module
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    with db.engine.connect() as connection:
        result = connection.execute("INSERT INTO users (UserName, Email, PhoneNumber, Password) VALUES (%s, %s, %s, %s)",
                (data['name'], data['email'], data['phone_number'], hashed_password))
        
    return jsonify({'message': 'New user created!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    with db.engine.connect() as connection:
        result = connection.execute("SELECT * FROM users WHERE Email = %s", (data['email'], ))
        user = result.fetchone()
        if not user or not check_password_hash(user['Password'], data['password']):
            return jsonify({'message': 'Invalid username or password'})
    return jsonify({'message': 'Login successful!'})

# Book module
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    with db.engine.connect() as connection:
        result = connection.execute("INSERT INTO books (Title, Author, Genre, ISBN, PublicationDate, AvailabilityStatus) VALUES (%s, %s, %s, %s, %s, 'Available')",
                (data['title'], data['author'], data['genre'], data['isbn'], data['publication_date']))

    return jsonify({'message': 'New book added!'})

@app.route('/books/<int:book_id>/borrow', methods=['POST'])
def borrow_book(book_id):
    with db.engine.connect() as connection:
        result = connection.execute("SELECT * FROM books WHERE BookID = %s", (book_id, ))
        book = result.fetchone()
        if book and book['AvailabilityStatus'] == 'Available':
            connection.execute("UPDATE books SET AvailabilityStatus = 'Checked Out' WHERE BookID = %s", (book_id, ))
            return jsonify({'message': 'Book borrowed successfully'})
        elif not book:
            return jsonify({'message': 'Book not found'})
        else:
            return jsonify({'message': 'Book is not available for borrowing'})

@app.route('/books/<int:book_id>/return', methods=['POST'])
def return_book(book_id):
    with db.engine.connect() as connection:
        result = connection.execute("SELECT * FROM books WHERE BookID = %s", (book_id, ))
        book = result.fetchone()
        if book and book['AvailabilityStatus'] == 'Checked Out':
            connection.execute("UPDATE books SET AvailabilityStatus = 'Available' WHERE BookID = %s", (book_id, ))
            return jsonify({'message': 'Book returned successfully'})
        elif not book:
            return jsonify({'message': 'Book not found'})
        else:
            return jsonify({'message': 'Book is not checked out'})

# return search
@app.route('/books/return/search', methods=['POST'])
def search_borrowed_books():
    keyword = request.json.get('keyword')
    with db.engine.connect() as connection:
        result = connection.execute("SELECT * FROM books WHERE Title LIKE %s AND AvailabilityStatus = 'Checked Out'", ('%' + keyword + '%',))
        books = result.fetchall()
        if not books:
            return jsonify({'message': 'No borrowed books found for the given keyword'})
        else:
            return jsonify({'books': [dict(book) for book in books]})


# borrow search
@app.route('/books/borrow/search', methods=['POST'])
def search_available_books():
    keyword = request.json.get('keyword')
    with db.engine.connect() as connection:
        result = connection.execute("SELECT * FROM books WHERE Title LIKE %s AND AvailabilityStatus = 'Available'", ('%' + keyword + '%',))
        books = result.fetchall()
        if not books:
            return jsonify({'message': 'No available books found for the given keyword'})
        else:
            return jsonify({'books': [dict(book) for book in books]})



if __name__ == "__main__":
    app.run(port=8000, debug=True)