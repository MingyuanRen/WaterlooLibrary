-- All the queries in the file are been given using actual examples
-- The actuall implementation of the queries in the application includes changes on the actual values 
-- The following are the 

-- Login (Using email)
SELECT * FROM Users WHERE Email = 'example@gmail.com'

-- Search for a book (Using title)
SELECT * FROM Books WHERE title LIKE 'example book'

-- Search for a book (Using ISBN)
SELECT * FROM Books WHERE ISBN LIKE '12345678'

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
SELECT inventory FROM Books WHERE ISBN = "0002005018";

--- 4. If 3 returns an inventory greater than 1, then we will first update inventory
UPDATE Books SET inventory = inventory - 1
WHERE ISBN = "0002005018";

--- 5. Insert into BookRecord table where
INSERT INTO BorrowRecord (uid, ISBN, renewable,
DateBorrowed, DateDue, DateReturned)
VALUES (1, "0002005018", 1, "2020-05-01", "2020-05-14", NULL);


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

