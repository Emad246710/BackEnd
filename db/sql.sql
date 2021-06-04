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
  userId INTEGER ,
  foreign key (userId) references User(id) ON DELETE CASCADE,
  -- unique(type),
  primary key (id)
);

CREATE TABLE Note (
  id INTEGER not null,
  content TEXT not null,
  createdOn TEXT not null,
  priority INTEGER , --  1 <= priority <= 5 or NULL
  userId INTEGER not null,
  categoryId INTEGER , -- Nullable
  foreign key (userId) references User(id) ON DELETE CASCADE,
  foreign key (categoryId) references Category(id) , -- ON DELETE Nothing
  CHECK ((priority >= 1 AND priority <=5 ) OR priority is NULL) 
  primary key (id)
);


insert into User values
(1, 'user1' , 'ps1'),
(2, 'user2', 'ps2'),
(3, 'user3', 'ps3'),
(4, 'user4', 'ps4'),
(5, 'user5', 'ps5');

insert into Category values
(1 ,  "type1" , 1),
(2 ,  "type2" , 1),
(3 ,  "type3" , 1),
(4 ,  "type4" , 1),
(5 ,  "type5" , 1),
(6 ,  "type6" , 2),
(7 ,  "type7" , 2),
(8 ,  "type8" , 2),
(9 ,  "type9" , 2),
(10 ,  "type10" , 2),
(11 ,  "type11" , 3),
(12 ,  "type12" , 3),
(13 ,  "type13" , 3),
(14 ,  "type14" , 3),
(15 ,  "type15" , 3),
(16 ,  "type16" , 4),
(17 ,  "type17" , 4),
(18 ,  "type18" , 4),
(19 ,  "type19" , 4),
(20 ,  "type20" , 4),
(21 ,  "type21" , 5),
(22 ,  "type22" , 5),
(23 ,  "type23" , 5),
(24 ,  "type24" , 5),
(25 ,  "type25" , 5);
 

insert into Note values
(1 , "Integer in libero vitae lorem consectetur rutrum at a turpis. Aliquam mi nisl, placerat at bibendum at..." , " 2020-04-01T22:00:00.000Z" , 1 , 1 , 1), 
 (2 , "Mauris dapibus a ante et pellentesque. Pellentesque iaculis pellentesque tortor ac mollis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed pretium ultricies eros vel sodales. " , " 2020-04-01T22:00:00.000Z" , 2 , 2 , 6), 
 (3 , "Pellentesque fringilla nibh non sem ultrices hendrerit. Nunc pellentesque quis libero vel dignissim..." , " 2020-04-01T22:00:00.000Z" , 3 , 3 , 11), 
 (4 , "Sed et finibus ante. Etiam et elementum elit. Sed suscipit, enim a pellentesque laoreet, urna ante bibendum ante, id molestie ipsum mi consectetur ligula. Donec commodo arcu vitae ante porta imperdiet eu eget dui. " , " 2020-04-02T22:00:00.000Z" , 4 , 4 , 16), 
 (5 , "Curabitur sit amet tellus risus. Maecenas dictum neque in nibh dapibus, sit amet molestie nibh sodales. Nullam ut velit in lectus blandit lobortis. Fusce ullamcorper tellus at lacus interdum, sed tempus sem porttitor." , " 2020-04-02T22:00:00.000Z" , 5 , 5 , 21), 
 (6 , "Duis sodales tristique mauris sit amet aliquet. Nulla ac molestie justo. Interdum et malesuada fames ac ante ipsum primis in faucibus. In sed tincidunt felis. Pellentesque eget nibh volutpat, elementum erat ut, placerat arcu. " , " 2020-04-03T22:00:00.000Z" , 1 , 1 , 2), 
 (7 , "Maecenas eget ante sit amet ante convallis consectetur. Nullam venenatis ut nisl sed luctus. Cras egestas condimentum diam in egestas. Integer imperdiet elit eget elit maximus ultricies. Aliquam tempus ligula vestibulum sollicitudin dictum. " , " 2020-04-03T22:00:00.000Z" , 2 , 2 , 7), 
 (8 , "Integer iaculis laoreet turpis, vitae faucibus dolor fringilla eget. Proin molestie nunc lorem, in pharetra sem faucibus in. In ut justo non lacus faucibus molestie. " , " 2020-04-04T22:00:00.000Z" , 3 , 3 , 12), 
 (9 , "In nec cursus elit, at bibendum odio. Integer enim dui, tempor sed iaculis vitae, gravida nec velit. Duis lobortis ante in orci consequat tristique. Nulla laoreet laoreet nisl ac laoreet. " , " 2020-04-04T22:00:00.000Z" , 4 , 4 , 17), 
 (10 , "Praesent sed lobortis turpis. Phasellus id ultricies velit. Sed sem nulla, tincidunt in euismod et, placerat quis velit. Nulla blandit erat et elit dignissim, vitae porttitor sem faucibus." , " 2020-04-05T22:00:00.000Z" , 5 , 5 , 22), 
 (11 , "Duis sodales tristique mauris sit amet aliquet. Nulla ac molestie justo. Interdum et malesuada fames ac ante ipsum primis in faucibus. In sed tincidunt felis. Pellentesque eget nibh volutpat, elementum erat ut, placerat arcu. " , " 2020-04-05T22:00:00.000Z" , 1 , 1 , 3), 
 (12 , "Maecenas eget ante sit amet ante convallis consectetur. Nullam venenatis ut nisl sed luctus. Cras egestas condimentum diam in egestas. Integer imperdiet elit eget elit maximus ultricies. Aliquam tempus ligula vestibulum sollicitudin dictum. " , " 2020-04-05T22:00:00.000Z" , 2 , 2 , 8), 
 (13 , "Integer iaculis laoreet turpis, vitae faucibus dolor fringilla eget. Proin molestie nunc lorem, in pharetra sem faucibus in. In ut justo non lacus faucibus molestie. " , " 2020-04-05T22:00:00.000Z" , 3 , 3 , 13), 
 (14 , "In nec cursus elit, at bibendum odio. Integer enim dui, tempor sed iaculis vitae, gravida nec velit. Duis lobortis ante in orci consequat tristique. Nulla laoreet laoreet nisl ac laoreet. " , " 2020-04-05T22:00:00.000Z" , 4 , 4 , 18), 
 (15 , "Duis sodales tristique mauris sit amet aliquet. Nulla ac molestie justo. Interdum et malesuada fames ac ante ipsum primis in faucibus. In sed tincidunt felis. Pellentesque eget nibh volutpat, elementum erat ut, placerat arcu. " , " 2020-04-05T22:00:00.000Z" , 5 , 5 , 23), 
 (16 , "Maecenas eget ante sit amet ante convallis consectetur. Nullam venenatis ut nisl sed luctus. Cras egestas condimentum diam in egestas. Integer imperdiet elit eget elit maximus ultricies. Aliquam tempus ligula vestibulum sollicitudin dictum. " , " 2020-04-05T22:00:00.000Z" , 1 , 1 , 4), 
 (17 , "Integer in libero vitae lorem consectetur rutrum at a turpis. Aliquam mi nisl, placerat at bibendum at..." , " 2020-04-05T22:00:00.000Z" , 2 , 2 , 9), 
 (18 , "Mauris dapibus a ante et pellentesque. Pellentesque iaculis pellentesque tortor ac mollis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed pretium ultricies eros vel sodales. " , " 2020-04-05T22:00:00.000Z" , 3 , 3 , 14), 
 (19 , "Pellentesque fringilla nibh non sem ultrices hendrerit. Nunc pellentesque quis libero vel dignissim..." , " 2020-04-05T22:00:00.000Z" , 4 , 4 , 19), 
 (20 , "Sed et finibus ante. Etiam et elementum elit. Sed suscipit, enim a pellentesque laoreet, urna ante bibendum ante, id molestie ipsum mi consectetur ligula. Donec commodo arcu vitae ante porta imperdiet eu eget dui. " , " 2020-04-05T22:00:00.000Z" , 5 , 5 , 24), 
 (21 , "Curabitur sit amet tellus risus. Maecenas dictum neque in nibh dapibus, sit amet molestie nibh sodales. Nullam ut velit in lectus blandit lobortis. Fusce ullamcorper tellus at lacus interdum, sed tempus sem porttitor." , " 2020-04-05T22:00:00.000Z" , 1 , 1 , 5), 
 (22 , "Duis sodales tristique mauris sit amet aliquet. Nulla ac molestie justo. Interdum et malesuada fames ac ante ipsum primis in faucibus. In sed tincidunt felis. Pellentesque eget nibh volutpat, elementum erat ut, placerat arcu. " , " 2020-04-05T22:00:00.000Z" , 2 , 2 , 10), 
 (23 , "Maecenas eget ante sit amet ante convallis consectetur. Nullam venenatis ut nisl sed luctus. Cras egestas condimentum diam in egestas. Integer imperdiet elit eget elit maximus ultricies. Aliquam tempus ligula vestibulum sollicitudin dictum. " , " 2020-04-01T22:00:00.000Z" , 3 , 3 , 15), 
 (24 , "Integer iaculis laoreet turpis, vitae faucibus dolor fringilla eget. Proin molestie nunc lorem, in pharetra sem faucibus in. In ut justo non lacus faucibus molestie. " , " 2020-04-01T22:00:00.000Z" , 4 , 4 , 20), 
 (25 , "In nec cursus elit, at bibendum odio. Integer enim dui, tempor sed iaculis vitae, gravida nec velit. Duis lobortis ante in orci consequat tristique. Nulla laoreet laoreet nisl ac laoreet. " , " 2020-04-01T22:00:00.000Z" , 5 , 5 , 25), 
 (26 , "Praesent sed lobortis turpis. Phasellus id ultricies velit. Sed sem nulla, tincidunt in euismod et, placerat quis velit. Nulla blandit erat et elit dignissim, vitae porttitor sem faucibus." , " 2020-04-02T22:00:00.000Z" , 1 , 1 , 1), 
 (27 , "Duis sodales tristique mauris sit amet aliquet. Nulla ac molestie justo. Interdum et malesuada fames ac ante ipsum primis in faucibus. In sed tincidunt felis. Pellentesque eget nibh volutpat, elementum erat ut, placerat arcu. " , " 2020-04-02T22:00:00.000Z" , 2 , 2 , 6), 
 (28 , "Maecenas eget ante sit amet ante convallis consectetur. Nullam venenatis ut nisl sed luctus. Cras egestas condimentum diam in egestas. Integer imperdiet elit eget elit maximus ultricies. Aliquam tempus ligula vestibulum sollicitudin dictum. " , " 2020-04-03T22:00:00.000Z" , 3 , 3 , 11), 
 (29 , "Integer iaculis laoreet turpis, vitae faucibus dolor fringilla eget. Proin molestie nunc lorem, in pharetra sem faucibus in. In ut justo non lacus faucibus molestie. " , " 2020-04-03T22:00:00.000Z" , 4 , 4 , 16), 
 (30 , "In nec cursus elit, at bibendum odio. Integer enim dui, tempor sed iaculis vitae, gravida nec velit. Duis lobortis ante in orci consequat tristique. Nulla laoreet laoreet nisl ac laoreet. " , " 2020-04-04T22:00:00.000Z" , 5 , 5 , 21), 
 (31 , "Duis sodales tristique mauris sit amet aliquet. Nulla ac molestie justo. Interdum et malesuada fames ac ante ipsum primis in faucibus. In sed tincidunt felis. Pellentesque eget nibh volutpat, elementum erat ut, placerat arcu. " , " 2020-04-04T22:00:00.000Z" , 1 , 1 , 2), 
 (32 , "Maecenas eget ante sit amet ante convallis consectetur. Nullam venenatis ut nisl sed luctus. Cras egestas condimentum diam in egestas. Integer imperdiet elit eget elit maximus ultricies. Aliquam tempus ligula vestibulum sollicitudin dictum. " , " 2020-04-05T22:00:00.000Z" , 2 , 2 , 7), 
 (33 , "Integer in libero vitae lorem consectetur rutrum at a turpis. Aliquam mi nisl, placerat at bibendum at..." , " 2020-04-05T22:00:00.000Z" , 3 , 3 , 12), 
 (34 , "Mauris dapibus a ante et pellentesque. Pellentesque iaculis pellentesque tortor ac mollis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed pretium ultricies eros vel sodales. " , " 2020-04-05T22:00:00.000Z" , 4 , 4 , 17), 
 (35 , "Pellentesque fringilla nibh non sem ultrices hendrerit. Nunc pellentesque quis libero vel dignissim..." , " 2020-04-05T22:00:00.000Z" , 5 , 5 , 22), 
 (36 , "Sed et finibus ante. Etiam et elementum elit. Sed suscipit, enim a pellentesque laoreet, urna ante bibendum ante, id molestie ipsum mi consectetur ligula. Donec commodo arcu vitae ante porta imperdiet eu eget dui. " , " 2020-04-05T22:00:00.000Z" , 1 , 1 , 3), 
 (37 , "Curabitur sit amet tellus risus. Maecenas dictum neque in nibh dapibus, sit amet molestie nibh sodales. Nullam ut velit in lectus blandit lobortis. Fusce ullamcorper tellus at lacus interdum, sed tempus sem porttitor." , " 2020-04-05T22:00:00.000Z" , 2 , 2 , 8), 
 (38 , "Duis sodales tristique mauris sit amet aliquet. Nulla ac molestie justo. Interdum et malesuada fames ac ante ipsum primis in faucibus. In sed tincidunt felis. Pellentesque eget nibh volutpat, elementum erat ut, placerat arcu. " , " 2020-04-05T22:00:00.000Z" , 3 , 3 , 13), 
 (39 , "Maecenas eget ante sit amet ante convallis consectetur. Nullam venenatis ut nisl sed luctus. Cras egestas condimentum diam in egestas. Integer imperdiet elit eget elit maximus ultricies. Aliquam tempus ligula vestibulum sollicitudin dictum. " , " 2020-04-05T22:00:00.000Z" , 4 , 4 , 18), 
 (40 , "Integer iaculis laoreet turpis, vitae faucibus dolor fringilla eget. Proin molestie nunc lorem, in pharetra sem faucibus in. In ut justo non lacus faucibus molestie. " , " 2020-04-05T22:00:00.000Z" , 5 , 5 , 23), 
 (41 , "In nec cursus elit, at bibendum odio. Integer enim dui, tempor sed iaculis vitae, gravida nec velit. Duis lobortis ante in orci consequat tristique. Nulla laoreet laoreet nisl ac laoreet. " , " 2020-04-05T22:00:00.000Z" , 1 , 1 , 4), 
 (42 , "Praesent sed lobortis turpis. Phasellus id ultricies velit. Sed sem nulla, tincidunt in euismod et, placerat quis velit. Nulla blandit erat et elit dignissim, vitae porttitor sem faucibus." , " 2020-04-05T22:00:00.000Z" , 2 , 2 , 9), 
 (43 , "Duis sodales tristique mauris sit amet aliquet. Nulla ac molestie justo. Interdum et malesuada fames ac ante ipsum primis in faucibus. In sed tincidunt felis. Pellentesque eget nibh volutpat, elementum erat ut, placerat arcu. " , " 2020-04-05T22:00:00.000Z" , 3 , 3 , 14), 
 (44 , "Maecenas eget ante sit amet ante convallis consectetur. Nullam venenatis ut nisl sed luctus. Cras egestas condimentum diam in egestas. Integer imperdiet elit eget elit maximus ultricies. Aliquam tempus ligula vestibulum sollicitudin dictum. " , " 2020-04-05T22:00:00.000Z" , 4 , 4 , 19), 
 (45 , "Integer iaculis laoreet turpis, vitae faucibus dolor fringilla eget. Proin molestie nunc lorem, in pharetra sem faucibus in. In ut justo non lacus faucibus molestie. " , " 2020-04-01T22:00:00.000Z" , 5 , 5 , 24), 
 (46 , "In nec cursus elit, at bibendum odio. Integer enim dui, tempor sed iaculis vitae, gravida nec velit. Duis lobortis ante in orci consequat tristique. Nulla laoreet laoreet nisl ac laoreet. " , " 2020-04-01T22:00:00.000Z" , 1 , 1 , 5), 
 (47 , "Duis sodales tristique mauris sit amet aliquet. Nulla ac molestie justo. Interdum et malesuada fames ac ante ipsum primis in faucibus. In sed tincidunt felis. Pellentesque eget nibh volutpat, elementum erat ut, placerat arcu. " , " 2020-04-01T22:00:00.000Z" , 2 , 2 , 10), 
 (48 , "Maecenas eget ante sit amet ante convallis consectetur. Nullam venenatis ut nisl sed luctus. Cras egestas condimentum diam in egestas. Integer imperdiet elit eget elit maximus ultricies. Aliquam tempus ligula vestibulum sollicitudin dictum. " , " 2020-04-02T22:00:00.000Z" , 3 , 3 , 15), 
 (49 , "Integer in libero vitae lorem consectetur rutrum at a turpis. Aliquam mi nisl, placerat at bibendum at..." , " 2020-04-02T22:00:00.000Z" , 4 , 4 , 20), 
 (50 , "Mauris dapibus a ante et pellentesque. Pellentesque iaculis pellentesque tortor ac mollis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed pretium ultricies eros vel sodales. " , " 2020-04-03T22:00:00.000Z" , 5 , 5 , 25);


PRAGMA foreign_keys = ON;


SELECT *
FROM User u, Note n 
WHERE u.id=n.userId AND   u.id=1;
