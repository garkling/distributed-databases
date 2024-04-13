// GET ALL AUTHORS WITH BOOK AND GENRE INFO
MATCH (a:Author)<-[:WRITTEN_BY]-(b:Book)-[:IS_TYPE_OF]->(g:Genre)
WITH a.name AS `Author Name`, 
    a.nationality AS `Nationality`, 
    COLLECT(DISTINCT b.title) AS `Books`, 
    COLLECT(DISTINCT g.name) AS `Genres`
RETURN `Author Name`, `Nationality`, `Books`, `Genres`
ORDER BY `Author Name`