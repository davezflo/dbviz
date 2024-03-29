
-- Begin Structure --

CREATE TABLE Author (
    AuthorId INT PRIMARY KEY,
    Name TEXT,
    Age INT
);
CREATE TABLE Book (
    BookId INT PRIMARY KEY,
    Title TEXT,
    PublicationDate datetime
);
CREATE TABLE AuthoredBy (
    AuthorId INT,
    BookId INT,
    FOREIGN KEY(AuthorId) REFERENCES Author(AuthorId),
    FOREIGN KEY(BookId) REFERENCES Book(BookId)
);

-- End Structure --

-- Begin Examples --
-- select Name from Author join authoredby on author.authorid = authoredby.authorid join book on authoredby.bookid = book.bookid where book.title LIKE '%Journey%Through%the%Stars%';
-- select Title from Book join authoredby on book.bookid = authoredby.bookid join author on authored.authorid = author.authorid where author.name LIKE %Casey%Quinn%'; 
-- select title, publicationdate from Book join authoredby on book.bookid = authoredby.bookid join author on authored.authorid = author.authorid where author.name LIKE %Casey%Quinn%';
-- End Examples --

-- Begin Inserts --

-- The following was generated by GPT-4
-- Inserting Authors
INSERT INTO Author (AuthorId, Name, Age) VALUES (1, 'Alex Morgan', 45);
INSERT INTO Author (AuthorId, Name, Age) VALUES (2, 'Taylor Lee', 38);
INSERT INTO Author (AuthorId, Name, Age) VALUES (3, 'Jordan Kim', 52);
INSERT INTO Author (AuthorId, Name, Age) VALUES (4, 'Casey Quinn', 29);
INSERT INTO Author (AuthorId, Name, Age) VALUES (5, 'Riley Jordan', 41);

-- Inserting Books
INSERT INTO Book (BookId, Title, PublicationDate) VALUES (1, 'The Hidden Valley', '2021-05-15');
INSERT INTO Book (BookId, Title, PublicationDate) VALUES (2, 'Journey Through the Stars', '2020-11-20');
INSERT INTO Book (BookId, Title, PublicationDate) VALUES (3, 'Echoes of the Past', '2019-03-22');
INSERT INTO Book (BookId, Title, PublicationDate) VALUES (4, 'Whispers of Tomorrow', '2022-01-08');
INSERT INTO Book (BookId, Title, PublicationDate) VALUES (5, 'Beyond the Horizon', '2018-07-30');
INSERT INTO Book (BookId, Title, PublicationDate) VALUES (6, 'Shadows in the Mist', '2021-09-17');
INSERT INTO Book (BookId, Title, PublicationDate) VALUES (7, 'Dreams of the Silent City', '2020-04-12');
INSERT INTO Book (BookId, Title, PublicationDate) VALUES (8, 'Secrets of the Ocean', '2022-06-23');
INSERT INTO Book (BookId, Title, PublicationDate) VALUES (9, 'Mysteries Unveiled', '2019-12-05');
INSERT INTO Book (BookId, Title, PublicationDate) VALUES (10, 'Legends of the Forgotten Realm', '2023-02-14');

-- Inserting Relationships in AuthoredBy
-- (These are arbitrary relationships between authors and books)
INSERT INTO AuthoredBy (AuthorId, BookId) VALUES (1, 1);
INSERT INTO AuthoredBy (AuthorId, BookId) VALUES (1, 2);
INSERT INTO AuthoredBy (AuthorId, BookId) VALUES (2, 3);
INSERT INTO AuthoredBy (AuthorId, BookId) VALUES (2, 4);
INSERT INTO AuthoredBy (AuthorId, BookId) VALUES (3, 5);
INSERT INTO AuthoredBy (AuthorId, BookId) VALUES (3, 6);
INSERT INTO AuthoredBy (AuthorId, BookId) VALUES (4, 7);
INSERT INTO AuthoredBy (AuthorId, BookId) VALUES (4, 8);
INSERT INTO AuthoredBy (AuthorId, BookId) VALUES (5, 9);
INSERT INTO AuthoredBy (AuthorId, BookId) VALUES (5, 10);

-- End Inserts --