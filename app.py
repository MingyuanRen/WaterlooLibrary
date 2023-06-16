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
        result = connection.execute("INSERT INTO Users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
                (data['name'], data['email'], data['phone'], hashed_password))
        
    return jsonify({'message': 'New user created!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    with db.engine.connect() as connection:
        result = connection.execute("SELECT * FROM Users WHERE email = %s", (data['email'], ))
        user = result.fetchone()
        if not user or not check_password_hash(user['password'], data['password']):
            return jsonify({'message': 'Invalid username or password'})
    
    return jsonify({'message': 'Login successful!'})


# Book module
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    with db.engine.connect() as connection:
        result = connection.execute("INSERT INTO Books (ISBN, title, author, year_of_publication, publisher, genre, inventory, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (data['isbn'], data['title'], data['author'], data['year_of_publication'], data['publisher'], data['genre'], data['inventory'], data['price']))

    return jsonify({'message': 'New book added!'})


# @app.route('/books/<int:book_id>/borrow', methods=['POST'])
# def borrow_book(book_id):
#     with db.engine.connect() as connection:
#         result = connection.execute("SELECT * FROM books WHERE BookID = %s", (book_id, ))
#         book = result.fetchone()
#         if book and book['AvailabilityStatus'] == 'Available':
#             connection.execute("UPDATE books SET AvailabilityStatus = 'Checked Out' WHERE BookID = %s", (book_id, ))
#             return jsonify({'message': 'Book borrowed successfully'})
#         elif not book:
#             return jsonify({'message': 'Book not found'})
#         else:
#             return jsonify({'message': 'Book is not available for borrowing'})

# @app.route('/books/<int:book_id>/return', methods=['POST'])
# def return_book(book_id):
#     with db.engine.connect() as connection:
#         result = connection.execute("SELECT * FROM books WHERE BookID = %s", (book_id, ))
#         book = result.fetchone()
#         if book and book['AvailabilityStatus'] == 'Checked Out':
#             connection.execute("UPDATE books SET AvailabilityStatus = 'Available' WHERE BookID = %s", (book_id, ))
#             return jsonify({'message': 'Book returned successfully'})
#         elif not book:
#             return jsonify({'message': 'Book not found'})
#         else:
#             return jsonify({'message': 'Book is not checked out'})

# # return search
# @app.route('/books/return/search', methods=['POST'])
# def search_borrowed_books():
#     keyword = request.json.get('keyword')
#     with db.engine.connect() as connection:
#         result = connection.execute("SELECT * FROM books WHERE Title LIKE %s AND AvailabilityStatus = 'Checked Out'", ('%' + keyword + '%',))
#         books = result.fetchall()
#         if not books:
#             return jsonify({'message': 'No borrowed books found for the given keyword'})
#         else:
#             return jsonify({'books': [dict(book) for book in books]})


# # borrow search
# @app.route('/books/borrow/search', methods=['POST'])
# def search_available_books():
#     keyword = request.json.get('keyword')
#     with db.engine.connect() as connection:
#         result = connection.execute("SELECT * FROM books WHERE Title LIKE %s AND AvailabilityStatus = 'Available'", ('%' + keyword + '%',))
#         books = result.fetchall()
#         if not books:
#             return jsonify({'message': 'No available books found for the given keyword'})
#         else:
#             return jsonify({'books': [dict(book) for book in books]})

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
        books = result.fetchall()

    if not books:
        return jsonify({'message': 'No books found'}), 404

    return jsonify(books)



if __name__ == "__main__":
    app.run(port=8000, debug=True)