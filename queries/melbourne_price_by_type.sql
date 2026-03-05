SELECT Type, COUNT(*) AS n, AVG(Price) AS avg_price
FROM melbourne
WHERE Price IS NOT NULL
GROUP BY Type
ORDER BY avg_price DESC;
