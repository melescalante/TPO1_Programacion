accounts = [[1, "Mercado Pago", 1000000], 
            [2, "Galicia", 4395000],
            [3, "Efectivo", 500000]]
transactions = [[1, 2, 1, "2-3-2026", "20:20", 5000000, "Sueldo", "Marzo"], 
                [2, 3, 3, "11-3-2026", "13:21", -5000, "Chocolate del Kiosco", "Marzo"], 
                [3, 1, 2, "12-3-2026", "14:55", -200000, "Expensas", "Marzo"], 
                [4, 2, 4, "13-3-2026", "00:02", -400000, "Matricula", "Marzo"]]
categories = [[1, "Sueldo"], 
              [2, "Alimento"], 
              [3, "Gastos mensuales"],
              [4, "Educación"]]
budgets = [[1, 3, 20000], 
           [2, 2, 150000], 
           [3, 1, 120000], 
           [4, 4, 300000]]
 
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
 
def add_transaction(id, name_account, name_category, date, time, amount, description, month, transaction_type):    
    id_account = obtain_id_by_name(accounts, name_account)
    id_category = obtain_id_by_name(categories, name_category)
    
    # Should throw exceptions
    if (id_account == 0):
        print("The id count was not found ", name_account)
        return
    if (id_category == 0):
        print("The id category was not found ", name_category)
        return
    
    multiplier = 1
    if transaction_type == "expense":
        multiplier = -1
    final_amount = amount * multiplier
    
    transactions.append([id, id_account, id_category, date, time, final_amount, description, month])
    
    # Modificar saldo del id de la cuenta
    account = accounts[id_account]
    account[2] += final_amount
 
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
        
def obtain_id_by_name(matrix, name):
    for raw in matrix:
        if raw[1] == name:
            return raw[0]
        
    return -1
 
print_matrix(["ID", "Nombre", "Total"], accounts)