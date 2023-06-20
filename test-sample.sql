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




