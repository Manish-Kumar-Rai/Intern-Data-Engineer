USE books_db;


-- Creating Summary Table --
CREATE TABLE summary_table
AS
SELECT
	year AS publication_year,
    COUNT(*) AS book_count,
    ROUND(AVG(price),2) AS average_price
FROM books_raw
GROUP BY year
ORDER BY publication_year;

SELECT * FROM summary_table;


SELECT * FROM books_raw
LIMIT 100;

-- Counting total records in books_raw table
SELECT
	COUNT(*) AS total_book
FROM books_raw;

-- Counting total records in summary table
SELECT
	COUNT(*) AS total_record
FROM summary_table;
