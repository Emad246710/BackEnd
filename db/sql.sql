CREATE TABLE User (
  id INTEGER not null,
  username TEXT not null,
  password TEXT not null,
  unique(username)
  primary key (id)
);

CREATE TABLE Category (
  id INTEGER not null,
  type TEXT not null,
  unique(type),
  primary key (id)
);

CREATE TABLE Note (
  id INTEGER not null,
  content TEXT not null,
  createdOn TEXT not null,
  priority INTEGER not null, --  1 <= priority <= 5
  userId INTEGER not null,-- Make it Nullable??
  categoryId INTEGER not null, -- Nullable
  foreign key (userId) references User(id) ON DELETE CASCADE,
  foreign key (categoryId) references Category(id) , -- ON DELETE Nothing
  CHECK (priority >= 1 AND priority <=5) 
  primary key (id)
);


insert into User values
(1, 'user1' , 'ps1'),
(2, 'user2', 'ps2'),
(3, 'user3', 'ps3');

insert into Category values
(1 , 'type1'),
(2 , 'type2'),
(3 , 'type3'),
(4 , 'type4'),
(5 , 'type5');


insert into Note values
 (1 , "Integer in libero vitae lorem consectetur rutrum at a turpis. Aliquam mi nisl, placerat at bibendum at...", '2020-04-01T22:00:00.000Z' , 1, 1 , 1 ),
 (2 , "Mauris dapibus a ante et pellentesque. Pellentesque iaculis pellentesque tortor ac mollis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed pretium ultricies eros vel sodales. ", '2020-04-01T22:00:00.000Z' , 5, 2 , 2 ),
 (3 , "Pellentesque fringilla nibh non sem ultrices hendrerit. Nunc pellentesque quis libero vel dignissim...", '2020-04-01T22:00:00.000Z' , 2, 3 , 3 ),
 (4 , "Sed et finibus ante. Etiam et elementum elit. Sed suscipit, enim a pellentesque laoreet, urna ante bibendum ante, id molestie ipsum mi consectetur ligula. Donec commodo arcu vitae ante porta imperdiet eu eget dui. ", '2020-04-02T22:00:00.000Z' , 4, 1 , 4 ),
 (5 , "Curabitur sit amet tellus risus. Maecenas dictum neque in nibh dapibus, sit amet molestie nibh sodales. Nullam ut velit in lectus blandit lobortis. Fusce ullamcorper tellus at lacus interdum, sed tempus sem porttitor.", '2020-04-02T22:00:00.000Z' , 3, 1 , 5 ),
 (6 , "Duis sodales tristique mauris sit amet aliquet. Nulla ac molestie justo. Interdum et malesuada fames ac ante ipsum primis in faucibus. In sed tincidunt felis. Pellentesque eget nibh volutpat, elementum erat ut, placerat arcu. ", '2020-04-03T22:00:00.000Z' , 2, 2 , 3 ),
 (7 , "Maecenas eget ante sit amet ante convallis consectetur. Nullam venenatis ut nisl sed luctus. Cras egestas condimentum diam in egestas. Integer imperdiet elit eget elit maximus ultricies. Aliquam tempus ligula vestibulum sollicitudin dictum. ", '2020-04-03T22:00:00.000Z' , 1, 2 , 2 ),
 (8 , "Integer iaculis laoreet turpis, vitae faucibus dolor fringilla eget. Proin molestie nunc lorem, in pharetra sem faucibus in. In ut justo non lacus faucibus molestie. ", '2020-04-04T22:00:00.000Z' , 5, 3 , 1 ),
 (9 , "In nec cursus elit, at bibendum odio. Integer enim dui, tempor sed iaculis vitae, gravida nec velit. Duis lobortis ante in orci consequat tristique. Nulla laoreet laoreet nisl ac laoreet. ", '2020-04-04T22:00:00.000Z' , 4, 3 , 5),
 (10 , "Praesent sed lobortis turpis. Phasellus id ultricies velit. Sed sem nulla, tincidunt in euismod et, placerat quis velit. Nulla blandit erat et elit dignissim, vitae porttitor sem faucibus.", '2020-04-05T22:00:00.000Z' , 3, 1 , 4 );




PRAGMA foreign_keys = ON;


SELECT *
FROM User u, Note n 
WHERE u.id=n.userId AND   u.id=1;

-- SELECT *
-- FROM author a
-- WHERE NOT EXISTS(
-- 		 SELECT *
-- 		 FROM book b
-- 		 WHERE NOT EXISTS(
-- 				  SELECT *
-- 				  FROM _BooksToAuthors bk_ar
-- 				  WHERE bk_ar.bookId=b.id AND bk_ar.authorId=a.id
-- 				  )
-- 		 )
-- ;

