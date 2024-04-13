//7. GET CUSTOMER INFO BY BOOK ORDER
MATCH (target:Book {title: "The Da Vinci Code"})<-[targetOrder:BOUGHT]-(c:Customer)

WITH c.name AS `Customer Name`, date(targetOrder.date) AS `Order Date`, targetOrder.price AS `Book Price`
RETURN `Customer Name`, `Order Date`, `Book Price`