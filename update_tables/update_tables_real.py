import pandas
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import random
import MySQLdb._exceptions as db_exception

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:458i*488P@localhost:3306/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Loading data
columns_to_use = ["ISBN", "Book-Title", "Book-Author", "Year-Of-Publication", "Publisher"]
book_data = pandas.read_csv(r'books.csv', usecols=columns_to_use, sep=';', header=0, index_col=False)

INSERT_INTO_BOOKS = """INSERT INTO Books (ISBN, title, author, year_of_publication, publisher, inventory, price)
        SELECT "{ISBN}", "{title}", "{author}", DATE "{year_of_publication}-01-01", "{publisher}", {inventory}, {price}
        WHERE NOT EXISTS (SELECT * FROM Books WHERE ISBN = '{ISBN}');"""

def generate_inventory():
    return random.randint(1, 50)


def generate_price():
    integer = str(random.randint(20, 200))
    fraction = "{:0>2}".format(str(random.randrange(5, 100, 5)))
    return float(integer + "." + fraction)
    

def update_tables():
    with db.engine.connect() as connection:
        for index, row in book_data.iterrows():
            try:
                connection.execute(text(
                    INSERT_INTO_BOOKS.format(
                        ISBN=row['ISBN'],
                        title=row['Book-Title'],
                        author=row['Book-Author'],
                        year_of_publication=row['Year-Of-Publication'],
                        publisher=row['Publisher'],
                        inventory=generate_inventory(),
                        price=generate_price()
                    )))
                connection.commit()
            except db_exception.ProgrammingError as e:
                print(e)

                # this type of error is most likely to be an SQL syntax error
                # caused by invalid or hard-to-handle chars in either book name
                # author name or publisher name. Thus, we can ignore this tuple
                # while print out which is that.
                continue


if __name__ == "__main__":

    try:
        with app.app_context():
            update_tables()
    except Exception as e:
        print(str(e))
