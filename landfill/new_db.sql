drop table if exists movies;
create table movies(
	id integer primary key autoincrement,
	filename varchar(255),
	title text,
	year integer,
	meta text,
	thumb text
);

