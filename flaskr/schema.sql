 DROP TABLE IF EXISTS Users;

 DROP TABLE IF EXISTS Location;

 DROP  TABLE IF EXISTS UserLocation;

 CREATE TABLE IF NOT EXISTS Users (
        username varchar [PRIMARY KEY, NOT NULL],
        PasswordHash binary [NOT NULL],
        firstName varchar,
        lastName varchar,
        isInfected boolean,
        isAdmin boolean
      );

 CREATE TABLE IF NOT EXISTS Location (
        location_id int [NOT NULL, PRIMARY KEY],
        name varchar [NOT NULL],
        rate float [NOT NULL]
      );

 CREATE TABLE IF NOT EXISTS UserLocation (
        location_id int,
        entryTime datetime,
        rate float,
        username varchar,
          foreign key(location_id)
              references Location(location_id),
          foreign key(username)
              references Users(username)
       );