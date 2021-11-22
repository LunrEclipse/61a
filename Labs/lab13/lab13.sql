.read data.sql


CREATE TABLE bluedog AS
  SELECT color, pet FROM students where color = "blue" AND pet = "dog";

CREATE TABLE bluedog_songs AS
  SELECT color, pet, song FROM students where color = "blue" and pet = "dog";


CREATE TABLE smallest_int_having AS
  SELECT time, smallest FROM students GROUP BY smallest HAVING COUNT(*) = 1 ;


CREATE TABLE matchmaker AS
  SELECT a.pet, a.song, a.color, b.color FROM students AS a, students AS b
    WHERE a.pet = b.pet AND a.song = b.song AND a.time != b.time;


CREATE TABLE sevens AS
  SELECT a.seven FROM students AS a, numbers as b
    WHERE a.number = 7 AND b.'7' = 'True' AND a.time = b.time;


CREATE TABLE avg_difference AS
  SELECT round(avg(abs(number-smallest))) FROM students;

