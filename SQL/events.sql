CREATE TABLE Events(
	id serial primary key,
	type varchar NOT NULL,
	currency varchar NOT NULL,
	category varchar NOT NULL,
	startTime timestamp default NULL,
	endTime timestamp default NULL,
	eventId integer,
	price float,
	title text,
	description text,
	longitude Double Precision,
	latitude Double Precision,
	api varchar,
	genre varchar,
	subGenre varchar,
	city varchar,
	country varchar
);