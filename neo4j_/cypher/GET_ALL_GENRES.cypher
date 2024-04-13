// GET ALL GENRES
MATCH (g:Genre)
RETURN g.name AS `Genre Name`
ORDER BY `Genre Name`