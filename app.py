from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models import db, User, Book
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zimablue@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all() # Creates tables 


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(
        UserName=data['name'],
        Email=data['email'],
        PhoneNumber=data['phone_number'],
        Password=hashed_password,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(Email=data['email']).first()
    if not user or not check_password_hash(user.Password, data['password']):
        return jsonify({'message': 'Invalid username or password'})
    return jsonify({'message': 'Login successful!'})

# Book module
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    new_book = Book(
        Title=data['title'],
        Author=data['author'],
        Genre=data['genre'],
        ISBN=data['isbn'],
        PublicationDate=data['publication_date'],
        AvailabilityStatus='Available'
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'New book added!'})

@app.route('/books/<int:book_id>/borrow', methods=['POST'])
def borrow_book(book_id):
    book = Book.query.get(book_id)

    if book:
        if book.AvailabilityStatus == 'Available':
            book.AvailabilityStatus = 'Checked Out'
            db.session.commit()
            return jsonify({'message': 'Book borrowed successfully'})
        else:
            return jsonify({'message': 'Book is not available for borrowing'})
    else:
        return jsonify({'message': 'Book not found'})

@app.route('/books/<int:book_id>/return', methods=['POST'])
def return_book(book_id):
    book = Book.query.get(book_id)

    if book:
        if book.AvailabilityStatus == 'Checked Out':
            book.AvailabilityStatus = 'Available'
            db.session.commit()
            return jsonify({'message': 'Book returned successfully'})
        else:
            return jsonify({'message': 'Book is not checked out'})
    else:
        return jsonify({'message': 'Book not found'})

if __name__ == "__main__":
    app.run(port=8000, debug=True)