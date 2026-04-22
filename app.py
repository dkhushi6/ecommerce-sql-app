import os
import models


def print_rows(rows, title=""):
    if title:
        print(f"\n--- {title} ---")
    if not rows:
        print("  (no results)")
        return
    rows = list(rows)
    cols = rows[0].keys()
    widths = {c: len(c) for c in cols}
    for row in rows:
        for c in cols:
            widths[c] = max(widths[c], len(str(row[c]) if row[c] is not None else "NULL"))
    header = "  ".join(c.ljust(widths[c]) for c in cols)
    print(header)
    print("-" * len(header))
    for row in rows:
        print("  ".join((str(row[c]) if row[c] is not None else "NULL").ljust(widths[c]) for c in cols))


MENU = """
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
"""


def main():
    fresh = not os.path.exists(models.DB)
    conn = models.connect()
    if fresh:
        models.init_db()
    else:
        with open("schema.sql") as f:
            conn.executescript(f.read())

    while True:
        print(MENU)
        choice = input("Select option: ").strip()

        if choice == "1":
            print_rows(models.all_orders(conn), "All Orders")

        elif choice == "2":
            oid = input("Order ID: ").strip()
            print_rows(models.order_details(conn, int(oid)), f"Order #{oid} Items")

        elif choice == "3":
            cid = input("Customer ID: ").strip()
            items = []
            while True:
                pid = input("  Product ID (blank to finish): ").strip()
                if not pid:
                    break
                qty = input("  Quantity: ").strip()
                items.append((int(pid), int(qty)))
            if items:
                order_id, result = models.place_order(conn, int(cid), items)
                if order_id:
                    print(f"\n  Order #{order_id} placed. Total: ${result:.2f}")
                else:
                    print(f"  {result}")

        elif choice == "4":
            oid = input("Order ID: ").strip()
            s = input("New status (pending/shipped/delivered/cancelled): ").strip()
            ok, err = models.update_order_status(conn, int(oid), s)
            if ok:
                print(f"\n  Order #{oid} status updated to '{s}'.")
            else:
                print(f"  {err}")

        elif choice == "5":
            print_rows(models.all_returns(conn), "All Returns")

        elif choice == "6":
            oid = input("Order ID: ").strip()
            pid = input("Product ID: ").strip()
            reason = input("Reason: ").strip()
            ok, err = models.request_return(conn, int(oid), int(pid), reason)
            if ok:
                print(f"\n  Return requested for product #{pid} in order #{oid}.")
            else:
                print(f"  {err}")

        elif choice == "7":
            rid = input("Return ID: ").strip()
            s = input("New status (requested/approved/rejected/refunded): ").strip()
            ok, err = models.update_return_status(conn, int(rid), s)
            if ok:
                print(f"\n  Return #{rid} status updated to '{s}'.")
            else:
                print(f"  {err}")

        elif choice == "8":
            print_rows(models.sales_summary(conn), "Sales Summary (excluding cancelled)")

        elif choice == "9":
            cid = input("Customer ID: ").strip()
            rows, title = models.customer_orders(conn, int(cid))
            print_rows(rows, f"Orders for {title}")

        elif choice == "10":
            t = input("Stock threshold (default 10): ").strip()
            print_rows(models.low_stock(conn, int(t) if t else 10), f"Low Stock (≤ {t or 10} units)")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("  Invalid option.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
