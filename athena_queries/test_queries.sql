-- example.sql
SELECT COUNT(*) FROM ecommerce_db.customers;

SELECT country, SUM(purchase_amount)
FROM ecommerce_db.customers
GROUP BY country
ORDER BY SUM(purchase_amount) DESC;
