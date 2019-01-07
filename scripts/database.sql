DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
  id Int PRIMARY KEY,
  username Varchar NOT NULL,
  password Varchar NOT NULL
);
INSERT INTO Users(id, username, password) VALUES(1, 'demo', 'demo');