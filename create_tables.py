from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zimablue@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def create_tables():
    with db.engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS Users (
                uid INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                phone VARCHAR(10) NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        """))
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS Administrators (
                aid INT PRIMARY KEY AUTO_INCREMENT,
                uid INT REFERENCES Users(uid)
            );
        """))
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS Books(
                ISBN VARCHAR(13) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                year_of_publication DATE,
                publisher VARCHAR(255),
                genre VARCHAR(50),
                inventory INT NOT NULL,
                price DECIMAL(10,2) NOT NULL
            );
        """))

        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS MemberUsers(
                uid INT NOT NULL,
                mID INT PRIMARY KEY AUTO_INCREMENT,
                points INT NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                INDEX (uid),
                FOREIGN KEY(uid) REFERENCES Users(uid)
            );
        """))


        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS Gifts(
                item VARCHAR(255) PRIMARY KEY,
                point_need INT NOT NULL,
                inventory INT NOT NULL
            );
        """))

        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS BorrowRecord(
                rid INT PRIMARY KEY AUTO_INCREMENT,
                uid INT NOT NULL REFERENCES Users(uid),
                ISBN VARCHAR(13) NOT NULL REFERENCES Books(ISBN),
                renewable BOOLEAN NOT NULL,
                DateBorrowed DATE NOT NULL,
                DateDue DATE NOT NULL,
                DateReturned DATE
            );
        """))

        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS Reservation(
                uid INT NOT NULL REFERENCES MemberUsers(uid),
                ISBN VARCHAR(13) NOT NULL REFERENCES Books(ISBN),
                DateReserved DATE NOT NULL,
                ExpireDate DATE NOT NULL,
                PRIMARY KEY(uid, ISBN)
            );
        """))

        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS Redemption(
                uid INT NOT NULL REFERENCES MemberUsers(uid),
                item VARCHAR(255) NOT NULL REFERENCES Gifts(item),
                date Date NOT NULL,
                PRIMARY KEY(uid, item)
            );
        """))

if __name__ == "__main__":
    try:
        with app.app_context():
            create_tables()
    except Exception as e:
        print(str(e))

