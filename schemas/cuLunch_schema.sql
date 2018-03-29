CREATE TABLE users (
  uni VARCHAR (10) PRIMARY KEY,
  name VARCHAR (50),
  schoolYear int NOT NULL,
  interests VARCHAR (200) NOT NULL,
  needsSwipes BOOLEAN,
  schoolName VARCHAR (50) NOT NULL
);

CREATE TABLE listings (
  expiryTime DATETIME NOT NULL,
  uni VARCHAR (10),
  location VARCHAR (10) NOT NULL,
  PRIMARY KEY (uni, expiryTime),
  FOREIGN KEY (uni) REFERENCES users
)