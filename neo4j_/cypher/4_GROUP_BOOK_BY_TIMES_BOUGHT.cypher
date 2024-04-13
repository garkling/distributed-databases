//4. GROUP BOOK BY TIMES BOUGHT
MATCH (b:Book)<-[order:BOUGHT]-(x) 
WITH b.title AS `Book Title`, count(order) AS `How Many Times Bought`
RETURN `Book Title`, `How Many Times Bought` ORDER BY `How Many Times Bought` DESC