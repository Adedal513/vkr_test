CREATE KEYSPACE IF NOT EXISTS main WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

USE main;

CREATE TABLE messages (message_id text, user_id text, text TEXT, product_category TEXT, classes MAP<TEXT, DOUBLE>, created_at TIMESTAMP, PRIMARY KEY(message_id));

create table time_series (created_at date, class text, cnt int, primary key (created_at, class));
create table class_stats(class text primary key, cnt int);
create table avg_probs(class text primary key, avg_prob double);
create table day_stats(time time, normal int, toxic int, primary key (time));
create table product_category_stats(product_category text, class text, amount int, PRIMARY KEY(product_category, class));