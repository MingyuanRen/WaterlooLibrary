-- All the queries in the file are been given using actual examples
-- The actuall implementation of the queries in the application includes changes on the actual values 
-- The following are the 

-- Add user(Sign up)
INSERT INTO Users (name, email, phone, Password) 
VALUES ('example', 'example@gmail.com', '1234567890', '12345')

-- Login (Using email)
SELECT * FROM Users WHERE Email = 'example@gmail.com'

-- Add book
INSERT INTO Books (ISBN, title, author, genre, year_of_publication, publisher, inventory, price)
VALUES ('12345678', 'example book', 'author', 'Fiction', DATE '2020-01-01', 'publiser', 10, 31)

-- Search for a book (Using title)
SELECT * FROM Books WHERE title LIKE 'example book' AND inventory > 0

-- Borrow book (Based on the searching result of previous step)
-- Assume the user select the book with ISBN '12345678' from the previous example
UPDATE Books
SET inventory = inventory - 1
WHERE ISBN = '12345678';

INSERT INTO BorrowRecord (uid, ISBN, renewable, DateBorrowed, DateDue, DateReturned)
VALUES (1, '12345678', true, CURRENT_DATE, DATEADD(month, 1, CURRENT_DATE), NULL);

-- Return book
-- Assume a user with uid 1 return the book with ISBN '12345678'
UPDATE Books
SET inventory = inventory + 1
WHERE ISBN = '12345678';

UPDATE BorrowRecord
SET DateReturned = CURRENT_DATE
WHERE (
    SELECT * FROM BorrowRecord 
    WHERE ISBN = '12345678'
    AND uid = 1
    AND DateReturned IS NULL
    LIMIT 1
);
