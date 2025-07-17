# Weekly Sales Manager

A simple command-line manager to track and summarize weekly sales by brand and day.
Originally designed for a small fragrance store, but easily adaptable to any small business by modifying the product list.

## Features

* Add new sales with brand, day, and cost.
* View current week's report grouped by day and brand.
* View total revenue and number of items sold.
* Automatically create new weeks and close them when needed.
* View past weeks' reports.

## How to Use

1. Run the program:

   ```bash
   python3 main.py
   ```

2. Use the interactive menu to:

   * Add a new sale.
   * Generate weekly reports.
   * View past weeks.
   * Exit the program.

## Requirements

* Python 3.x
* SQLite3 (built-in in Python)

## Notes

* All data is stored in a local SQLite database (`sales.db`).
* You can customize the list of brands by editing the `brands` table in `database.py`.

---

You can easily customize this tool to better reflect the structure of your business.
