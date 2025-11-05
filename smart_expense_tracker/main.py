import json
import os
import time
import calendar
from datetime import datetime, date
from collections import defaultdict

# -------------------- File Names --------------------
EXP_FILE = "expenses.json"
LOG_FILE = "app_log.txt"

# -------------------- Utility: Read/Write --------------------
def read_expenses():
    """Read expenses from JSON file safely."""
    if not os.path.exists(EXP_FILE):
        return []
    try:
        with open(EXP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError):
        print("Warning: expenses.json corrupted or unreadable. Starting fresh.")
        return []

def write_expenses(expenses):
    """Write expenses to JSON file safely."""
    try:
        with open(EXP_FILE, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print("Error writing file:", e)

# -------------------- Decorator: Log + Time --------------------
def log_and_time(func):
    """Decorator to log function name and execution time."""
    def wrapper(*args, **kwargs):
        start = datetime.now()
        print(f"\nStarting '{func.__name__}' at {start.strftime('%Y-%m-%d %H:%M:%S')}")
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - t0
        log_line = f"{start.strftime('%Y-%m-%d %H:%M:%S')} - {func.__name__} executed in {duration:.4f}s\n"
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(log_line)
        return result
    return wrapper

# -------------------- Add Expense --------------------
@log_and_time
def add_expense():
    """Add a new expense entry."""
    raw_date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if raw_date == "":
        expense_date = date.today().isoformat()
    else:
        try:
            parsed = datetime.strptime(raw_date, "%Y-%m-%d")
            expense_date = parsed.date().isoformat()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

    category = input("Enter category (e.g., Food, Travel, Shopping, Bills): ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    raw_amount = input("Enter amount: ").strip()
    try:
        amount = float(raw_amount)
        if amount < 0:
            raise ValueError
    except ValueError:
        print("Invalid amount. Enter a positive number.")
        return

    description = input("Enter description (optional): ").strip()

    expenses = read_expenses()
    new_entry = {
        "date": expense_date,
        "category": category.title(),
        "amount": amount,
        "description": description
    }
    expenses.append(new_entry)
    write_expenses(expenses)
    print("✅ Expense added successfully!")

# -------------------- View Expenses --------------------
@log_and_time
def view_expenses():
    """View all expenses sorted by date."""
    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded.")
        return

    try:
        expenses_sorted = sorted(expenses, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))
    except Exception:
        expenses_sorted = expenses

    print(f"\n{'Date':<12} {'Category':<12} {'Amount':>10}  Description")
    print("-" * 60)
    total = 0.0
    for e in expenses_sorted:
        date_s = e.get("date", "")
        cat = e.get("category", "")
        amt = float(e.get("amount", 0))
        desc = e.get("description", "")
        total += amt
        print(f"{date_s:<12} {cat:<12} {amt:10.2f}  {desc}")
    print("-" * 60)
    print(f"{'Total:':<26} {total:10.2f}")

# -------------------- Monthly Summary --------------------
@log_and_time
def generate_monthly_summary():
    """Generate and optionally export monthly summary."""
    month_year = input("Enter month and year (MM YYYY) or press Enter for current month: ").strip()
    if month_year == "":
        today = datetime.today()
        month = today.month
        year = today.year
    else:
        try:
            mm, yyyy = month_year.split()
            month = int(mm)
            year = int(yyyy)
            if not (1 <= month <= 12):
                raise ValueError
        except ValueError:
            print("Invalid input. Enter like: 11 2025")
            return

    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded.")
        return

    summary = defaultdict(float)
    total = 0.0
    for e in expenses:
        try:
            d = datetime.strptime(e["date"], "%Y-%m-%d")
        except Exception:
            continue
        if d.year == year and d.month == month:
            amt = float(e.get("amount", 0))
            cat = e.get("category", "Uncategorized")
            summary[cat] += amt
            total += amt

    month_name = calendar.month_name[month]
    print(f"\n{'★'*5} Monthly Summary: {month_name} {year} {'★'*5}")
    if not summary:
        print("No expenses for this month.")
        return
    for cat, amt in summary.items():
        print(f"{cat}: ₹{amt:.2f}")
    print("-" * 40)
    print(f"Total: ₹{total:.2f}")

    export = input("Export summary to JSON file? (y/n): ").strip().lower()
    if export == "y":
        filename = f"summary_{month_name}_{year}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {"month": month, "year": year, "summary": dict(summary), "total": total},
                f, indent=2, ensure_ascii=False
            )
        print(f"Summary exported to '{filename}'")

# -------------------- Main Menu --------------------
def main():
    """Main program menu loop."""
    while True:
        print("\n" + "★" * 5 + " Smart Expense Tracker " + "★" * 5)
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Generate Monthly Summary")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            generate_monthly_summary()
        elif choice == "4":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Try again.")

# -------------------- Run Program --------------------
if __name__ == "__main__":
    main()
