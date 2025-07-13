import os
import sqlite3

from database import initialize_database
from sales import add_sale, get_brands
from weeks import close_current_week, get_current_week, get_current_week_range


def main():
    DB_PATH = "data/sales.db"
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    initialize_database(conn)

    while True:
        print("\n--------- SALES MANAGER ---------")
        print("1. Add Sale")
        print("2. Generate Current Week Report")
        print("3. View Past Weeks")
        print("4. Exit")

        option = input("Choose an option: ").strip()

        if option == "1":
            add_sale_menu(conn)
        elif option == "2":
            generate_current_week_report(conn)
        elif option == "3":
            view_past_weeks(conn)
        elif option == "4":
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")

    conn.close()


def add_sale_menu(conn):
    start_date, _ = get_current_week_range()
    week = get_current_week(conn, start_date)

    if not week:
        print("No active week found.")
        return

    if week[3] == "close":
        print("The week is closed.")
        return

    week_id = week[0]
    days_list = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    while True:
        print("/n Select the day of the week:")
        for i, day in enumerate(days_list, 1):
            print(f"{i}. {day}")
        print("0. Return to the main menu")

        try:
            day_choice = int(input("Chose day: "))

            if day_choice == 0:
                return
            if 1 <= day_choice <= 7:
                selected_day = days_list[day_choice - 1]
            else:
                print("Invalid option.")
                continue
        except ValueError:
            print("Enter a valid number.")
            continue

        # Loop for multiple sales for the selected day
        while True:
            brands = get_brands(conn)
            print("\n Available brands:")
            for i, (_, name) in enumerate(brands, 1):
                print(f"{i}. {name}")
            print("0. Return to Day Selection")

            try:
                brand_choise = int(input("Select brand: "))
                if brand_choise == 0:
                    break
                if 1 <= brand_choise <= len(brands):
                    brand_id = brands[brand_choise - 1][0]
                else:
                    print("Invalid option.")
                    continue
            except ValueError:
                print("Enter a valid number.")
                continue

            try:
                cost = float(input("Enter sale cost: "))
            except ValueError:
                print("Invalid cost. Must be a number.")
                continue

            add_sale(conn, week_id, selected_day, brand_id, cost)
            print("Sale registerd.")


def generate_current_week_report(conn):
    start_date, _ = get_current_week_range()
    week = get_current_week(conn, start_date)

    if not week:
        print("No active week found.")
        return
    if week[3] == "close":
        print("The week is already closed.")
        print("Showing the final report ... \n")

    week_id = week[0]

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT sales.day, brands.name, sales.cost
        FROM sales
        JOIN brands on sales.brand_id = brands.brand_id
        WHERE sales.week_id = ?
        ORDER BY sales.day, brands.name;
        """,
        (week_id,),
    )
    rows = cursor.fetchall()
    if not rows:
        print("No sales for this week")
        return

    print("\n Weekly sales report:")
    daily_totals = {}
    total_amount = 0.0
    total_count = 0

    for day, brand, cost in rows:
        daily_totals.setdefault(day, []).append((brand, cost))
        total_amount += cost
        total_count += 1

    for day in sorted(daily_totals.keys()):
        print(f"\n {day}")
        day_total = 0
        for brand, cost in daily_totals[day]:
            print(f"    - {brand}: ${cost:.2f}")
            day_total += cost
        print(f"   Total for {day}: ${day_total:.2f}")

    print("\n==========================")
    print(f"Total sales: {total_count} items")
    print(f"Total revenue: {total_amount:.2f}")
    print("==========================\n")

    if week[3] == "close":
        return

    choice = input("Do you want to close this week? [y/n]: ").strip().lower()
    if choice == "y":
        close_current_week(conn, start_date)
        print("Week closed.")
    else:
        print("Week remains open.")
