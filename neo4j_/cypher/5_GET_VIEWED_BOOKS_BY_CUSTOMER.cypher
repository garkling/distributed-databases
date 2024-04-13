//5. GET VIEWED BOOKS BY CUSTOMER
MATCH (c:Customer {name: "Christopher Jones"})-[:VIEWED]->(viewed:Book),
    (viewed)-[:IS_TYPE_OF]->(viewedGenre:Genre),
    (viewed)-[:WRITTEN_BY]->(viewedAuthor:Author)

WITH viewed.title AS `Book Viewed`, viewedAuthor.name AS `Book Author`, COLLECT(viewedGenre.name) AS `Book Genres`
RETURN `Book Viewed`, `Book Author`, `Book Genres`