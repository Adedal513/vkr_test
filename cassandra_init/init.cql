CREATE KEYSPACE IF NOT EXISTS main WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

USE main;

CREATE TABLE messages (
    message_id UUID PRIMARY KEY,
    message_text TEXT,
    product_category TEXT,
    classes MAP<TEXT, DOUBLE>,
    created_at TIMESTAMP
);