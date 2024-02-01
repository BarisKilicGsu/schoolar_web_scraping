-- Active: 1706448604919@@127.0.0.1@5433@cities
CREATE TABLE users (
    id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY, 
    orcid TEXT,
    name VARCHAR(255) NOT NULL,
    google_scholar_code TEXT,
    profile_url TEXT,
    is_found BOOLEAN DEFAULT FALSE
);


CREATE TABLE articles (
    id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY, 
    user_id bigint REFERENCES users(id),
    name VARCHAR(255),
    makale_kod VARCHAR(255),
    alinti_kod VARCHAR(255),
    alinti_sayisi INTEGER,
    makale_href VARCHAR(255),
    alinti_href VARCHAR(255),
    is_found BOOLEAN DEFAULT FALSE
);

CREATE TABLE alintilayan_makaleler (
    id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY, 
    article_id bigint REFERENCES articles(id),
    title VARCHAR(255),
    authors VARCHAR(255),
    journal VARCHAR(255),
    citation_info VARCHAR(255),
    alintilayan_makale_ek_divs VARCHAR(255),
    alintilayan_makale_href VARCHAR(255),
    alintilayan_makale_id VARCHAR(255)
);