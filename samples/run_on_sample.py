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
        # result = connection.execute(text(
        #     """
        #     SELECT * FROM Users WHERE Email = 'example@gmail.com'
        #     """
        # ))
        # print("User Login:")
        # for row in result:
        #     print(row)
        # print()

        # result = connection.execute(text(
        #     """
        #     SELECT * FROM Books WHERE title LIKE 'example book'
        #     """
        # ))
        # print("Search Book(Title):")
        # for row in result:
        #     print(row)
        # print()

        # result = connection.execute(text(
        #     """
        #     SELECT * FROM Books WHERE ISBN LIKE '12345678'
        #     """
        # ))
        # print("Search Book(ISBN):")
        # for row in result:
        #     print(row) 
        # print()
        
        # result = connection.execute(text(
        #     """
        #     SELECT points FROM MemberUsers WHERE uid = '11'
        #     """
        # ))
        # print("Check points (of current user):")
        # for row in result:
        #     print(row) 
        # print()

        # result = connection.execute(text(
        #     """
        #     SELECT * FROM Gifts
        #     """
        # ))
        # print("Display gifts:")
        # for row in result:
        #     print(row) 
        # print()

        # result = connection.execute(text(
        #     """
        #     SELECT * FROM Reservation WHERE uid = '1'
        #     """
        # ))
        # print("Display gifts:")
        # for row in result:
        #     print(row) 
        # print()

        # result = connection.execute(text(
        #     """
        #     SELECT * FROM BorrowRecord WHERE uid = '1'
        #     """
        # ))
        # print("Check borrow record of current user:")
        # for row in result:
        #     print(row) 
        # print()

        # result = connection.execute(text(
        #     """
        #     SELECT * FROM BorrowRecord WHERE ISBN = '12345678'
        #     """
        # ))
        # print("Check borrow record of a book:")
        # for row in result:
        #     print(row) 
        # print()
        # # Borrow Books
        # ## 1. check if user is member
        # result = connection.execute(text(
        #     """
        #     SELECT * FROM MemberUsers
        #     WHERE uid = 1;
        #     """
        # ))
        # print("Check if user is member:")
        # for row in result:
        #     print(row) 
        # print()

        # ## 2. check the limit for borrowed books per user:
        # result = connection.execute(text(
        #     """
        #     SELECT count(*) FROM BorrowRecord
        #     WHERE uid = 1 AND DateReturned IS NULL;
        #     """
        # ))
        # print("Check the limit for borrowed books per user:")
        # for row in result:
        #     print(row) 
        # print()

        # ## 3. Check if the book with sample_isbn is available
        # result = connection.execute(text(
        #     """
        #     SELECT inventory FROM Books WHERE ISBN = "0002005018";
        #     """
        # ))
        # print("Check if the book with sample_isbn is available:")
        # for row in result:
        #     print(row) 
        # print()

        # ## 4. If 3 returns an inventory greater than 1, then we will first update inventory
        # result = connection.execute(text(
        #     """
        #     UPDATE Books SET inventory = inventory - 1
        #     WHERE ISBN = "0002005018";
        #     """
        # ))
        # connection.commit()
        # result = connection.execute(text(
        #     """
        #     SELECT * FROM Books WHERE ISBN = "0002005018";
        #     """
        # ))
        # print("If 3 returns an inventory greater than 1, then we will first update inventory:")
        # for row in result:
        #     print(row) 
        # print()
         
        # ## 5. Insert into BookRecord table where
        # result = connection.execute(text(
        #     """
        #     INSERT INTO BorrowRecord (uid, ISBN, renewable,
        #     DateBorrowed, DateDue, DateReturned)
        #     VALUES (1, "0002005018", 1, "2020-05-01", "2020-05-14", NULL);
        #     """
        # ))
        # connection.commit()
        # result = connection.execute(text(
        #     """
        #     SELECT * FROM BorrowRecord Where ISBN = "0002005018";
        #     """
        # ))
        # print("Insert into BookRecord table where:")
        # for row in result:
        #     print(row) 
        # print()

        # # Points Redemption related
        # ## 1. Check if current user is a member
        # result = connection.execute(text(
        #     """
        #     SELECT points FROM MemberUsers
        #     WHERE uid = 1;
        #     """
        # ))
        # print("Check if current user is a member:")
        # for row in result:
        #     print(row) 
        # print()

        # ## 2. Check if current user has enough points and if ample_gift has inventory > 0
        # result = connection.execute(text(
        #     """
        #     SELECT point_need, inventory FROM Gifts
        #     WHERE item = "pencil";  
        #     """
        # ))
        # print("Check if current user has enough points and if ample_gift has inventory > 0:")
        # for row in result:
        #     print(row) 
        # print()

        # ## 3. Update inventory of sample_gift
        # result = connection.execute(text(
        #     """
        #     UPDATE Gifts SET inventory = inventory - 1
        #     WHERE item = "pencil";
        #     """
        # ))
        # connection.commit()
        # result = connection.execute(text(
        #     """
        #     SELECT * FROM Gifts WHERE item = "pencil";
        #     """
        # ))
        # print("Update inventory of sample_gift:")
        # for row in result:
        #     print(row) 
        # print()

        # ## 4. Update user points
        # result = connection.execute(text(
        #     """
        #     UPDATE MemberUsers, gifts SET points = MemberUsers.points - gifts.point_need
        #     WHERE uid = 1 AND gifts.item = "pencil";
        #     """
        # ))
        # connection.commit()
        # result = connection.execute(text(
        #     """
        #     SELECT * FROM MemberUsers WHERE uid = 1;
        #     """
        # ))
        # print("Update user points:")
        # for row in result:
        #     print(row) 
        # print()

        # ## 5. Insert into Redemption where
        # result = connection.execute(text(
        #     """
        #     INSERT INTO Redemption
        #     VALUES (1, "pencil", "2020-01-01");
        #     """ 
        # ))
        # connection.commit()
        # result = connection.execute(text(
        #     """
        #     SELECT * FROM Redemption WHERE uid = 1;
        #     """ 
        # ))
        # print("Insert into Redemption where:")
        # for row in result:
        #     print(row) 
        # print()

        # # Points redemption:
        # ## 1. check if the return date of the book is already after the expected duedate
        # result = connection.execute(text(
        #     """
        #     SELECT DateDue FROM BorrowRecord
        #     WHERE ISBN = "0002005018";
        #     """ 
        # ))
        # print("check if the return date of the book is already after the expected duedate:")
        # for row in result:
        #     print(row) 
        # print()

        # ## 2. update the return date of that book to be today in the BorrowRecord table.
        # result = connection.execute(text(
        #     """
        #     UPDATE BorrowRecord SET DateReturned = "2020-05-10"
        #     WHERE uid = 1 AND ISBN = "0002005018";
        #     """ 
        # ))
        # connection.commit()
        # result = connection.execute(text(
        #     """
        #     SELECT * FROM BorrowRecord
        #     WHERE ISBN = "0002005018";
        #     """ 
        # ))
        # print("update the return date of that book to be today in the BorrowRecord table.:")
        # for row in result:
        #     print(row) 
        # print()

        # ## 3. check if current user is a member
        # result = connection.execute(text(
        #     """
        #     SELECT * FROM MemberUsers
        #     WHERE uid = 1;
        #     """ 
        # ))
        # print("check if current user is a member:")
        # for row in result:
        #     print(row) 
        # print()

        # ## 4. add points to membership account
        # result = connection.execute(text(
        #     """
        #     UPDATE MemberUsers SET points = points + 10
        #     WHERE uid = 1;
        #     """ 
        # ))
        # connection.commit()
        # result = connection.execute(text(
        #     """
        #     SELECT * FROM MemberUsers
        #     WHERE uid = 1;
        #     """ 
        # ))
        # print("add points to membership account:")
        # for row in result:
        #     print(row) 
        # print()


        # # User Registration and Login related
        # ## 1. Check if the user is already registered in the system
        # result = connection.execute(text(
        #     """
        #     SELECT email
        #     FROM Users
        #     WHERE email = 'sample@gmail.com';
        #     """ 
        # ))
        # connection.commit()
        # print("Check if the user is already registered in the system:")
        # for row in result:
        #     print(row) 
        # print()

        # ## 2. Registration
        # result = connection.execute(text(
        #     """
        #     INSERT INTO Users (name, email, phone, password)
        #     VALUES ("Tony", "tony@gmail.com", "1234567890", "password");   
        #     """ 
        # ))
        # connection.commit()
        # result = connection.execute(text(
        #     """ 
        #     SELECT * FROM Users WHERE name = 'Tony';   
        #     """ 
        # ))
        # print("Registration:")
        # for row in result:
        #     print(row) 
        # print()

        # Administrator related
        ## Adding Book
        result = connection.execute(text(
            """
            INSERT INTO Books (ISBN, title, author, year_of_publication, publisher, inventory, price)
            SELECT "00000", "example_book", "author", DATE "2020-01-01", "sample publisher", 10, 20.50
            WHERE NOT EXISTS (SELECT * FROM Books WHERE ISBN = '00000');    
            """ 
        ))
        connection.commit()
        result = connection.execute(text(
            """
            SELECT * FROM Books WHERE ISBN = '00000'
            """ 
        ))
        print("Adding Book:")
        for row in result:
            print(row) 
        print()

        ## Update User's info (uid is auto generated, so it cannot be changed)
        result = connection.execute(text(
            """
            UPDATE Users
            SET name = 'user_name', email = 'sample@email.com', phone = '1234567890'
            WHERE uid = 1
            """ 
        ))
        connection.commit()
        result = connection.execute(text(
            """
            SELECT * FROM Users WHERE uid = 1
            """ 
        ))
        print("Update User's info (uid is auto generated, so it cannot be changed):")
        for row in result:
            print(row) 
        print()


        ## Update member's info if the user is also a member
        result = connection.execute(text(
            """
            UPDATE MemberUsers
            SET points = 20000, start_date = DATE '2020-09-09', end_date = DATE '2023-10-03'
            WHERE uid = 1
            """ 
        ))
        connection.commit()
        result = connection.execute(text(
            """
            SELECT * FROM Users WHERE uid = 1
            """ 
        ))
        print("Update member's info if the user is also a member:")
        for row in result:
            print(row) 
        print()


if __name__ == "__main__":
    with app.app_context():
        run_sample_sql()