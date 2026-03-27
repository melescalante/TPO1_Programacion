from matrix import accounts, transactions, categories, budgets
def obtain_id_by_name(matrix, name):
    for raw in matrix:
        if raw[1] == name:
            return raw[0]
    return -1

def create_id(matrix):
    id=len(matrix) + 1
    return id

def add_account(account_name, total_money):
    id=create_id(accounts)
    for account in accounts:
        if account[1] == account_name:
            return
    accounts.append([id, account_name, total_money])
 
def add_category(category_name):
    id=create_id(categories)
    for category in categories:
        if category[1] == category_name:
            return
    categories.append([id, category_name])
def delete_category(name):
    index=0
    id_category=obtain_id_by_name(categories,name)
    for category in categories:
        if category[0]==id_category:
            index=categories.index(category)
            delete=categories.pop(index)
            print(delete, "Eliminado")
    print()
def add_budget(name_category, limit_amount):
    id=create_id(budgets)
    id_category=obtain_id_by_name(categories, name_category)
    if (id_category == -1):
        print("The category does not exist. Please create it.")
        return("The id category was not found ", name_category)
    for category in categories:
        if category[1] == name_category:
            budgets.append([id, id_category, limit_amount])
            return
def delete_budget(name):
    id_category= obtain_id_by_name(categories,name)
    index=0
    delete=[]
    for budget in budgets:
        if budget[1]==id_category:
            index=budgets.index(budget)
            delete=budgets.pop(index)
            print(delete)
    print()

def add_transaction(name_account, name_category, date, time, amount, description, month, transaction_type="income"):  
    id= create_id(transactions)
    id_account = obtain_id_by_name(accounts, name_account)
    id_category = obtain_id_by_name(categories, name_category)
    # Should throw exceptions
    # if transaction_type==None:transaction_type="income" 
    if (id_account == -1):
        print("The account does not exist. Please create it.")
        return("The id count was not found ", name_account)
        
    if (id_category == -1):
        print("The category does not exist. Please create it.")
        return("The id category was not found ", name_category)
    
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
        print(title, end="  \t")
    print()
   
    raws = len(matrix)
    cols = len(matrix[0])
    for raw in range(raws):
        for col in range(cols):
            print(matrix[raw][col], end="  \t")
        print()

# print_matrix(["id_cuenta", "Nombre", "Total"], accounts)
# print_matrix(["id_categoria", "Nombre"], categories)
# print_matrix(["id_presupuesto", "id_categoria", "Monto Limite"], budgets)
# print_matrix(["id_movimiento", "id_cuenta", "id_categoria","Fecha","Hora","Importe","Descripcion", "Mes"], transactions)
delete_budget("Ropa")
# Ejemplo con excepcion
# add_transaction("Galicia","1","2-3-2026","20:20",1200000,"Sueldo","Marzo")
# Ejemplo correcto
add_transaction("Galicia","Sueldo","2-3-2026","20:20",1200000,"Sueldo","Marzo")
add_account("BBVA", 1200000)
add_category("Ropa")
add_budget("Ropa", 12000)
delete_category("Sueldo")