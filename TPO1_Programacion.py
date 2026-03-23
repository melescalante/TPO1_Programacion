accounts = [[1, "Mercado Pago", 1000000], [2, "Galicia", 4395000], [3, "Efectivo", 500000]]
transactions = [[1, "2-3-2026", "20:20", 5000000, "Sueldo"], [2, "11-3-2026", "13:21", -5000, "Chocolate del Kiosco"], [3, "12-3-2026", "14:55", -200000, "Expensas"], [4, "13-3-2026", "00:02", -400000, "Matricula"]]
categories = [[1,"Sueldo"], [2, "Alimento"], [3, "Gastos mensuales"],[4,"Educación"]]
budgets = [[1,3,20000],[2,2,150000],[3,1,120000],[4,4,300000]]
 
def add_account(id, account_name, total_money):
    for account in accounts:
        if account[1] == account_name:
            return
    accounts.append([id, account_name, total_money])
 
def add_category(id, category_name):
    for category in categories:
        if category[1] == category_name:
            return
    categories.append([id, category_name])
   
def add_budget(id, name_category, limit_amount):
    for category in categories:
        if category[1] == name_category:
            budgets.append([id, name_category, limit_amount])
            return
 
def add_transaction_income(id, date, time, amount, account_name, description):    
    transactions.append([id, date, time, amount, account_name, description])
   
    for account in accounts:
        if account[1] == account_name:
            account[2] += amount
            return
 
def add_transaction_expense(id, date, time, amount, account_name, description):        
    transactions.append([id, date, time, -amount, account_name, description])
   
    for account in accounts:
        if account[1] == account_name:
            account[2] -= amount
            return
 
def print_matrix(titles, matrix):
    for title in titles:
        print(title, end="\t")
    print()
   
    raws = len(matrix)
    cols = len(matrix[0])
    for raw in range(raws):
        for col in range(cols):
            print(matrix[raw][col], end="\t")
        print()

 
print_matrix(["ID", "Nombre", "Total"], accounts)

