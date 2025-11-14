# EMPLOYEE PERFORMANCE ANALYTICS SYSTEM

#read lines from input file
def read_file(filename):
    try:
        with open(filename, "r") as file:
            return file.readlines()#returns as a list
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return []

#invalid rows into error_log.txt file
def log_error(line, message):
    with open("error_log.txt", "a") as log:
        log.write(f'Invalid row: "{line.strip()}" -> {message}\n')


#validate emp record line by line
def validate_record(line):
    try:
        parts = [p.strip() for p in line.split(",")]#creates a list
        if len(parts) != 4:
            log_error(line, "Incorrect number of fields")
            return None
        emp_id, name, dept, rating = parts

        #check empid
        if not emp_id.isdigit():
            log_error(line, "EmployeeID is not numeric")
            return None

        #check ename
        if name == "":
            log_error(line, "EmployeeName is empty")
            return None

        #check department
        if dept == "":
            log_error(line, "Department is empty")
            return None

        #check rating
        try:
            rating = float(rating)
            if not (1.0 <= rating <= 5.0):
                log_error(line, "Rating should be between 1.0 and 5.0")
                return None
        except ValueError:
            log_error(line, "Rating is not a valid float")
            return None

        return {
            "id": int(emp_id),
            "name": name,
            "dept": dept,
            "rating": rating
        }

    except Exception as e:
        log_error(line, f"Unexpected error: {str(e)}")
        return None

#find total no of valid emps, avg rating dept wise, top performer based on rating
def process_records(records):
    dept_ratings = {}
    top_employee = None

    for emp in records:
        dept = emp["dept"]
        rating = emp["rating"]

        #Department rating grouping
        if dept not in dept_ratings:
            dept_ratings[dept] = []
        dept_ratings[dept].append(rating)

        #top performer
        if top_employee is None or emp["rating"] > top_employee["rating"]:
            top_employee = emp

    return dept_ratings, top_employee

#write summary to performance_summary.txt
def write_summary(valid_records, dept_ratings, top_employee):
    with open("performance_summary.txt", "w") as out:
        out.write(f"Total Valid Employees: {len(valid_records)}\n\n")
        out.write("Average Ratings by Department:\n")

        for dept, ratings in dept_ratings.items():
            avg = sum(ratings) / len(ratings)
            out.write(f"{dept}: {avg:.2f}\n")

        out.write("\nTop Performer:\n")
        out.write(f"Employee Name: {top_employee['name']}\n")
        out.write(f"Department: {top_employee['dept']}\n")
        out.write(f"Rating: {top_employee['rating']}\n")

#main function
def main():
    filename = "employee_performance.txt"
    lines = read_file(filename)#reads file
    valid_records = []

    #check each record
    for line in lines:
        record = validate_record(line)
        if record:
            valid_records.append(record)

    #if no valid records, stop
    if not valid_records:
        print("No valid records found! Check error_log.txt")
        return

    #process valid records
    dept_ratings, top_employee = process_records(valid_records)

    #write summary
    write_summary(valid_records, dept_ratings, top_employee)

    print("Processing completed")
    print("Check performance_summary.txt and error_log.txt")
#run
main()
