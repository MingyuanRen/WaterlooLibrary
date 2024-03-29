from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask import jsonify, request
from sqlalchemy.sql import text
from flask import abort
from flask import make_response
from flask_cors import CORS
from sqlalchemy import text, select

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zimablue@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'Users'

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(255), nullable=False)



# user module
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    with db.engine.connect() as connection:
        result = connection.execute(text("INSERT INTO Users ({name}, {email}, {phone}, {password}) VALUES (%s, %s, %s, %s)".format(
            name = data['name'], email = data['email'], phone = data['phone'], password = hashed_password)))
        
    return jsonify({'message': 'New user created!'})

##############################################################################################
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
            if userInfo == None: raise Exception()
    
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

##############################################################################################

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

# Get user info by email
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
        #result = connection.execute(text(sql_query), tuple(sql_values))
        columns = ["isbn", "title", "author", "year_of_publication",
                   "publisher", "genre", "inventory", "price"]
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
        DateBorrowed = datetime.now().date()
        # check if book is already reserved
        reserved = connection.execute(text("SELECT count(*) FROM Reservation WHERE uid = :uid AND ISBN = :isbn AND ExpireDate >= :today"), 
                                      {"uid": uid, "isbn": isbn, "today": DateBorrowed}).fetchone()
        
        if reserved and reserved[0] == 1:
            connection.execute(text("DELETE FROM Books WHERE uid = :uid AND ISBN = :isbn"), {"uid": uid, "isbn": isbn})
        else:
            book = connection.execute(text("SELECT * FROM Books WHERE ISBN = :isbn"), {"isbn": isbn}).fetchone()
            inventory = book[6]
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

        connection.execute(text("""
            INSERT INTO BorrowRecord (uid, ISBN, renewable, DateBorrowed, DateDue, DateReturned) 
            VALUES (:uid, :ISBN, :renewable, :DateBorrowed, :DateDue, :DateReturned)
        """), borrow_record)
    return jsonify({'message': 'Book borrowed successfully'})

@app.route('/books/reserve', methods=['POST'])
def reserve_book():
    data = request.get_json()

    if not data or 'uid' not in data or 'isbn' not in data:
        return jsonify({'message': 'You need to provide both user ID (uid) and ISBN of the book'}), 400

    uid = data['uid']
    isbn = data['isbn']

    with db.engine.connect() as connection:
        # Check if the book is available
        book = connection.execute(text("SELECT * FROM Books WHERE ISBN = :isbn"), {"isbn": isbn}).fetchone()
        inventory = 6
        if not book or book[6] <= 0:
            return jsonify({'message': 'This book is not available'}), 400
        
        # Check if user has reserved books < 5
        reserved = connection.execute(text("SELECT count(*) FROM Reservation WHERE uid = :uid AND ExpireDate >= :today"), {"uid": uid}).fetchone()
        if reserved and reserved[0] == 5:
            return jsonify({'message': 'You have reached the limit for reservation'}), 400

        # Record the borrowing operation
        DateBorrowed = datetime.now()
        ExpireDate = DateBorrowed + timedelta(days=5)  # Assuming the book is due in two weeks
        reservation_record = {
            "uid": uid,
            "ISBN": isbn,
            "DateReserved": DateBorrowed,
            "ExpireDate": ExpireDate,
        }

        connection.execute(text("""
            INSERT INTO Reservation (uid, ISBN, DateReserved, ExpireDate) 
            VALUES (:uid, :ISBN, :DateReserved, :ExpireDate)
        """), reservation_record)

    return jsonify({'message': 'Book reserved successfully'})

# Adminstrators
## return book
@app.route('/admin/return', methods=['POST'])
def return_book():
    data = request.get_json()
    # print(data)
    if not data or 'email' not in data or 'isbn' not in data:
        return jsonify({'message': 'You need to provide both user ID (uid) and ISBN of the book'}), 400

    email = data['email']
    isbn = data['isbn']
    # print("email: " + email)
    # print("isbn" + isbn)

    with db.engine.connect() as connection:
        # Check if the user has borrowed the book
        uid = connection.execute(text(
            """
            SELECT uid FROM Users
            WHERE email = '{email}'
            """.format(
                email = email
            )
        )).fetchone()
        if not uid:
            return jsonify({'message': 'User not found with provided email, please re-enter'}), 400
        uid = uid[0]

        borrow_record = connection.execute(text("""
            SELECT * FROM BorrowRecord 
            WHERE ISBN = '{isbn}' AND uid = {uid} AND DateReturned IS NULL
        """.format(isbn = isbn, uid = uid))).fetchone()

        if not borrow_record:
            return jsonify({'message': 'No record found of this user borrowing this book'}), 400

        # Update the record to show that the book has been returned
        DateReturned = datetime.now().date()
        # print("date: " + DateReturned)
        connection.execute(text("""
            UPDATE BorrowRecord 
            SET DateReturned = DATE '{DateReturned}'
            WHERE ISBN = '{isbn}' AND uid = {uid} AND DateReturned IS NULL
        """.format(DateReturned = DateReturned, isbn = isbn, uid = uid)))

        # Increase the book inventory
        connection.execute(text("UPDATE Books SET inventory = inventory + 1 WHERE ISBN = '{isbn}'".format(isbn = isbn)))
        
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

        # connection.commit()

    return jsonify({'message': 'Book added successfully'})

## View any user's information
@app.route('/admin/viewUserInfo', methods=['GET', 'POST'])
def viewUser():
    # print('get the function')
    data = request.get_json()
    print(data['email'])
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
        user_dict = {}
        user_cols = ['uid', 'name', 'email', 'phone', 'mid', 'points', 'start_date', 'end_date']
        for i in range(len(user_cols)):
            if user and user[i] is not None:
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

## update user's information
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
        # connection.commit()

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

            # connection.commit()
    return jsonify({'message': 'User info updated successfully'})


if __name__ == "__main__":
    app.run(port=8000, debug=True)
