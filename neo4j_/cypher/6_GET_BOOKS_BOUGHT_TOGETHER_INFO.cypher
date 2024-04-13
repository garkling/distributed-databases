//6. GET BOOKS BOUGHT TOGETHER INFO
MATCH (target:Book {title: "The Da Vinci Code"})<-[targetOrder:BOUGHT]-(c:Customer),
        (a:Author)<-[:WRITTEN_BY]-(sameOrderBooks:Book)<-[sameOrder:BOUGHT {date: targetOrder.date}]-(c) 

WITH date(targetOrder.date) AS `Order Date`, sameOrderBooks.title AS `Book Title`, sameOrderBooks.publish_year AS `Publish Year`, a.name AS `Author Name`, a.nationality AS `Author Nationality`
RETURN `Order Date`, `Book Title`, `Publish Year`, `Author Name`, `Author Nationality`
ORDER BY `Order Date` DESC