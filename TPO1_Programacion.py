from matrix import accounts, transactions, categories, budgets

MAX_SPACES = 110

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

def delete_account(account):
    index=0
    id_account=obtain_id_by_name(accounts,account)
    for acc in accounts:
        if acc[0]==id_account:
            index=accounts.index(acc)
            delete=accounts.pop(index)
            print("Eliminado")
    print()
    
def return_money_to_account(accounts, id_account, total_money):
    for account in accounts:
        if account[0] == id_account:
            total_money *= -1 # Invierte el monto para devolver al resultado anterior a la cuenta.
            account[2] += total_money
            return

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
            print("\033[32mOperación realizada con éxito.\033[0m")
    print()

def add_budget(name_category, limit_amount):
    id=create_id(budgets)
    id_category=obtain_id_by_name(categories, name_category)
    if (id_category == -1):
        print("\033[31mThe category does not exist. Please create it.\033[0m")
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
            print("\033[32mOperación realizada con éxito\033[0m")
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

def delete_transaction():
    print_transactions(transactions)
    id=int(input("Que transaccion deseas eliminar? Indique el numero: "))
    
    for transaction in transactions:
        if transaction[0]==id:
            index=transactions.index(transaction)
            delete=transactions.pop(index)
            id_account = delete[1]
            total_money = delete[5]
            return_money_to_account(accounts, id_account, total_money)
            print_transactions(transactions)
            print("\033[32mOperación realizada con éxito.\033[0m")
            return
        
    print("\033[31mOperación realizada sin éxito, el número de ID no existe.\033[0m")

def print_transactions(matrix_transactions):
    RESET = "\033[0m"
    BOLD  = "\033[1m"
    print("="*MAX_SPACES)
    print(f'{"Transacciones":^110}')
    print("="*MAX_SPACES)
    print(f"{BOLD}{'Numero':<8}{'Cuenta':<15}{'Categoria':<15}{'Fecha':<15}{'Hora':<10}{'Monto':<15}{'Descripcion':<20}{'Mes':<15}{RESET}")
    for i in range(len(matrix_transactions)):
        id=matrix_transactions[i][0]
        cuenta = matrix_transactions[i][1]
        categoria = matrix_transactions[i][2]
        fecha =  matrix_transactions[i][3]
        hora =  matrix_transactions[i][4]
        monto = "$"+ str(matrix_transactions[i][5])
        desc =  matrix_transactions[i][6]
        mes =  matrix_transactions[i][7]
        print(f"{BOLD}{id:<8}{RESET}{cuenta:<15}{categoria:<15}{fecha:<15}{hora:<10}{monto:<15}{desc:<20}{mes:<15}")
    print()

delete_budget("Ropa")
# Ejemplo con excepcion
add_transaction("Galicia","1","2-3-2026","20:20",1200000,"Sueldo","Marzo")
delete_transaction()
# Ejemplo correcto
add_transaction("Galicia","Sueldo","2-3-2026","20:20",1200000,"Sueldo","Marzo")
add_account("BBVA", 1200000)
add_category("Ropa")