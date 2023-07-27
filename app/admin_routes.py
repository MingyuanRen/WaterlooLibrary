from flask import jsonify, request, abort, make_response
from sqlalchemy.sql import text
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import text, select

from app import app, db
from models import User

CORS(app)


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

        connection.commit()

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
