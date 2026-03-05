SELECT zipcode, COUNT(*) AS n,
       AVG(CAST(REPLACE(REPLACE(price,'$',''),',','') AS REAL)) AS avg_price
FROM airbnb_listings
WHERE zipcode IS NOT NULL AND price IS NOT NULL
GROUP BY zipcode
HAVING n >= 5
ORDER BY avg_price DESC
LIMIT 10;
