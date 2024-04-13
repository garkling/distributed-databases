//2. GET CUSTOMER ORDERS INFO GROUPED BY DATE
MATCH (:Customer {name: "Sarah Davis"})-[order:BOUGHT]->(book:Book)
WITH date(order.date) AS `Order Date`, SUM(order.price) AS `Order Total`, COLLECT(book.title) AS `Books` 
RETURN `Order Date`, `Order Total`, `Books`
ORDER BY `Order Date` DESC