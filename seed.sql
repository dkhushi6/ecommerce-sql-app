-- Sample Data

INSERT INTO customers (name, email, phone) VALUES
('Alice Johnson', 'alice@example.com', '555-1001'),
('Bob Smith',     'bob@example.com',   '555-1002'),
('Carol White',   'carol@example.com', '555-1003'),
('David Brown',   'david@example.com', '555-1004');

INSERT INTO products (name, category, price, stock) VALUES
('Wireless Headphones', 'Electronics', 79.99,  50),
('Running Shoes',       'Footwear',    59.99, 100),
('Coffee Maker',        'Appliances', 49.99,  30),
('Backpack',            'Bags',        39.99,  75),
('Smartwatch',          'Electronics',129.99,  20);

INSERT INTO orders (customer_id, status, total) VALUES
(1, 'delivered', 159.98),
(2, 'shipped',    59.99),
(3, 'pending',    89.98),
(4, 'delivered',  79.99),
(1, 'cancelled',  49.99);

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 79.99),
(1, 2, 1, 59.99),
(2, 2, 1, 59.99),
(3, 4, 1, 39.99),
(3, 3, 1, 49.99),
(4, 1, 1, 79.99),
(5, 3, 1, 49.99);

INSERT INTO returns (order_id, product_id, reason, status) VALUES
(1, 2, 'Wrong size',      'approved'),
(4, 1, 'Defective item',  'refunded'),
(3, 4, 'Changed my mind', 'requested');
