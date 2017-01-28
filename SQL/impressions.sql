CREATE TYPE impressionType AS ENUM ('click', 'buy', 'exclude');
CREATE TABLE Impressions(
	id serial primary key,
	userId BIGINT NOT NULL,
	type impressionType NOT NULL,
	time timestamp without time zone default (now() at time zone 'utc')
);