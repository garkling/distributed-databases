//1. GET CUSTOMER ORDERS INFO
MATCH (:Customer {name: "Sarah Davis"})-[order:BOUGHT]->(book:Book)
WITH date(order.date) AS `Order Date`, order.price AS `Book Price`, book.title AS `Book Title` 
RETURN `Order Date`, `Book Price`, `Book Title`
ORDER BY `Order Date` DESC