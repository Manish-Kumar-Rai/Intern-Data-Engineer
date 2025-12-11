-- Names table
CREATE TABLE IF NOT EXISTS names (
    id SERIAL PRIMARY KEY,
    locale TEXT NOT NULL,
    name_type TEXT NOT NULL, -- 'first', 'middle', 'last', 'title'
    value TEXT NOT NULL,
    gender TEXT
);

-- Cities table
CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    locale TEXT NOT NULL,
    city TEXT NOT NULL,
    region TEXT,
    postal_code TEXT
);

-- Email domains
CREATE TABLE IF NOT EXISTS email_domains (
    id SERIAL PRIMARY KEY,
    locale TEXT NOT NULL,
    domain TEXT NOT NULL
);

-- Eye colors
CREATE TABLE IF NOT EXISTS eye_colors (
    id SERIAL PRIMARY KEY,
    locale TEXT NOT NULL,
    color TEXT NOT NULL
);

-- Phone formats
CREATE TABLE IF NOT EXISTS phone_formats (
    id SERIAL PRIMARY KEY,
    locale TEXT NOT NULL,
    format_pattern TEXT NOT NULL
);

-- Street names
CREATE TABLE IF NOT EXISTS street_names (
    id SERIAL PRIMARY KEY,
    locale TEXT NOT NULL,
    name TEXT NOT NULL
);

-- Street suffixes
CREATE TABLE IF NOT EXISTS street_suffixes (
    id SERIAL PRIMARY KEY,
    locale TEXT NOT NULL,
    suffix TEXT NOT NULL
);
