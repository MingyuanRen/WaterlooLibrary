from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask import jsonify, request
from sqlalchemy.sql import text
from flask import abort
from flask import make_response
from flask_cors import CORS
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:458i*488P@localhost:3306/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def run_sample_sql():
    with db.engine.connect() as connection:
        result = connection.execute(text(
            """
            SELECT * FROM Users WHERE Email = 'example@gmail.com'
            """
        ))
        print("User Login:")
        for row in result:
            print(row)
        print()

        result = connection.execute(text(
            """
            SELECT * FROM Books WHERE title LIKE 'example book'
            """
        ))
        print("Search Book(Title):")
        for row in result:
            print(row)
        print()

        result = connection.execute(text(
            """
            SELECT * FROM Books WHERE ISBN LIKE '12345678'
            """
        ))
        print("Search Book(ISBN):")
        for row in result:
            print(row) 
        print()
        
        result = connection.execute(text(
            """
            SELECT points FROM MemberUsers WHERE uid = '11'
            """
        ))
        print("Check points (of current user):")
        for row in result:
            print(row) 
        print()

        result = connection.execute(text(
            """
            SELECT * FROM Gifts
            """
        ))
        print("Display gifts:")
        for row in result:
            print(row) 
        print()

        result = connection.execute(text(
            """
            SELECT * FROM Reservation WHERE uid = '1'
            """
        ))
        print("Display gifts:")
        for row in result:
            print(row) 
        print()

        result = connection.execute(text(
            """
            SELECT * FROM BorrowRecord WHERE uid = '1'
            """
        ))
        print("Check borrow record of current user:")
        for row in result:
            print(row) 
        print()

        result = connection.execute(text(
            """
            SELECT * FROM BorrowRecord WHERE ISBN = '12345678'
            """
        ))
        print("Check borrow record of a book:")
        for row in result:
            print(row) 
        print()
        # Borrow Books
        ## 1. check if user is member
        result = connection.execute(text(
            """
            SELECT * FROM MemberUsers
            WHERE uid = 1;
            """
        ))
        print("Check if user is member:")
        for row in result:
            print(row) 
        print()

        ## 2. check the limit for borrowed books per user:
        result = connection.execute(text(
            """
            SELECT count(*) FROM BorrowRecord
            WHERE uid = 1 AND DateReturned IS NULL;
            """
        ))
        print("Check the limit for borrowed books per user:")
        for row in result:
            print(row) 
        print()

        ## 3. Check if the book with sample_isbn is available
        result = connection.execute(text(
            """
            SELECT inventory FROM Books WHERE ISBN = "0002005018";
            """
        ))
        print("Check if the book with sample_isbn is available:")
        for row in result:
            print(row) 
        print()

        ## 4. If 3 returns an inventory greater than 1, then we will first update inventory
        result = connection.execute(text(
            """
            UPDATE Books SET inventory = inventory - 1
            WHERE ISBN = "0002005018";
            """
        ))
        print("If 3 returns an inventory greater than 1, then we will first update inventory:")
        for row in result:
            print(row) 
        print()
         
        ## 5. Insert into BookRecord table where
        result = connection.execute(text(
            """
            INSERT INTO BorrowRecord (uid, ISBN, renewable,
            DateBorrowed, DateDue, DateReturned)
            VALUES (1, "0002005018", 1, "2020-05-01", "2020-05-14", NULL);
            """
        ))
        print("Insert into BookRecord table where:")
        for row in result:
            print(row) 
        print()

        # Points Redemption related
        ## 1. Check if current user is a member
        result = connection.execute(text(
            """
            SELECT points FROM MemberUsers
            WHERE uid = 1;
            """
        ))
        print("Check if current user is a member:")
        for row in result:
            print(row) 
        print()

        ## 2. Check if current user has enough points and if ample_gift has inventory > 0
        result = connection.execute(text(
            """
            SELECT point_need, inventory FROM Gifts
            WHERE item = "pencil";  
            """
        ))
        print("Check if current user has enough points and if ample_gift has inventory > 0:")
        for row in result:
            print(row) 
        print()

        ## 3. Update inventory of sample_gift
        result = connection.execute(text(
            """
            UPDATE Gifts SET inventory = inventory - 1
            WHERE item = "pencil";
            """
        ))
        print("Update inventory of sample_gift:")
        for row in result:
            print(row) 
        print()

        ## 4. Update user points
        result = connection.execute(text(
            """
            INSERT INTO BorrowRecord (uid, ISBN, renewable,
            DateBorrowed, DateDue, DateReturned)
            VALUES (1, "0002005018", 1, "2020-05-01", "2020-05-14", NULL);
            """
        ))
        print("Update user points:")
        for row in result:
            print(row) 
        print()

        result = connection.execute(text(
            """
            INSERT INTO BorrowRecord (uid, ISBN, renewable,
            DateBorrowed, DateDue, DateReturned)
            VALUES (1, "0002005018", 1, "2020-05-01", "2020-05-14", NULL);
            """
        ))
        print("Insert into BookRecord table where:")
        for row in result:
            print(row) 
        print()


if __name__ == "__main__":
    with app.app_context():
        run_sample_sql()