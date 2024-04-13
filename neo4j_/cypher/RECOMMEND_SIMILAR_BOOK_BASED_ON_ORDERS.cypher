//RECOMMEND SIMILAR BOOK BASED ON ORDERS
MATCH (c:Customer {name: 'Mike Martinez'})-[:BOUGHT]->(hasBooks:Book)-[:IS_TYPE_OF]->(genre:Genre), 
      (a:Author)<-[:WRITTEN_BY]-(similarBooks:Book WHERE NOT (c)-[:VIEWED]->(similarBooks))-[:IS_TYPE_OF]->(genre)
WITH similarBooks.title AS `Recommended Book`, a.name AS `Author`, COUNT(genre) AS `Priority`
RETURN `Recommended Book`, `Author`, `Priority`
ORDER BY `Priority` DESC
LIMIT 10