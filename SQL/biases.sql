CREATE TYPE biasType AS ENUM ('admin', 'promotion', 'exclude');
CREATE TABLE Biases(
	id serial primary key,
	eventId BIGINT NOT NULL,
	type biasType NOT NULL,
	weight smallInt NOT NULL,
	startTime timestamp default (now() at time zone 'utc'),
	endTime timestamp default NULL,
	created timestamp without time zone default (now() at time zone 'utc')
);