from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:458i*488P@localhost:3306/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

INSERT_INTO = {
    'Users' : 
        """
        INSERT INTO Users (uid, name, email, phone, password)
        SELECT {uid}, '{name}', '{email}', '{phone}', '{password}'
        WHERE NOT EXISTS (SELECT * FROM Users WHERE uid = {uid});
        """,
    'Books' :
        """
        INSERT INTO Books (ISBN, title, author, year_of_publication, publisher, genre, inventory, price)
        SELECT '{ISBN}', '{title}', '{author}', DATE '{year_of_publication}-01-01', '{publisher}', '{genre}', {inventory}, {price}
        WHERE NOT EXISTS (SELECT * FROM Books WHERE ISBN = '{ISBN}');
        """,
    'MemberUsers' : 
        """
        INSERT INTO MemberUsers (uid, mID, points, start_date, end_date)
        SELECT {uid}, {mID}, {points}, DATE '{start_date}', DATE '{end_date}'
        WHERE NOT EXISTS (SELECT * FROM MemberUsers WHERE uid = {uid});
        """,  
    'Gifts' :
        """
        INSERT INTO Gifts (item, point_need, inventory)
        SELECT '{item}', {point_need}, {inventory}
        WHERE NOT EXISTS (SELECT * FROM Gifts WHERE item = '{item}');
        """,
    'BorrowRecord' :
        """
        INSERT INTO BorrowRecord (rid, uid, ISBN, renewable, DateBorrowed, DateDue, DateReturned)
        SELECT {rid}, {uid}, '{ISBN}', {renewable}, DATE '{date_borrowed}', DATE '{date_due}', DATE'{date_returned}'
        WHERE NOT EXISTS (SELECT * FROM BorrowRecord WHERE rid = {rid});
        """,    
    'Reservation' :
        """
        INSERT INTO Reservation (uid, ISBN, DateReserved, ExpireDate)
        SELECT {uid}, '{ISBN}', DATE '{DateReserved}', DATE '{ExpireDate}'
        WHERE NOT EXISTS (SELECT * FROM Reservation WHERE (uid, ISBN) = ({uid}, '{ISBN}'));
        """,
    'Redemption' :
        """
        INSERT INTO Redemption (uid, item, date)
        SELECT {uid}, '{item}', DATE '{date}'
        WHERE NOT EXISTS (SELECT * FROM Redemption WHERE (uid, item) = ({uid}, '{item}'));
        """  
}

# insert sample data into tables
# Note: tables have to be created before
def update_tables():
    with db.engine.connect() as connection:
        connection.execute(text(
            INSERT_INTO['Users'].format(
                uid=1, name='Lucas', email='lucas@gmail.com', phone='2029182132', password='K4GpyUl') +
            INSERT_INTO['Users'].format(
                uid=2, name='Tom', email='tom@gmail.com', phone='4635174607', password='EIwug8') +
            INSERT_INTO['Users'].format(
                uid=3, name='Ash', email='ash@hotmail.com', phone='4927195635', password='0KqsRoT') +
            INSERT_INTO['Users'].format(
                uid=4, name='Thomas', email='thomas@hotmail.com', phone='6629953138', password='V6mz1iU') +
            INSERT_INTO['Users'].format(
                uid=5, name='Viktor', email='vik@hotmail.com', phone='3444515449', password='TtrwsDW')
        ))

        connection.execute(text(
            INSERT_INTO['Books'].format(
                ISBN='0195153448',
                title='Classical Mythology',
                author='Mark P. O. Morford',
                year_of_publication=2002,
                publisher='Oxford University Press',
                genre='Historical Fiction',
                inventory=3,
                price=100.00
            ) +
            INSERT_INTO['Books'].format(
                ISBN='0002005018',
                title='Clara Callan',
                author='Richard Bruce Wright',
                year_of_publication=2001,
                publisher='HarperFlamingo Canada',
                genre='Fiction',
                inventory=2,
                price=500.00
            ) +
            INSERT_INTO['Books'].format(
                ISBN='0060973129',
                title='Decision in Normandy',
                author='Carlo D Este',
                year_of_publication=1991,
                publisher='HarperPerennial',
                genre='Bibiolograph',
                inventory=0,
                price=100000.00
            ) +
            INSERT_INTO['Books'].format(
                ISBN='0374157065',
                title='Flu: The Story of the Great Influenza Pandemic of 1918 and the Search for the Virus That Caused It',
                author='Gina Bari Kolata',
                year_of_publication=1999,
                publisher='Farrar Straus Giroux',
                genre='Report',
                inventory=0,
                price=100.00
            ) +
            INSERT_INTO['Books'].format(
                ISBN='0393045218',
                title='The Mummies of Urumchi',
                author='E. J. W. Barber',
                year_of_publication=1999,
                publisher='W. W. Norton &amp; Company',
                genre='Book',
                inventory=10,
                price=100.00
            )
        ))

        connection.execute(text(
            INSERT_INTO['MemberUsers'].format(
                uid=1, mID=1, points=1000, start_date='2023-06-15', end_date='2024-06-16'
            ) +
            INSERT_INTO['MemberUsers'].format(
                uid=5, mID=2, points=7000, start_date='2023-06-07', end_date='2024-06-08'
            )
        ))

        connection.execute(text(
            INSERT_INTO['Gifts'].format(
                item='Airpods', point_need=2000, inventory=2
            ) +
            INSERT_INTO['Gifts'].format(
                item='pencil', point_need=20, inventory=20
            )
        ))

        connection.execute(text(
            INSERT_INTO['BorrowRecord'].format(
                rid=1, uid=1, ISBN='0393045218', renewable='true', date_borrowed='2020-01-01', date_due='2020-02-01', date_returned='2020-01-15'
            ) +
            INSERT_INTO['BorrowRecord'].format(
                rid=2, uid=1, ISBN='0195153448', renewable='false', date_borrowed='2020-01-01', date_due='2020-02-01', date_returned='2020-02-01'
            )
        ))

        connection.execute(text(
            INSERT_INTO['Reservation'].format(
                uid=1, ISBN='0393045218', DateReserved='2022-03-04', ExpireDate='2023-01-01'
            ) + 
            INSERT_INTO['Reservation'].format(
                uid=1, ISBN='0195153448', DateReserved='2022-03-04', ExpireDate='2023-01-01'
            )
        ))

        connection.execute(text(
            INSERT_INTO['Redemption'].format(
                uid=5, item='pencil', date='2023-07-02'
            )
            # INSERT_INTO['Redemption'].format(
            #     uid=1, item='Airpods', date='2023-05-02'
            # )               
        ))

if __name__ == "__main__":
    with app.app_context():
        update_tables()
