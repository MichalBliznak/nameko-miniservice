DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
  userid Varchar PRIMARY KEY NOT NULL,
  username Varchar NOT NULL,
  password Varchar NOT NULL
);
INSERT INTO Users(userid, username, password) VALUES('dca6c3ff-7742-487e-b897-0ce353388907', 'demo', 'demo');