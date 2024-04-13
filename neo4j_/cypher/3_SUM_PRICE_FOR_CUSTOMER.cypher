//3. SUM PRICE FOR CUSTOMER
MATCH (Customer {name: "Sarah Davis"})-[order:BOUGHT]->(:Book)
WITH COUNT(order) AS `Item Count`, ROUND(SUM(order.price), 2) AS `Order Total` 
RETURN `Item Count`, `Order Total`