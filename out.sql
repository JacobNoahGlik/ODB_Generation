DROP TABLE Lives;
DROP TABLE Place;
DROP TABLE SongsAppears;
DROP TABLE Plays;
DROP TABLE Instruments;
DROP TABLE Musicians;

CREATE TABLE Musicians (
	ssn CHAR(9),
	name CHAR(30),
	annualIncome REAL,
	PRIMARY KEY (ssn)
);
CREATE TABLE Instruments (
	instrID CHAR(10),
	iname CHAR(30),
	musickey CHAR(10),
	PRIMARY KEY (instrID)
);
CREATE TABLE Plays (
	ssn CHAR(9),
	instrID CHAR(10),
	PRIMARY KEY (ssn,instrID),
	FOREIGN KEY ssn REFERENCES Musicians (ssn),
	FOREIGN KEY instrID REFERENCES Instruments (instrID)
);
CREATE TABLE SongsAppears (
	songID CHAR(10),
	ssn CHAR(9),
	title CHAR(40),
	albumIdentifier CHAR(40),
	PRIMARY KEY (songID),
	FOREIGN KEY ssn REFERENCES Musicians (ssn)
);
CREATE TABLE Place (
	aid CHAR(10),
	address CHAR(40),
	otherInfo CHAR(40),
	PRIMARY KEY (aid)
);
CREATE TABLE Lives (
	ssn CHAR(9),
	aid CHAR(10),
	phone CHAR(10),
	PRIMARY KEY (ssn,aid),
	FOREIGN KEY ssn REFERENCES Musicians (ssn),
	FOREIGN KEY aid REFERENCES Place (aid)
);

SELECT 'Musicians' FROM dual;
SELECT * FROM Musicians;
SELECT 'Instruments' FROM dual;
SELECT * FROM Instruments;
SELECT 'Plays' FROM dual;
SELECT * FROM Plays;
SELECT 'SongsAppears' FROM dual;
SELECT * FROM SongsAppears;
SELECT 'Place' FROM dual;
SELECT * FROM Place;
SELECT 'Lives' FROM dual;
SELECT * FROM Lives;
