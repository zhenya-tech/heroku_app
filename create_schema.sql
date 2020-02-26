CREATE TABLE IF NOT EXISTS users
(
    id integer primary key autoincrement not null,
    name text not null,
    viber_id text not null unique
);

CREATE TABLE IF NOT EXISTS words
(
    id integer primary key autoincrement not null,
    word text not null,
    translation text not null,
    examples text not null
);

CREATE TABLE IF NOT EXISTS learning
(
    user_id integer not null,
    word_id integer not null,
    right_answer integer not null default 0,
    time_last_answer timestamp null,
    primary key(user_id, word_id),
    foreign key(user_id) references users(id),
    foreign key(word_id) references words(id)
);

CREATE TABLE IF NOT EXISTS round
(
    id integer primary key autoincrement not null,
    user_id integer not null,
    count_answers integer not null,
    correct_count integer not null,
    time_round timestamp null,
    foreign key(user_id) references users(id)
)