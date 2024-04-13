//8. GET VIEWED NOT BOUGHT BOOK
MATCH (c:Customer {name: "Christopher Jones"})-[:VIEWED]->(viewed:Book),
    (viewed)-[:IS_TYPE_OF]->(viewedGenre:Genre),
    (viewed)-[:WRITTEN_BY]->(viewedAuthor:Author)
WHERE NOT (c)-[:BOUGHT]->(viewed:Book)

WITH viewed.title AS `Book Title`, viewedAuthor.name AS `Book Author`, COLLECT(viewedGenre.name) AS `Book Genres`
RETURN `Book Title`, `Book Author`, `Book Genres`
ORDER BY `Book Title`