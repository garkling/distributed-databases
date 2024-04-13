// GET ALL BOOKS WITH AUTHOR AND GENRE INFO
MATCH (a:Author)<-[:WRITTEN_BY]-(b:Book)-[:IS_TYPE_OF]->(g:Genre)
WITH 
    b.title AS `Book Title`, 
    b.publish_year AS `Publish Year`, 
    a.name AS `Author Name`, 
    a.nationality AS `Author Nationality`, 
    COLLECT(g.name) AS `Genres`
RETURN `Book Title`, `Publish Year`, `Author Name`, `Author Nationality`, `Genres`
ORDER BY `Book Title`