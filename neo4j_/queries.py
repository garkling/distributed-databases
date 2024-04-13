query_dict = {
    "get_all": {"graph": """MATCH (n)-[r]-(m) RETURN n, r, m"""},
    "get_all_books": {
        "table": """
        MATCH (a:Author)<-[:WRITTEN_BY]-(b:Book)-[:IS_TYPE_OF]->(g:Genre)
        WITH 
            b.title AS `Book Title`, 
            b.publish_year AS `Publish Year`, 
            a.name AS `Author Name`, 
            a.nationality AS `Author Nationality`, 
            COLLECT(g.name) AS `Genres`
        RETURN `Book Title`, `Publish Year`, `Author Name`, `Author Nationality`, `Genres`
        ORDER BY `Book Title`
        """,
        "graph": """
            MATCH (a:Author)<-[w:WRITTEN_BY]-(b:Book)-[t:IS_TYPE_OF]->(g:Genre)
            RETURN a, w, b, t, g
        """
    },
    "get_all_authors": {
        "table": """
        MATCH (a:Author)<-[:WRITTEN_BY]-(b:Book)-[:IS_TYPE_OF]->(g:Genre)
        WITH 
            a.name AS `Author Name`, 
            a.nationality AS `Nationality`, 
            COLLECT(DISTINCT b.title) AS `Books`, 
            COLLECT(DISTINCT g.name) AS `Genres`
        RETURN `Author Name`, `Nationality`, `Books`, `Genres`
        ORDER BY `Author Name`
        """,
        "graph": """
            MATCH (a:Author)<-[w:WRITTEN_BY]-(b:Book)-[t:IS_TYPE_OF]->(g:Genre)
            RETURN a, w, b, t, g
        """
    },
    "get_all_customers": {
        "table": """
        MATCH (c:Customer)
        OPTIONAL MATCH (c)-[order:BOUGHT]->(b:Book)
        WITH c, ROUND(SUM(order.price), 2) AS `Money Spent`, COUNT(DISTINCT b) AS `Bought`
        OPTIONAL MATCH (c)-[:VIEWED]->(v:Book)
        WITH c.name AS `Customer Name`, `Bought`, `Money Spent`, COUNT(DISTINCT v) AS `Viewed`
        RETURN `Customer Name`, `Bought`, `Viewed`, `Viewed` - `Bought` AS `Viewed Not Bought`, `Money Spent`
        ORDER BY `Money Spent` DESC
        """,
        "graph": """
        MATCH (c:Customer)-[r:BOUGHT|VIEWED]->(b:Book)
        RETURN c, r, b
        """
    },
    "get_all_genres": {
        "table": """
        MATCH (g:Genre)
        RETURN g.name AS `Genre Name`
        ORDER BY `Genre Name`
        """,
        "graph": """
        MATCH (g:Genre)<-[t:IS_TYPE_OF]-(b:Book)
        RETURN g, t, b
        """
    },
    "get_customer_orders_info": {
        "table": """
        MATCH (:Customer {name: $value})-[order:BOUGHT]->(book:Book)
        WITH date(order.date) AS `Order Date`, order.price AS `Book Price`, book.title AS `Book Title` 
        RETURN `Order Date`, `Book Price`, `Book Title`
        ORDER BY `Order Date` DESC
        """,
        "graph": """
        MATCH (c:Customer {name: $value})-[order:BOUGHT]->(book:Book)
        RETURN c, order, book
        """
    },
    "get_customer_orders_grouped_by_date": {
        "table": """
        MATCH (:Customer {name: $value})-[order:BOUGHT]->(book:Book)
        WITH date(order.date) AS `Order Date`, SUM(order.price) AS `Order Total`, COLLECT(book.title) AS `Books` 
        RETURN `Order Date`, `Order Total`, `Books`
        ORDER BY `Order Date` DESC    
        """,
        "graph": """
        MATCH (c:Customer {name: $value})-[order:BOUGHT]->(book:Book)
        RETURN c, order, book
        """
    },
    "sum_price_for_customer": {
        "table": """
        MATCH (Customer {name: $value})-[order:BOUGHT]->(:Book)
        WITH COUNT(order) AS `Item Count`, ROUND(SUM(order.price), 2) AS `Order Total` 
        RETURN `Item Count`, `Order Total`
        """
    },
    "group_books_by_times_bought": {
        "table": """
        MATCH (b:Book)<-[order:BOUGHT]-(x) 
        WITH b.title AS `Book Title`, count(order) AS `How Many Times Bought`
        RETURN `Book Title`, `How Many Times Bought` 
        ORDER BY `How Many Times Bought` DESC
        """
    },
    "get_viewed_books_by_customer": {
        "table": """
        MATCH (c:Customer {name: $value})-[:VIEWED]->(viewed:Book),
            (viewed)-[:IS_TYPE_OF]->(viewedGenre:Genre),
            (viewed)-[:WRITTEN_BY]->(viewedAuthor:Author)

        WITH viewed.title AS `Book Viewed`, viewedAuthor.name AS `Book Author`, COLLECT(viewedGenre.name) AS `Book Genres`
        RETURN `Book Viewed`, `Book Author`, `Book Genres`
        """,
        "graph": """
        MATCH (c:Customer {name: $value})-[v:VIEWED]->(viewed:Book),
             (viewed)-[w:WRITTEN_BY]->(viewedAuthor:Author)
        RETURN c, v, w, viewed, viewedAuthor
        """
    },
    "get_books_bought_together_with_book": {
        "table": """
        MATCH (target:Book {title: $value})<-[targetOrder:BOUGHT]-(c:Customer),
        (a:Author)<-[:WRITTEN_BY]-(sameOrderBooks:Book)<-[sameOrder:BOUGHT {date: targetOrder.date}]-(c)

        WITH date(targetOrder.date) AS `Order Date`, sameOrderBooks.title AS `Book Title`, sameOrderBooks.publish_year AS `Publish Year`, a.name AS `Author Name`, a.nationality AS `Author Nationality`
        RETURN `Order Date`, `Book Title`, `Publish Year`, `Author Name`, `Author Nationality`
        ORDER BY `Order Date` DESC
        """,
        "graph": """
        MATCH (target:Book {title: $value})<-[targetOrder:BOUGHT]-(c:Customer),
            (a:Author)<-[w:WRITTEN_BY]-(sameOrderBooks:Book)<-[sameOrder:BOUGHT {date: targetOrder.date}]-(c)
        RETURN target, c, targetOrder, a, w, sameOrderBooks, sameOrder
        """
    },
    "get_customer_info_by_book_ordered": {
        "table": """
        MATCH (target:Book {title: $value})<-[targetOrder:BOUGHT]-(c:Customer)

        WITH c.name AS `Customer Name`, date(targetOrder.date) AS `Order Date`, targetOrder.price AS `Book Price`
        RETURN `Customer Name`, `Order Date`, `Book Price`
        """,
        "graph": """
        MATCH (target:Book {title: $value})<-[targetOrder:BOUGHT]-(c:Customer)
        RETURN target, targetOrder, c
        """
    },
    "get_viewed_not_bought_books_by_customer": {
        "table": """
        MATCH (c:Customer {name: $value})-[:VIEWED]->(viewed:Book),
            (viewed)-[:IS_TYPE_OF]->(viewedGenre:Genre),
            (viewed)-[:WRITTEN_BY]->(viewedAuthor:Author)
        WHERE NOT (c)-[:BOUGHT]->(viewed:Book)

        WITH viewed.title AS `Book Title`, viewedAuthor.name AS `Book Author`, COLLECT(viewedGenre.name) AS `Book Genres`
        RETURN `Book Title`, `Book Author`, `Book Genres`
        ORDER BY `Book Title`
        """,
        "graph": """
        MATCH (c:Customer {name: $value})-[v:VIEWED]->(viewed:Book),
            (viewed)-[t:IS_TYPE_OF]->(viewedGenre:Genre),
            (viewed)-[w:WRITTEN_BY]->(viewedAuthor:Author)
        WHERE NOT (c)-[:BOUGHT]->(viewed:Book)
        RETURN c, v, viewed, w, viewedAuthor, t, viewedGenre
        """
    },
    "get_orders_by_date": {
        "table": """
        MATCH (c:Customer)-[order:BOUGHT {date: $value}]->(b:Book)-[:WRITTEN_BY]->(a:Author)
        WITH c.name AS `Customer Name`, order.price AS `Book Price`, b.title AS `Book Title`, a.name AS `Author Name`
        RETURN `Customer Name`, `Book Price`, `Book Title`, `Author Name`
        """,
        "graph": """
        MATCH (c:Customer)-[order:BOUGHT {date: $value}]->(b:Book)-[w:WRITTEN_BY]->(a:Author)
        RETURN c, order, b, w, a
        """
    },
    "recommend_same_author_books_by_viewed": {
        "table": """
        MATCH (c:Customer {name: $value})-[:VIEWED]->(viewed:Book)-[:WRITTEN_BY]->(sharedAuthor:Author)
        WHERE NOT (c)-[:BOUGHT]->(viewed)
        WITH DISTINCT sharedAuthor, COUNT(sharedAuthor) as occ, c
        MATCH (sharedBook:Book)-[:WRITTEN_BY]->(sharedAuthor)
        WHERE NOT (c)-[:VIEWED]->(sharedBook)

        WITH sharedBook.title AS `Same Author Book`, sharedAuthor.name AS `Author`, occ AS `Occurrences` 
        RETURN `Same Author Book`, `Author`, `Occurrences`
        ORDER BY `Occurrences` DESC
        """,
        "graph": """
        MATCH (c:Customer {name: $value})-[v:VIEWED]->(viewed:Book)-[w1:WRITTEN_BY]->(sharedAuthor:Author)
        WHERE NOT (c)-[:BOUGHT]->(viewed)
        WITH DISTINCT sharedAuthor, COUNT(sharedAuthor) as occ, c, viewed, v, w1
        MATCH (sharedBook:Book)-[w2:WRITTEN_BY]->(sharedAuthor)
        WHERE NOT (c)-[:VIEWED]->(sharedBook)
        RETURN c, v, viewed, sharedAuthor, w1, w2, sharedBook
        """
    },
    "recommend_similar_books_based_on_customer_orders": {
        "table": """
        MATCH (c:Customer {name: $value})-[:BOUGHT]->(hasBooks:Book)-[:IS_TYPE_OF]->(genre:Genre), 
              (a:Author)<-[:WRITTEN_BY]-(similarBooks:Book WHERE NOT (c)-[:VIEWED]->(similarBooks))-[:IS_TYPE_OF]->(genre)

        WITH similarBooks.title AS `Recommended Book`, a.name AS `Author`, COUNT(genre) AS `Priority`
        RETURN `Recommended Book`, `Author`, `Priority`
        ORDER BY `Priority` DESC
        LIMIT 10
        """,
        "graph": """
        MATCH (c:Customer {name: $value})-[b:BOUGHT]->(hasBooks:Book)-[t1:IS_TYPE_OF]->(genre:Genre), 
              (a:Author)<-[w:WRITTEN_BY]-(similarBooks:Book WHERE NOT (c)-[:VIEWED]->(similarBooks))-[t2:IS_TYPE_OF]->(genre)
        RETURN c, b, hasBooks, t1, genre, a, w, t2, similarBooks
        """
    }
}

node_props = {
    "Book": "title",
    "Author": "name",
    "Genre": "name",
    "Customer": "name",
}

formats = ("table", "graph")
