//RECOMMEND SAME AUTHOR BOOKS BY VIEWED
MATCH (c:Customer {name: "John Smith"})-[:VIEWED]->(viewed:Book)-[:WRITTEN_BY]->(sharedAuthor:Author)
WHERE NOT (c)-[:BOUGHT]->(viewed)
WITH DISTINCT sharedAuthor, COUNT(sharedAuthor) as occ, c
MATCH (sharedBook:Book)-[:WRITTEN_BY]->(sharedAuthor)
WHERE NOT (c)-[:VIEWED]->(sharedBook)
WITH sharedBook.title AS `Same Author Book`, sharedAuthor.name AS `Author`, occ AS `Occurrences` 
RETURN `Same Author Book`, `Author`, `Occurrences`
ORDER BY `Occurrences` DESC