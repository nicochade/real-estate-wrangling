SELECT
  (SELECT COUNT(*) FROM melbourne) AS melbourne_rows,
  (SELECT COUNT(*) FROM airbnb_listings) AS airbnb_rows;
