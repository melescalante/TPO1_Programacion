def total_last_month(transactions):
    last_year = 0
    last_month = 0

    for i in transactions:
        date = i[3]
        day, month, year = date.split("-")

        month = int(month)
        year = int(year)

        if year > last_year or (year == last_year and month > last_month):
            last_year = year
            last_month = month

    total_expenses = 0

    for i in transactions:
        date = i[3]
        day, month, year = date.split("-")

        month = int(month)
        year = int(year)

        if month == last_month and year == last_year and i[5] < 0:
            total_expenses += i[5]

    return abs(total_expenses)

def average_month(transactions):
    total_month = {}

    for i in transactions:
        date = i[3]
        day, month, year = date.split("-")

        key = year + "-" + month  

        if i[5] < 0:
            if key not in total_month:
                total_month[key] = 0
            total_month[key] += i[5]

    if len(total_month) == 0:
        return 0

    total = sum(total_month.values())
    average = round(total / len(total_month), 2)

    return abs(average)