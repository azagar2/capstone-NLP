CREATE TABLE purchase_metadata(
	id serial primary key,
	listing text,
	weekday_bought smallint,
	weekday_event smallint,
	category smallint,
	cost_of_ticket double precision,
	days_before smallint
);