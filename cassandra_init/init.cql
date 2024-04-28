CREATE KEYSPACE IF NOT EXISTS main WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

USE main;

CREATE TABLE messages (
    message_id text,
    user_id text,
    text TEXT,
    product_category TEXT,
    classes MAP<TEXT, DOUBLE>,
    created_at TIMESTAMP,
    PRIMARY_KEY(message_id)
);

create table time_series (created_at date, class text, cnt int, primary key (created_at, class));
create table class_stats(class text primary key, cnt int);