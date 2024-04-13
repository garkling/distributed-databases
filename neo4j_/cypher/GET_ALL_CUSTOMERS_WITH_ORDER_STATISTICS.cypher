// GET ALL CUSTOMERS WITH ORDER STATISTICS
MATCH (c:Customer)
OPTIONAL MATCH (c)-[order:BOUGHT]->(b:Book)
WITH c, ROUND(SUM(order.price), 2) AS `Money Spent`, COUNT(DISTINCT b) AS `Bought`
OPTIONAL MATCH (c)-[:VIEWED]->(v:Book)
WITH c.name AS `Customer Name`, `Bought`, `Money Spent`, COUNT(DISTINCT v) AS `Viewed`
RETURN `Customer Name`, `Bought`, `Viewed`, `Viewed` - `Bought` AS `Viewed Not Bought`, `Money Spent`
ORDER BY `Money Spent` DESC