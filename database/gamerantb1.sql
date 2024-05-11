DROP DATABASE IF EXISTS gamerantb1;
CREATE DATABASE gamerantb1;

\c gamerantb1;

CREATE TABLE news_articles (
    article_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    publisher VARCHAR,
    title VARCHAR,
    keywords VARCHAR[],
    url VARCHAR
);