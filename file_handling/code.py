# Question-1
def read_marks(filename):
    marks = {}
    with open(filename, 'r') as file:
        for line in file:
            student_id, name, subject, score = line.strip().split(',')
            score = int(score)
            if student_id not in marks:
                marks[student_id] = {'name': name, 'scores': {}}
            marks[student_id]['scores'][subject] = score
    return marks

def calculate_marks(marks):
    report = {}
    for student_id, data in marks.items(): #studentid ante rollno, data lo {name,scores}
        scores = data['scores'] #scores ki okadict untadi with subject and scores as its key-value pair
        total = sum(scores.values())
        average = total / len(scores)
        highest_subject = max(scores)
        lowest_subject = min(scores)
        report[student_id] = {
            'name': data['name'],
            'total': total,
            'average': average,
            'highest': (highest_subject, scores[highest_subject]),
            'lowest': (lowest_subject, scores[lowest_subject])
        }
    return report

def write_report(report, filename):
    with open(filename, 'w') as file:
        for student_id, data in sorted(report.items(), key=lambda item: item[1]['average'], reverse=True): 
            #displays records in the descending order of avg of each student - sorted(report.items(),key = based on val,decending/ascending)
            file.write(f"Student ID: {student_id}\n")
            file.write(f"Name: {data['name']}\n")
            file.write(f"Total Marks: {data['total']}\n")
            file.write(f"Average Marks: {data['average']:.1f}\n")
            file.write(f"Highest Scored Subject: {data['highest'][0]} ({data['highest'][1]})\n")
            file.write(f"Lowest Scored Subject: {data['lowest'][0]} ({data['lowest'][1]})\n")
            file.write("--------------------------------------\n")

marks = read_marks("D:/Data_Engineer_Python_Training/Training files/file_handling/marks.txt") # marks = {rollno:{name:'',scores:{subjname:''}}}
report = calculate_marks(marks)
write_report(report, "D:/Data_Engineer_Python_Training/Training files/file_handling/report.txt")


# Question-2

""" import csv
from datetime import datetime

def calculate_expenses(file_name):
    total_expense = 0
    category_expense = {}
    daily_expense = {}

    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip the header row
        for row in reader:
            date = row[0]
            category = row[1]
            amount = float(row[2])

            total_expense += amount
            category_expense[category] = category_expense.get(category, 0) + amount
            daily_expense[date] = daily_expense.get(date, 0) + amount

    return total_expense, category_expense, daily_expense

def write_summary(total_expense, category_expense, daily_expense):
    highest_spending_day = max(daily_expense, key=daily_expense.get)
    month = datetime.strptime(highest_spending_day, '%Y-%m-%d').strftime('%B')
    year = datetime.strptime(highest_spending_day, '%Y-%m-%d').year

    with open('monthly_summary.txt', 'w', encoding='utf-8') as file:
        file.write(f"================= Expense Summary ({month} {year}) =================\n")
        file.write(f"Total Monthly Expense: ₹{total_expense:.2f}\n")
        file.write("Category-wise Breakdown:\n")
        for category, amount in category_expense.items():
            file.write(f"  {category} : ₹{amount:.2f}\n")
        file.write(f"Highest Spending Day: {highest_spending_day} (₹{daily_expense[highest_spending_day]:.2f})\n")

# Driver code
total_expense, category_expense, daily_expense = calculate_expenses("D:/Data_Engineer_Python_Training/Training files/file_handling/expenses.csv")
write_summary(total_expense, category_expense, daily_expense) """