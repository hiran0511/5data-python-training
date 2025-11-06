import json
import datetime
from functools import wraps

# ------------------- Decorator for Logging -------------------
def log_and_time(func):
    @wraps(func)
    def wrapper():
        start_time = datetime.datetime.now()
        print(f"\nFunction '{func.__name__}' started at {start_time}")
        func()
        end_time = datetime.datetime.now()
        total_time = (end_time - start_time).total_seconds()
        with open("app_log.txt", "a") as f:
            f.write(f"{start_time} - '{func.__name__}' executed in {total_time}s\n")
        print(f"Function '{func.__name__}' executed in {total_time}s")
    return wrapper

# ------------------- Add Expense -------------------
@log_and_time
def add_expense():
    try:
        with open("expenses.json", "r") as f:
            expenses = json.load(f)
    except FileNotFoundError:
        expenses = []

    # Get details from user
    date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date_input:
        date_input = datetime.date.today().isoformat()
    category = input("Enter category: ").strip()
    try:
        amount = float(input("Enter amount: ").strip())
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    description = input("Enter description: ").strip()

    # Add expense entry
    expenses.append({
        "date": date_input,
        "category": category,
        "amount": amount,
        "description": description
    })

    with open("expenses.json", "w") as f:
        json.dump(expenses, f, indent=4)

    print("✅ Expense added successfully!")

# ------------------- View All Expenses -------------------
@log_and_time
def view_expenses():
    try:
        with open("expenses.json", "r") as f:
            expenses = json.load(f)
    except FileNotFoundError:
        print("No expenses found yet.")
        return

    # Sort by date
    expenses.sort(key=lambda x: x["date"])
    total = sum(e["amount"] for e in expenses)

    print("\nAll Expenses:")
    print("-" * 50)
    for e in expenses:
        print(f"Date: {e['date']}, Category: {e['category']}, Amount: ₹{e['amount']}, Description: {e['description']}")
    print("-" * 50)
    print(f"Total Expenditure: ₹{total}")

# ------------------- Monthly Summary -------------------
@log_and_time
def monthly_summary():
    try:
        with open("expenses.json", "r") as f:
            expenses = json.load(f)
    except FileNotFoundError:
        print("No expenses found yet.")
        return

    # Get month & year
    month = int(input("Enter month (MM): "))
    year = int(input("Enter year (YYYY): "))

    monthly = []
    for e in expenses:
        try:
            dt = datetime.datetime.strptime(e["date"], "%Y-%m-%d")
        except ValueError:
            continue
        if dt.month == month and dt.year == year:
            monthly.append(e)

    if not monthly:
        print("No records found for this month.")
        return

    summary = {}
    for e in monthly:
        summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]

    print(f"\n📅 Monthly Summary: {datetime.date(year, month, 1).strftime('%B')} {year}")
    print("-" * 40)
    for cat, amt in summary.items():
        print(f"{cat}: ₹{amt}")
    print(f"Total: ₹{sum(summary.values())}")

# ------------------- Menu -------------------
while True:
    print("\n💰 Smart Expense Tracker 💰")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Monthly Summary")
    print("4. Exit")
    choice = input("Enter your choice (1/2/3/4): ").strip()

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        monthly_summary()
    elif choice == "4":
        print("✅ Exited Successfully. Goodbye!")
        break
    else:
        print("❌ Invalid choice. Try again.")
