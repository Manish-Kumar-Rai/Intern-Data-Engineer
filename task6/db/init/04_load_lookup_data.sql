-- Table: names
\COPY names(locale, name_type, value, gender)
FROM '/docker-entrypoint-initdb.d/data/names.csv'
WITH (FORMAT csv, HEADER true);

-- Table: cities
\COPY cities(locale, city, region, postal_code)
FROM '/docker-entrypoint-initdb.d/data/cities.csv'
WITH (FORMAT csv, HEADER true);

-- Table: email_domains
\COPY email_domains(locale, domain)
FROM '/docker-entrypoint-initdb.d/data/email_domains.csv'
WITH (FORMAT csv, HEADER true);

-- Table: eye_colors
\COPY eye_colors(locale, color)
FROM '/docker-entrypoint-initdb.d/data/eye_colors.csv'
WITH (FORMAT csv, HEADER true);

-- Table: phone_formats
\COPY phone_formats(locale, format_pattern)
FROM '/docker-entrypoint-initdb.d/data/phone_formats.csv'
WITH (FORMAT csv, HEADER true);

-- Table: street_names
\COPY street_names(locale, name)
FROM '/docker-entrypoint-initdb.d/data/streets.csv'
WITH (FORMAT csv, HEADER true);

-- Table: street_suffixes
\COPY street_suffixes(locale, suffix)
FROM '/docker-entrypoint-initdb.d/data/street_suffixes.csv'
WITH (FORMAT csv, HEADER true);
