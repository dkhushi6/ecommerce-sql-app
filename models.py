import sqlite3

DB = "ecommerce.db"


def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = connect()
    with open("schema.sql") as f:
        conn.executescript(f.read())
    with open("seed.sql") as f:
        conn.executescript(f.read())
    conn.close()
    print("Database initialized with sample data.\n")


def all_orders(conn):
    return conn.execute("""
        SELECT o.id AS order_id, c.name AS customer, o.status, o.total, o.created_at
        FROM orders o
        JOIN customers c ON c.id = o.customer_id
        ORDER BY o.id
    """).fetchall()


def order_details(conn, order_id):
    return conn.execute("""
        SELECT oi.order_id, p.name AS product, oi.quantity, oi.unit_price,
               (oi.quantity * oi.unit_price) AS subtotal
        FROM order_items oi
        JOIN products p ON p.id = oi.product_id
        WHERE oi.order_id = ?
    """, (order_id,)).fetchall()


def all_returns(conn):
    return conn.execute("""
        SELECT r.id, r.order_id, c.name AS customer, p.name AS product,
               r.reason, r.status, r.created_at
        FROM returns r
        JOIN orders o ON o.id = r.order_id
        JOIN customers c ON c.id = o.customer_id
        JOIN products p ON p.id = r.product_id
        ORDER BY r.id
    """).fetchall()


def place_order(conn, customer_id, items):
    """items = list of (product_id, quantity)"""
    total = 0
    item_data = []
    for pid, qty in items:
        row = conn.execute("SELECT price, stock FROM products WHERE id = ?", (pid,)).fetchone()
        if not row:
            return None, f"Product {pid} not found."
        if row["stock"] < qty:
            return None, f"Insufficient stock for product {pid}."
        total += row["price"] * qty
        item_data.append((pid, qty, row["price"]))

    cur = conn.execute("INSERT INTO orders (customer_id, status, total) VALUES (?, 'pending', ?)",
                       (customer_id, total))
    order_id = cur.lastrowid
    for pid, qty, price in item_data:
        conn.execute("INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?,?,?,?)",
                     (order_id, pid, qty, price))
        conn.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (qty, pid))
    conn.commit()
    return order_id, total


def update_order_status(conn, order_id, status):
    valid = {'pending', 'shipped', 'delivered', 'cancelled'}
    if status not in valid:
        return False, f"Invalid status. Choose from: {valid}"
    conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    conn.commit()
    return True, None


def request_return(conn, order_id, product_id, reason):
    exists = conn.execute(
        "SELECT 1 FROM order_items WHERE order_id = ? AND product_id = ?",
        (order_id, product_id)
    ).fetchone()
    if not exists:
        return False, "Product not found in this order."
    conn.execute(
        "INSERT INTO returns (order_id, product_id, reason) VALUES (?, ?, ?)",
        (order_id, product_id, reason)
    )
    conn.commit()
    return True, None


def update_return_status(conn, return_id, status):
    valid = {'requested', 'approved', 'rejected', 'refunded'}
    if status not in valid:
        return False, f"Invalid status. Choose from: {valid}"
    conn.execute("UPDATE returns SET status = ? WHERE id = ?", (status, return_id))
    conn.commit()
    return True, None


def sales_summary(conn):
    return conn.execute("""
        SELECT p.name AS product, p.category,
               SUM(oi.quantity) AS units_sold,
               SUM(oi.quantity * oi.unit_price) AS revenue
        FROM order_items oi
        JOIN products p ON p.id = oi.product_id
        JOIN orders o ON o.id = oi.order_id
        WHERE o.status != 'cancelled'
        GROUP BY p.id
        ORDER BY revenue DESC
    """).fetchall()


def customer_orders(conn, customer_id):
    rows = conn.execute("""
        SELECT o.id AS order_id, o.status, o.total, o.created_at
        FROM orders o
        WHERE o.customer_id = ?
        ORDER BY o.id
    """, (customer_id,)).fetchall()
    name = conn.execute("SELECT name FROM customers WHERE id = ?", (customer_id,)).fetchone()
    return rows, (name["name"] if name else f"Customer #{customer_id}")


def low_stock(conn, threshold=10):
    return conn.execute("""
        SELECT id, name, category, stock
        FROM products
        WHERE stock <= ?
        ORDER BY stock
    """, (threshold,)).fetchall()
