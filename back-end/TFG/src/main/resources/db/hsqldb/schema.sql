DROP TABLE administrators IF EXISTS;
DROP TABLE employees IF EXISTS;
DROP TABLE customers IF EXISTS;
DROP TABLE companies IF EXISTS;

CREATE TABLE administrators(
	id 			INTEGER IDENTITY PRIMARY KEY,
	email 		VARCHAR(30),
  	password  	VARCHAR(30),
  	name    	VARCHAR(255),
  	surname     VARCHAR_IGNORECASE(80),
  	dni       	VARCHAR(80),
  	telephone  	VARCHAR(20)
  	);	

CREATE TABLE employees(
	id 			INTEGER IDENTITY PRIMARY KEY,
	email 		VARCHAR(30),
  	password  	VARCHAR(30),
  	name    	VARCHAR(255),
  	surname     VARCHAR_IGNORECASE(80),
  	dni       	VARCHAR(80),
  	telephone  	VARCHAR(20),
  	qualification  	VARCHAR(255)
	);
	
CREATE TABLE customers(
	id 			INTEGER IDENTITY PRIMARY KEY,
	email 		VARCHAR(30),
  	password  	VARCHAR(30),
  	name    	VARCHAR(255),
  	surname     VARCHAR_IGNORECASE(80),
  	dni       	VARCHAR(80),
  	telephone  	VARCHAR(20),
  	address  	VARCHAR(255),
  	account		VARCHAR(255)
	);
	
CREATE TABLE companies(
	id 			INTEGER IDENTITY PRIMARY KEY,
	email 		VARCHAR(30),
  	password  	VARCHAR(30),
  	name    	VARCHAR(255),
  	cif     	VARCHAR(80),
  	telephone  	VARCHAR(20),
  	address  	VARCHAR(255),
  	account		VARCHAR(255)
	);