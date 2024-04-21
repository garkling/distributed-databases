#!/usr/bin/env bash
set -f

function cqlsh() {
  echo "cqlsh:store> $1;"
  sudo docker compose exec -it cassandra-1 cqlsh -k store -e "$1"
  echo
}

echo '_________________________________________________ITEMS_OPERATIONS________________________________________________'
read -rp "get_categories NEXT [press any to continue]"
echo '_________________________________________________get_categories__________________________________________________'

cqlsh "SELECT DISTINCT category FROM items"

echo '_________________________________________________________________________________________________________________'
read -rp "describe_items NEXT [press any to continue]"
echo '________________________________________________ describe_items__________________________________________________'

cqlsh "DESCRIBE TABLE items"

echo '_________________________________________________________________________________________________________________'
read -rp "get_items_sorted_by_price NEXT [press any to continue]"
echo '____________________________________________get_items_sorted_by_price____________________________________________'

cqlsh "SELECT * FROM items_by_price WHERE category = 'Laptops'"

echo '_________________________________________________________________________________________________________________'
read -rp "get_items_by_model NEXT [press any to continue]"
echo '________________________________________________get_items_by_model_______________________________________________'

cqlsh "SELECT * FROM items WHERE category = 'Smartphones' AND model LIKE '%Ultra%'"

echo '_________________________________________________________________________________________________________________'
read -rp "get_items_by_price_range NEXT [press any to continue]"
echo '_____________________________________________get_items_by_price_range____________________________________________'

cqlsh "SELECT * FROM items_by_price WHERE category = 'TV' AND price >= 1000 AND price <= 2000"

echo '_________________________________________________________________________________________________________________'
read -rp "get_items_by_price_by_brand NEXT [press any to continue]"
echo '___________________________________________get_items_by_price_by_brand___________________________________________'

cqlsh "SELECT * FROM items_by_price WHERE category = 'Laptops' AND price = 1299.99 AND brand = 'Dell'"

echo '_________________________________________________________________________________________________________________'
read -rp "get_items_by_property_key NEXT [press any to continue]"
echo '_____________________________________________get_items_by_property_key___________________________________________'

cqlsh "SELECT * FROM items WHERE category = 'Smartphones' and props CONTAINS KEY 'fast_charge'"

echo '_________________________________________________________________________________________________________________'
read -rp "get_items_by_property_value NEXT [press any to continue]"
echo '___________________________________________get_items_by_property_value___________________________________________'

cqlsh "SELECT * FROM items WHERE category = 'Laptops' and props['screen_matrix'] = 'IPS'"

echo '_________________________________________________________________________________________________________________'
read -rp "update_item_property NEXT [press any to continue]"
echo '______________________________________________update_item_property_______________________________________________'

cqlsh "UPDATE items
             SET props = props + {'color': 'Mystery Silver'}
             WHERE category = 'Smartphones' AND brand = 'Huawei' AND model = 'Huawei Mate 40 Pro'"

cqlsh "SELECT * FROM items WHERE category = 'Smartphones' AND brand = 'Huawei' AND model = 'Huawei Mate 40 Pro'"

echo '_________________________________________________________________________________________________________________'
read -rp "insert_item_property NEXT [press any to continue]"
echo '_______________________________________________insert_item_property______________________________________________'

cqlsh "UPDATE items
             SET props = props + {'stylus': 'Apple Pencil'}
             WHERE category = 'Tablets' AND brand = 'Apple' AND model = 'iPad Pro (12.9-inch, 5th Gen)'"

cqlsh "SELECT * FROM items WHERE category = 'Tablets' AND brand = 'Apple' AND model = 'iPad Pro (12.9-inch, 5th Gen)'"

echo '_________________________________________________________________________________________________________________'
read -rp "delete_item_property NEXT [press any to continue]"
echo '_______________________________________________delete_item_property______________________________________________'

cqlsh "UPDATE items
             SET props = props - {'os'}
             WHERE category = 'Laptops' AND brand = 'HP' AND model = 'HP Envy 15'"

cqlsh "SELECT * FROM items WHERE category = 'Laptops' AND brand = 'HP' AND model = 'HP Envy 15'"

echo '________________________________________________________________________________________________________________ '
read -rp "ORDER OPERATIONS NEXT [press any to continue]"





echo '________________________________________________ORDERS_OPERATIONS________________________________________________'
echo '_______________________________________________get_order_customers_______________________________________________'

cqlsh "SELECT DISTINCT customer_name FROM orders"

echo '_________________________________________________________________________________________________________________'
read -rp "describe_orders NEXT [press any to continue]"
echo '_________________________________________________describe_orders_________________________________________________'

cqlsh "DESCRIBE TABLE orders"

echo '_________________________________________________________________________________________________________________'
read -rp "get_orders NEXT [press any to continue]"
echo '____________________________________________________get_orders___________________________________________________'

cqlsh "SELECT * FROM orders WHERE customer_name = 'James Cooper'"

echo '_________________________________________________________________________________________________________________'
read -rp "get_orders_by_item_id NEXT [press any to continue]"
echo '______________________________________________get_orders_by_item_id______________________________________________'

get_orders_by_item_id_3="SELECT * FROM orders WHERE customer_name = 'Liam Harris' AND items CONTAINS"
cqlsh "SELECT items FROM orders WHERE customer_name = 'Liam Harris'"

echo "[INFO] Copy-parte a UUID for the next query"
read -rp "[PROMPT] $get_orders_by_item_id_3 " param
echo
cqlsh "$get_orders_by_item_id_3 $param"

echo '_________________________________________________________________________________________________________________'
read -rp "get_orders_by_date_range NEXT [press any to continue]"
echo '____________________________________________get_orders_by_date_range_____________________________________________'

cqlsh "SELECT order_date, order_total, items FROM orders
        WHERE customer_name = 'Liam Harris' AND order_date >= '2024-01-01 00:00:00' AND order_date <= '2024-12-31 00:00:00'"

echo '_________________________________________________________________________________________________________________'
read -rp "get_orders_total_sum_by_customers NEXT [press any to continue]"
echo '________________________________________get_orders_total_sum_by_customers________________________________________'

cqlsh "SELECT customer_name, SUM(order_total) AS total_total FROM orders GROUP BY customer_name"

echo '_________________________________________________________________________________________________________________'
read -rp "get_max_order_total_by_customers NEXT [press any to continue]"
echo '________________________________________get_max_order_total_by_customers_________________________________________'

cqlsh "SELECT customer_name, MAX(order_total) AS max_total, order_date, items FROM orders GROUP BY customer_name"

echo '_________________________________________________________________________________________________________________'
read -rp "insert_order_items NEXT [press any to continue]"
echo '_______________________________________________insert_order_items________________________________________________'

cqlsh "SELECT model, price, id FROM items"
echo "[INFO] Copy-paste items UUIDs from the above in {}, e.g. {fe361c5c-995f-4d58-b3bf-6e27845f8e87, cd7b6edb-a299-430d-9cc3-d139aee1dbd3}"
read -rp "[PROMPT] UPDATE orders SET items = items + " items_id
echo "[INFO] Enter the items total or a random int"
read -rp "[PROMPT] UPDATE orders SET items = items + $items_id, order_total = " order_total

echo "[BEFORE]"
cqlsh "SELECT * FROM orders
        WHERE customer_name = 'Sophia Martin' AND order_date = '2024-04-01 15:11:39'"

cqlsh "UPDATE orders SET items = items + $items_id, order_total = $order_total WHERE customer_name = 'Sophia Martin' AND order_date = '2024-04-01 15:11:39'"

echo "[AFTER]"
cqlsh "SELECT * FROM orders
        WHERE customer_name = 'Sophia Martin' AND order_date = '2024-04-01 15:11:39'"

echo '_________________________________________________________________________________________________________________'
read -rp "delete_order_items NEXT [press any to continue]"
echo '_______________________________________________delete_order_items________________________________________________'

cqlsh "SELECT items, order_total FROM orders
        WHERE customer_name = 'Ava Turner' AND order_date = '2023-11-11 19:44:12'"

echo "[INFO] Copy-paste items UUIDs from the above in {}, e.g. {fe361c5c-995f-4d58-b3bf-6e27845f8e87, cd7b6edb-a299-430d-9cc3-d139aee1dbd3}"
read -rp "[PROMPT] UPDATE orders SET items = items - " items_id
echo "[INFO] Enter the items total or a random int"
read -rp "[PROMPT] UPDATE orders SET items = items - $items_id, order_total = " order_total

cqlsh "UPDATE orders
        SET items = items - $items_id, order_total = $order_total
        WHERE customer_name = 'Ava Turner' AND order_date = '2023-11-11 19:44:12'"

cqlsh "SELECT items, order_total FROM orders WHERE customer_name = 'Ava Turner' AND order_date = '2023-11-11 19:44:12'"

echo '_________________________________________________________________________________________________________________'
read -rp "get_order_total_writetime NEXT [press any to continue]"
echo '____________________________________________get_order_total_writetime____________________________________________'

cqlsh "SELECT id, order_date, WRITETIME(order_total) AS write_time FROM orders"

echo '_________________________________________________________________________________________________________________'
read -rp "insert_order_ttl NEXT [press any to continue]"
echo '________________________________________________insert_order_ttl_________________________________________________'

insert_order_ttl_9="INSERT INTO orders (customer_name, order_date, items, order_total, id) VALUES ('Mike Smith', '2024-04-15 22:59:59'"

cqlsh "SELECT model, price, id FROM items"
echo "[INFO] Copy-paste items UUIDs from the above in {}, e.g. {fe361c5c-995f-4d58-b3bf-6e27845f8e87, cd7b6edb-a299-430d-9cc3-d139aee1dbd3}"
read -rp "[PROMPT] $insert_order_ttl_9, " items
echo "[INFO] Enter the items total or a random int"
read -rp "[PROMPT] $insert_order_ttl_9 $items," total

cqlsh "$insert_order_ttl_9, $items, $total, 08b869dc-c791-4f46-b34d-e5ff0aaab02f) IF NOT EXISTS USING TTL 5"
cqlsh "SELECT * FROM orders WHERE customer_name = 'Mike Smith' AND order_date = '2024-04-15 22:59:59'"
echo "[INFO] Sleeping for 5 seconds"
sleep 5
cqlsh "SELECT * FROM orders WHERE customer_name = 'Mike Smith' AND order_date = '2024-04-15 22:59:59'"

echo '_________________________________________________________________________________________________________________'
read -rp "get_orders_in_json NEXT [press any to continue]"
echo '_______________________________________________get_orders_in_json________________________________________________'

cqlsh "SELECT JSON * FROM orders WHERE customer_name = 'Mia Rodriguez'"

echo '_________________________________________________________________________________________________________________'
read -rp "insert_order_json NEXT [press any to continue]"
echo '________________________________________________insert_order_json________________________________________________'

cqlsh "SELECT model, price, id FROM items"
insert_order_11="INSERT INTO orders JSON {
  \"customer_name\": \"Noah Young\",
  \"order_date\": \"2023-12-21 14:22:17\",
  "

echo "[INFO] Copy-paste items UUIDs from the above in double-quotes in [], e.g. [\"fe361c5c-995f-4d58-b3bf-6e27845f8e87\", \"cd7b6edb-a299-430d-9cc3-d139aee1dbd3\"]"
read -rp "[PROMPT] $insert_order_11\"items\": " items
read -rp "[PROMPT] $insert_order_11\"items\": $items,
  \"order_total\": " total
cqlsh "INSERT INTO orders JSON '{
  \"customer_name\": \"Noah Young\",
  \"order_date\": \"2023-12-21 14:22:17\",
  \"items\": $items,
  \"order_total\": $total,
  \"id\": \"0a242a5c-38b1-4793-9fa1-9da8f76f46e2\"
}' IF NOT EXISTS"
cqlsh "SELECT * FROM orders WHERE customer_name = 'Noah Young' AND order_date = '2023-12-21 14:22:17'"

echo '_________________________________________________________________________________________________________________'
