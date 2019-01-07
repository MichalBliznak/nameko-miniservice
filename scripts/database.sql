DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
  id Int PRIMARY KEY,
  username Varchar NOT NULL,
  password Varchar NOT NULL
);
INSERT INTO Users(username, password) VALUES('michalbliznak', '123456789');