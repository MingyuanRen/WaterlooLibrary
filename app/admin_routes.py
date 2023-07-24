from flask import jsonify, request, abort, make_response
from sqlalchemy.sql import text
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import text, select
from flask_mail import Mail, Message as MailMessage
from mailbox import Message

from app import app, db
from models import User


CORS(app)
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "waterloolibrary.group22@gmail.com"
app.config['MAIL_PASSWORD'] = "eprpsmfustpjjyxx"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


# Adminstrators
# return book
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
                email=email
            )
        )).fetchone()
        if not uid:
            return jsonify({'message': 'User not found with provided email, please re-enter'}), 400
        uid = uid[0]

        borrow_record = connection.execute(text("""
            SELECT * FROM BorrowRecord 
            WHERE ISBN = '{isbn}' AND uid = {uid} AND DateReturned IS NULL
        """.format(isbn=isbn, uid=uid))).fetchone()

        if not borrow_record:
            return jsonify({'message': 'No record found of this user borrowing this book'}), 400

        # Update the record to show that the book has been returned
        DateReturned = datetime.now().date()
        # print("date: " + DateReturned)
        connection.execute(text("""
            UPDATE BorrowRecord 
            SET DateReturned = DATE '{DateReturned}'
            WHERE ISBN = '{isbn}' AND uid = {uid} AND DateReturned IS NULL
        """.format(DateReturned=DateReturned, isbn=isbn, uid=uid)))

        # Increase the book inventory
        connection.execute(text(
            "UPDATE Books SET inventory = inventory + 1 WHERE ISBN = '{isbn}'".format(isbn=isbn)))

        connection.commit()

    return jsonify({'message': 'Book returned successfully'})

# Adding book


@app.route('/admin/addBook', methods=['POST'])
def AddBook():
    data = request.get_json()

    # if not data or 'uid' not in data or 'isbn' not in data:
    #     return jsonify({'message': 'You need to provide both user ID (uid) and ISBN of the book'}), 400

    # ISBN, title, author, year_of_publication, publisher, inventory, price
    isbn = data['isbn']
    title = data['title']
    author = data['author']
    year_of_publication = data['year_of_publication']
    publisher = data['publisher']
    inventory = data['inventory']
    price = data['price']

    # print(isbn)

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

# View any user's information


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
        user_dict = {}
        user_cols = ['uid', 'name', 'email', 'phone',
                     'mid', 'points', 'start_date', 'end_date']
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

# update user's information


@app.route('/admin/updateUserInfo', methods=['POST'])
def updateUser():
    data = request.get_json()
    # print(data)
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
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                uid=data['uid']
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
                    points=data['points'],
                    start_date=data['start_date'],
                    end_date=data['end_date'],
                    uid=data['uid']
                )
            ))

            connection.commit()
    return jsonify({'message': 'User info updated successfully'})

# Requests for administrator


@app.route('/admin/requests', methods=['GET'])
def get_requests():
    # Fetch the requests from the database and return them
    # data = request.get_json()
    # if not data:
    #     return jsonify(messag='Request not valid'), 400
    with db.engine.connect() as connection:
        result = connection.execute(text(
            """
            SELECT Users.uid, name, email, phone, reason 
            FROM Users
            INNER JOIN (SELECT uid, reason FROM AdminRequests) AS T
            WHERE Users.uid = T.uid
            """
        ))
        rows = result.fetchall()
        data = [{
            'uid': row[0],
            'name': row[1],
            'email': row[2],
            'phone': row[3],
            'reason': row[4]}
            for row in rows]
        # print(data)
    return jsonify(data)


@app.route('/admin/approveRequest', methods=['POST'])
def approve_request():
    # Approve the request and delete it from the database
    # print("this is approve request")
    data = request.get_json()
    uid = data['uid']
    # print(uid)

    with db.engine.connect() as connection:
        # upate Administrator table to contain the new admin
        connection.execute(text(
            """
            INSERT INTO Administrators (uid) VALUES ({uid});
            """.format(
                uid=uid
            )
        ))
        connection.commit()
        temp = connection.execute(text(
            """
            SELECT uid, reason FROM AdminRequests
            WHERE uid = {uid};
            """.format(
                uid = uid
            )
        ))
        temp = temp.fetchone();
        # update adminRqeusts table to delete the request
        connection.execute(text(
            """
            DELETE FROM AdminRequests
            WHERE uid = {uid};
            """.format(
                uid=uid
            )
        ))
        connection.commit()

        # sending out the email
    mail_message = MailMessage(
        'Administrator Application',
        sender='waterloolibrary.group22@gmail.com',
        recipients=[data['email']],
    )
    mail_message.body = 'Congrats! You\'ve become a library administrator!'
    # print("after the message is set")
    try:
        mail.send(mail_message)
        print("mail sent")
    except:
        with db.engine.connect() as connection:
            connection.execute(text(
                """
                INSERT INTO AdminRequedsts(uid, reason)
                VALUES({uid}, {reason});
                DELETE FROM Administrators
                WHERE uid = {uid};
                """.format(
                    uid = temp[0],
                    reason = temp[1],
                )
            ))
        return jsonify({'message': 'fail'})

    return jsonify({'message': 'success'})


@app.route('/admin/disapproveRequest', methods=['POST'])
def disapprove_request():
    # Delete the request from the database without approving it
    # print("this is disapprove requests")
    data = request.get_json()
    uid = data['uid']

    with db.engine.connect() as connection:
        temp = connection.execute(text(
            """
            SELECT uid, reason FROM AdminRequests
            WHERE uid = {uid};
            """.format(
                uid = uid
            )
        ))
        temp = temp.fetchone();
        connection.execute(text(
            """
            DELETE FROM AdminRequests
            WHERE uid = {uid};
            """.format(
                uid=uid
            )
        ))
        connection.commit()
    
    mail_message = MailMessage(
        'Administrator Application',
        sender='waterloolibrary.group22@gmail.com',
        recipients=[data['email']],
    )
    mail_message.body = """
        Thanks for your application! 
        Unfortunately, you are not selected as an adminstrator this time.
        We will keep your application for further opportunities.
    """
    # print("after the message is set")
    try:
        mail.send(mail_message)
        print("mail sent")
    except:
        with db.engine.connect() as connection:
            connection.execute(text(
                """
                INSERT INTO AdminRequedsts(uid, reason)
                VALUES({uid}, {reason});
                """.format(
                    uid = temp[0],
                    reason = temp[1],
                )
            ))
        return jsonify({'message': 'fail'})

    return jsonify({'message': 'success'})


@app.route('/admin/requestsCount', methods=['GET'])
def get_requests_count():
    # Return the number of pending requests
    # print("this is get count")
    with db.engine.connect() as connection:
        # update adminRqeusts table to delete the request
        result = connection.execute(text(
            """
            SELECT COUNT(*) FROM AdminRequests
            """
        ))
        request_num = result.fetchall()[0][0]
        print(request_num)

    return jsonify({'request_num': request_num})
