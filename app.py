from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask import jsonify, request
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:458i*488P@localhost:3306/library'
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


# Adminstrators
## return book
@app.route('/admin/return', methods=['POST'])
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
        
        connection.commit()

    return jsonify({'message': 'Book returned successfully'})

## Adding book
@app.route('/admin/addBook', methods=['POST'])
def AddBook():
    data = request.get_json()

    # if not data or 'uid' not in data or 'isbn' not in data:
    #     return jsonify({'message': 'You need to provide both user ID (uid) and ISBN of the book'}), 400
    
    #ISBN, title, author, year_of_publication, publisher, inventory, price
    isbn = data['isbn']
    title = data['title']
    author = data['author']
    year_of_publication = data['year_of_publication']
    publisher = data['publisher']
    inventory = data['inventory']
    price = data['price']

    print(isbn)

    with db.engine.connect() as connection:
        # Insert the new book into BOOKS table
        connection.execute(text(
            """
            INSERT INTO Books (ISBN, title, author, year_of_publication, publisher, inventory, price)
            SELECT "{ISBN}", "{title}", "{author}", DATE "{year_of_publication}-01-01", "{publisher}", {inventory}, {price}
            WHERE NOT EXISTS (SELECT * FROM Books WHERE ISBN = '{ISBN}');
            """.format(
                ISBN=isbn,
                title=title,
                author=author,
                year_of_publication=year_of_publication,
                publisher=publisher,
                inventory=inventory,
                price=price
            )
        ))

        connection.commit()

    return jsonify({'message': 'Book added successfully'})

## View any user's information
@app.route('/admin/viewUserInfo', methods=['GET', 'POST'])
def viewUser():
    # print('get the function')
    data = request.get_json()
    # print(data['email'])
    with db.engine.connect() as connection:
        result = connection.execute(text(
            """
            SELECT Users.uid, name, email, phone, mid, points, start_date, end_date
            FROM Users
            LEFT OUTER JOIN MemberUsers ON Users.uid = MemberUsers.uid
            WHERE email = '{email}'
            """.format(email=data['email'])
            ))
        user = result.fetchone()
        print(user)
        user_dict = {}
        user_cols = ['uid', 'name', 'email', 'phone', 'mid', 'points', 'start_date', 'end_date']
        for i in range(len(user_cols)):
            if user[i] is not None:
                if user_cols[i] == 'start_date' or user_cols[i] == 'end_date':
                    user_dict[user_cols[i]] = user[i].strftime('%Y-%m-%d')
                else:
                    user_dict[user_cols[i]] = user[i]
        # print(user_dict)
        # if not user or not check_password_hash(user['password'], data['password']):
        #     return jsonify({'message': 'Invalid username or password'})
    if user:
        return jsonify(user_dict), 200
    else:
        return jsonify(message='User not found'), 404
    
@app.route('/admin/updateUserInfo', methods=['POST'])
def updateUser():
    data = request.get_json()
    print(data)
    for val in list(dict(data).values()):
        if not val:
            # print ("Some entry has None values")
            return jsonify(message='Cannot input empty attributes'), 400

    with db.engine.connect() as connection:
        # Insert the new book into BOOKS table
        connection.execute(text(
            """
            UPDATE Users
            SET name = '{name}', email = '{email}', phone = '{phone}'
            WHERE uid = {uid}
            """.format(
                name = data['name'],
                email = data['email'],
                phone = data['phone'],
                uid = data['uid']
            )
        ))
        connection.commit()

        if data.get('mid') is not None:
            connection.execute(text(
                """
                UPDATE MemberUsers
                SET points = {points}, start_date = DATE '{start_date}', end_date = DATE '{end_date}'
                WHERE uid = {uid}
                """.format(
                    points = data['points'],
                    start_date = data['start_date'],
                    end_date = data['end_date'],
                    uid = data['uid']
                )
            ))

            connection.commit()
    return jsonify({'message': 'User info updated successfully'})

if __name__ == "__main__":
    app.run(port=8000, debug=True)