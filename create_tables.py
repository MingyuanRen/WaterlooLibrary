from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zimablue@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def create_tables():
    with db.engine.connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                UserID INT PRIMARY KEY AUTO_INCREMENT,
                UserName VARCHAR(50) NOT NULL,
                Email VARCHAR(100) NOT NULL UNIQUE,
                PhoneNumber VARCHAR(15) NOT NULL UNIQUE,
                Password VARCHAR(255) NOT NULL,
                Status VARCHAR(10) NOT NULL DEFAULT 'Active'
            );
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS books (
                BookID INT PRIMARY KEY AUTO_INCREMENT,
                Title VARCHAR(255),
                Author VARCHAR(255),
                Genre VARCHAR(255),
                ISBN VARCHAR(13),
                PublicationDate DATE,
                AvailabilityStatus ENUM('Available', 'Checked Out', 'Reserved') DEFAULT 'Available'
            );
        """)

if __name__ == "__main__":
    with app.app_context():
        create_tables()
