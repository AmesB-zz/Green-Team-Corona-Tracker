--SQL schema framework from Flask tutorial
--https://flask.palletsprojects.com/en/2.0.x/tutorial/database/
--© Copyright 2010 Pallets


DROP TABLE IF EXISTS user;
--DROP TABLE IF EXISTS post;

CREATE TABLE user (
  --id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR PRIMARY KEY NOT NULL,
  passwordHash TEXT NOT NULL
--  firstName VARCHAR NOT NULL
 -- lastName VARCHAR NOT NULL
 -- isInfected ??
 -- isAdmin ??
);

--CREATE TABLE post (
--  id INTEGER PRIMARY KEY AUTOINCREMENT,
 -- author_id INTEGER NOT NULL,
 -- created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 -- title TEXT NOT NULL,
--  body TEXT NOT NULL,
--  FOREIGN KEY (author_id) REFERENCES user (id)
--);