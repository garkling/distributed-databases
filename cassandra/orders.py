customer_orders = {
    "Olivia Clark": {
        "2023-12-20 12:43:15": (
            "SELECT * FROM items WHERE category = 'Gaming Consoles' AND model LIKE '%PlayStation%'",
            "SELECT * FROM items WHERE category = 'TV' AND brand = 'LG' AND model = 'LG GX OLED'",
        ),
        "2024-01-20 11:00:31": (
            "SELECT * FROM items WHERE category = 'Smartphones' AND brand = 'Apple' AND model = 'iPhone 13 Pro Max'",
        ),
        "2024-04-01 15:11:39": (
            "SELECT * FROM items WHERE category = 'Laptops' AND brand = 'Alienware' AND model = 'm15 R6'",
            "SELECT * FROM items WHERE category = 'Laptops' AND brand = 'Lenovo' AND model = 'Legion 7i'",
        )
    },
    "Ethan White": {
        "2023-12-18 15:59:23": (
            "SELECT * FROM items WHERE category = 'Smartwatches' AND props['smartphone_sync'] = 'iOS 13+'",
        ),
        "2023-12-19 20:45:01": (
            "SELECT id, MIN(price) AS price FROM items WHERE category='Laptops' AND props['storage'] = '1TB SSD'",
            "SELECT * FROM items_by_price WHERE category='Headphones' AND price <= 200 ORDER BY price DESC LIMIT 1"
        ),
        "2024-03-15 01:31:08": (
            "SELECT * FROM items WHERE category = 'Smartwatches' AND model LIKE 'Samsung Galaxy%'",
            "SELECT * FROM items WHERE category = 'Smartphones' AND model = 'Samsung Galaxy S22 Ultra'"
        )
    },
    "Ava Turner": {
        "2023-11-11 19:44:12": (
            "SELECT * FROM items WHERE category = 'Smartphones' AND brand = 'Google' AND props CONTAINS KEY 'e_sim'",
            "SELECT * FROM items WHERE category = 'Tablets' AND brand = 'Samsung'",
            ("SELECT * FROM items_by_price WHERE category = 'Laptops' AND price >= 1500 AND price <= 2000", ('brand', 'Dell'))
        ),
        "2023-12-23 09:43:19": (
            "SELECT * FROM items WHERE category = 'TV' AND brand = 'Samsung' AND props['screen_size'] = '65 inches' LIMIT 1",
            "SELECT * FROM items WHERE category = 'Headphones' AND brand = 'Sennheiser' AND props['wireless'] = 'No'"
        )
    },
    "Liam Harris": {
        "2023-11-11 12:21:56": (
            "SELECT * FROM items_by_price WHERE category = 'Smartwatches' AND price >= 350 LIMIT 1",
            "SELECT * FROM items WHERE category = 'Smartphones' AND brand = 'Huawei' AND model = 'Huawei Nova 9'",
            "SELECT * FROM items WHERE category = 'Smartphones' AND brand = 'Huawei' AND model = 'Huawei P40'",
        ),
        "2024-01-27 08:17:32": (
            "SELECT * FROM items_by_price WHERE category = 'Tablets' AND price >= 400 AND price <= 500",
        ),
        "2024-04-15 03:11:41": (
            "SELECT * FROM items WHERE category = 'Laptops' AND brand = 'HP' AND props['battery'] = 'Up to 11 hours' LIMIT 1",
            "SELECT * FROM items WHERE category = 'Gaming Consoles' AND model = 'Nintendo Switch Lite'"
        ),
        "2024-04-17 05:51:04": (
            ("SELECT * FROM items_by_price WHERE category = 'Headphones' AND price <= 200", ("props", "color", "Blue")),
        )
    },
    "Sophia Martin": {
        "2024-01-18 17:34:06": (
            "SELECT * FROM items WHERE category = 'TV' AND props['HDR'] = 'Active HDR'",
            "SELECT * FROM items WHERE category = 'Gaming Consoles' AND brand = 'Microsoft' AND model = 'Xbox Series X'"
        ),
        "2024-04-01 15:11:39": (
            "SELECT * FROM items WHERE category = 'Laptops' AND model LIKE 'Predator%'",
        )
    },
    "Noah Young": {
        "2023-10-30 17:00:01": (
            "SELECT * FROM items WHERE category = 'Tablets' AND model LIKE 'iPad Pro%'",
        )
    },
    "Isabella Garcia": {
        "2024-02-13 21:03:22": (
            "SELECT * FROM items WHERE category = 'Smartphones' AND brand = 'Samsung' AND model = 'Samsung Galaxy S22 Ultra'",
        ),
        "2024-02-13 21:03:24": (
            "SELECT * FROM items WHERE category = 'Headphones' AND brand = 'Sony' AND model = 'Sony WH-1000XM4'",
        ),
        "2024-03-28 11:54:31": (
            "SELECT * FROM items WHERE category='TV' AND model LIKE '%NanoCel%'",
        ),
        "2024-04-11 13:41:43": (
            "SELECT * FROM items WHERE category='Gaming Consoles' AND brand = 'Nintendo' AND model = 'Nintendo Switch'",
        )
    },
    "Mason Lee": {
        "2023-12-02 16:17:43": (
            ("SELECT * FROM items_by_price WHERE category = 'Laptops' AND price <= 1200", ('model', 'Swift 5')),
        ),
        "2024-02-28 17:16:21": (
            "SELECT * FROM items WHERE category = 'Smartphones' AND brand = 'OnePlus' AND props['fast_charge'] = '20W'",
            "SELECT * FROM items WHERE category = 'Tablets' AND brand = 'Samsung' AND props CONTAINS KEY 'keyboard_support'"
        ),
        "2024-04-13 23:11:54": (
            "SELECT * FROM items WHERE category = 'Smartwatches' AND model LIKE '%Fit%'",
        )
    },
    "Mia Rodriguez": {
        "2023-12-30 07:13:57": (
            "SELECT id, MAX(price) AS price FROM items_by_price WHERE category = 'TV'",
        ),
        "2024-01-02 22:09:34": (
            "SELECT * FROM items WHERE category = 'Smartphones' AND model LIKE '%iPhone%'",
        )
    },
    "James Cooper": {
        "2023-12-17 19:03:41": (
            "SELECT * FROM items WHERE category = 'Smartphones' AND brand = 'Sony' AND props['storage'] = '256GB'",
            "SELECT * FROM items WHERE category = 'Headphones' AND model = 'Sennheiser HD 660 S'"
        ),
        "2024-02-04 18:54:13": (
            "SELECT * FROM items WHERE category = 'TV' AND props['refresh_rate'] = '120Hz' LIMIT 1",
        ),
        "2024-02-27 11:12:09": (
            "SELECT * FROM items WHERE category = 'Gaming Consoles' AND model = 'PlayStation 5'",
        ),
        "2024-02-27 14:54:23": (
            "SELECT id, MIN(price) AS price FROM items WHERE category = 'Headphones' AND props['type'] = 'True wireless earbuds'",
        ),
        "2024-04-02 13:43:05": (
            "SELECT * FROM items WHERE category = 'Smartwatches' AND model = 'Apple Watch Series 7'",
        )
    }
}