# ecommerce-sql-app

A command-line e-commerce order and returns management system backed by SQLite.

## Features

- Place orders with automatic stock deduction and total calculation
- Update order status (`pending` → `shipped` → `delivered` / `cancelled`)
- Request and manage product returns with status tracking
- View sales summary (revenue and units sold per product, excluding cancelled orders)
- Look up all orders for a specific customer
- Low stock report with configurable threshold

## Tech Stack

- **Python 3** — application logic and CLI interface
- **SQLite** — embedded relational database (`ecommerce.db`)
- No external dependencies required

## Database Schema

| Table | Description |
|---|---|
| `customers` | Customer name, email, phone |
| `products` | Product name, category, price, stock level |
| `orders` | Order linked to customer, with status and total |
| `order_items` | Line items linking orders to products |
| `returns` | Return requests linked to order + product |

ER diagram:

![ER Diagram](er_diagram.png)

## Setup

```bash
# Clone the repo
git clone <repo-url>
cd ecommerce-sql-app

# Run the app (database is created automatically on first launch)
python app.py
```

No dependencies to install — uses only the Python standard library.

## Usage

On first run, the database is initialized from `schema.sql` and seeded with sample data from `seed.sql`.

```
╔══════════════════════════════════════╗
║   E-Commerce Order & Returns DB      ║
╠══════════════════════════════════════╣
║  1. View all orders                  ║
║  2. View order details               ║
║  3. Place new order                  ║
║  4. Update order status              ║
║  5. View all returns                 ║
║  6. Request a return                 ║
║  7. Update return status             ║
║  8. Sales summary                    ║
║  9. Customer orders                  ║
║ 10. Low stock report                 ║
║  0. Exit                             ║
╚══════════════════════════════════════╝
```

## Project Structure

```
ecommerce-sql-app/
├── app.py        # CLI entry point and menu logic
├── models.py     # Database connection and all SQL queries
├── schema.sql    # Table definitions
├── seed.sql      # Sample data
└── er_diagram.png
```

## Order & Return Statuses

**Orders:** `pending` → `shipped` → `delivered` | `cancelled`

**Returns:** `requested` → `approved` → `refunded` | `rejected`
