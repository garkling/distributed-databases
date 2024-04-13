//9. GET ORDERS BY DATE
MATCH (c:Customer)-[order:BOUGHT {date: "2023-11-03"}]->(b:Book)-[:WRITTEN_BY]->(a:Author)
WITH c.name AS `Customer Name`, order.price AS `Book Price`, b.title AS `Book Title`, a.name AS `Author Name`
RETURN `Customer Name`, `Book Price`, `Book Title`, `Author Name`