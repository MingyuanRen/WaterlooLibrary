-- All the queries in the file are been given using actual examples
-- The actuall implementation of the queries in the application includes changes on the actual values 
-- All the following ISBN and Book titles are from actual production database

-- Login (Using email)
SELECT * FROM Users WHERE Email = 'lucas@gmail.com'

-- Search for a book (Using title)
SELECT * FROM Books WHERE title LIKE 'Liar'

-- Search for a book (Using ISBN)
SELECT * FROM Books WHERE ISBN LIKE '0001047213'

-- Check points (of current user)
SELECT points FROM MemberUsers WHERE uid = '11'

-- Display gifts
SELECT * FROM Gifts

-- Check reservation
SELECT * FROM Reservation WHERE uid = '1'

-- Check borrow record of current user
SELECT * FROM BorrowRecord WHERE uid = '1'

-- Check borrow record of a book
SELECT * FROM BorrowRecord WHERE ISBN = '12345678'

-- Borrow book related
--- 1. check if user is member: 
SELECT * FROM MemberUsers
WHERE uid = 1;

--- 2. check the limit for borrowed books per user
SELECT count(*) FROM BorrowRecord
WHERE uid = 1 AND DateReturned IS NULL;

--- 3. Check if the book with sample_isbn is available
SELECT inventory FROM Books WHERE ISBN = "000104799X";

--- 4. If 3 returns an inventory greater than 1, then we will first update inventory
UPDATE Books SET inventory = inventory - 1
WHERE ISBN = "000104799X";

--- 5. Insert into BookRecord table where
INSERT INTO BorrowRecord (uid, ISBN, renewable,
DateBorrowed, DateDue, DateReturned)
VALUES (1, "000104799X", 1, "2020-05-01", "2020-05-14", NULL);


-- Points Redemption related
--- 1. Check if current user is a member
SELECT points FROM MemberUsers
WHERE uid = 1;

--- 2. Check if current user has enough points and if ample_gift has inventory > 0
SELECT point_need, inventory FROM Gifts
WHERE item = "pencil";

--- 3. Update inventory of sample_gift
UPDATE Gifts SET inventory = inventory - 1
WHERE item = "pencil";

--- 4. Update user points
UPDATE MemberUsers, gifts SET points = MemberUsers.points - gifts.point_need
WHERE uid = 1 AND gifts.item = "pencil";

--- 5. Insert into Redemption where
INSERT INTO Redemption
VALUES (1, "pencil", "2020-01-01");

-- Return Book related
--- 1. check if the return date of the book is already after the expected duedate
SELECT DateDue FROM BorrowRecord
WHERE ISBN = "000104799X";

--- 2. update the return date of that book to be today in the BorrowRecord table.
UPDATE BorrowRecord SET DateReturned = "2020-05-10"
WHERE uid = 1 AND ISBN = "000104799X";

--- 3. check if current user is a member
SELECT * FROM MemberUsers
WHERE uid = 1;

--- 4. add points to membership account
UPDATE MemberUsers SET points = points + 10
WHERE uid = 1;

-- User Registration and Login related
--- 1. Check if the user is already registered in the system
SELECT email
FROM Users
WHERE email = 'sample@gmail.com';

--- 2. Registration
INSERT INTO Users (name, email, phone, password)
VALUES ("sample", "sample@gmail.com", "1234567890", "password");

--- 3. Login
SELECT title, author, DateBorrowed, DateDue, DateReturned
FROM Users NATURAL JOIN borrowrecord NATURAL JOIN Books
WHERE email = "lucas@gmail.com" AND password = "12345";


