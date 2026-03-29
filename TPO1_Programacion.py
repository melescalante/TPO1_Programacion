from matrix import accounts, transactions, categories, budgets

MAX_SPACES_TRANSACTIONS = 110
MAX_SPACES_BUDGETS =60
MAX_SPACES_CATEGORIES =50
# ANSI STYLES
RESET = "\033[0m"
BOLD  = "\033[1m"
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

def get_account_by_id(matrix_account, id_account):
    for raw in matrix_account:
        if raw[0] == id_account:
            return raw
    return None

def get_accounts(matrix_account):
    return

def update_account(matrix_account):
    get_accounts(matrix_account)
    id_account = int(input("¿Que cuenta desea actualizar? Indique el numero o escriba 0 para salir: "))
    if id_account == 0:
        print("\033[32mNo se actualizo ninguna cuenta.\033[0m")
        return

    account = get_account_by_id(matrix_account, id_account)
    while account is None:
        print("\033[31mLa cuenta no existe.\033[0m")

        id_account = int(input("¿Que cuenta desea actualizar? Indique el numero o escriba 0 para salir: "))
        if id_account == 0:
            print("\033[32mNo se actualizo ninguna cuenta.\033[0m")
            return
                
        account = get_account_by_id(matrix_account, id_account)

    for account in matrix_account:
        if account[0] == id_account:
            change_name_account(account)
            change_money_account(account)
            print("\033[32mLa cuenta se actualizó con éxito.\033[0m")
            return
    
    print("\033[31mEl id que seleccionó no existe.\033[0m")

def change_name_account(account):
    change_name = input("Desea cambiar el nombre de la cuenta? Escriba 'si' o 'no', sin las comillas")
    while change_name != "si" or change_name != "no":
        print("\033[33mEl valor que ingreso no existe.\033[0m")
        change_name = input("Vuelva a ingresar 'si' o 'no', sin las comillas")
    
    if (change_name == "no"):
        return
    
    name_account = input("Ingrese un nuevo nombre de cuenta: ")
    while len(name_account) == 0 or name_account.isalpha():
        print("\033[33mEl nombre que ingreso no tiene valor o no es una palabra.\033[0m")
        name_account = input("Ingrese un nuevo nombre de cuenta: ")
    account[1] = name_account

def change_money_account(account):            
    change_money = input("Desea cambiar el monto de la cuenta? Escriba 'si' o 'no', sin las comillas")
    while change_money != "si" or change_money != "no":
        print("\033[33mEl valor que ingreso no existe.\033[0m")
        change_money = input("Vuelva a ingresar 'si' o 'no', sin las comillas")

    if change_money == "no":
        return
    
    total_money = input("Ingrese un nuevo monto de dinero: ")
    while not total_money.isnumeric():
        print("\033[33mEl valor que ingreso no es número.\033[0m")
        total_money = input("Ingrese un nuevo monto de dinero: ")
    account[2] = total_money

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
        
def get_category_by_id(matrix_categories, id_category):
    return
        
def get_categories(matrix_categories):
    print("="*MAX_SPACES_CATEGORIES)
    print(f'{"Categorias":^50}')
    print("="*MAX_SPACES_CATEGORIES)
    print(f"{BOLD}{'Numero':<20}{'Categoria':<30}{RESET}")
    for i in range(len(matrix_categories)):
        id=matrix_categories[i][0]
        amount = matrix_categories[i][1]
        print(f"{BOLD}{id:<20}{RESET}{amount:<30}")
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

def update_category(matrix_categories):
    id_category = int(input("¿Que categoría desea actualizar? Indique el numero o escriba 0 para salir: "))
    if id_category == 0:
        print("\033[32mNo se actualizo ninguna categoría.\033[0m")
        return

    category = get_category_by_id(matrix_categories, id_category)
    while category is None:
        print("\033[31mLa categoría no existe.\033[0m")

        id_category = int(input("¿Que categoría desea actualizar? Indique el numero o escriba 0 para salir: "))
        if id_category == 0:
            print("\033[32mNo se actualizo ninguna categoría.\033[0m")
            return
                
        category = get_category_by_id(matrix_categories, id_category)
    
    change_category(category)
    
def change_category(category):
    name_category = input("Ingrese un nuevo nombre de categoría: ")
    while len(name_category) == 0 or name_category.isalpha():
        print("\033[33mEl valor que ingreso no tiene valor o no es una palabra.\033[0m")
        name_category = input("Ingrese un nuevo nombre de categoría: ")
    category[1] = name_category

def get_budget_by_id(matrix_budgets, id_budget):
    for raw in matrix_budgets:
        if raw[0] == id_budget:
            return raw
    return None

def get_budgets(matrix_budgets):
    print("="*MAX_SPACES_BUDGETS)
    print(f'{"Presupuestos":^60}')
    print("="*MAX_SPACES_BUDGETS)
    print(f"{BOLD}{'Numero':<10}{'Categoria':<25}{'Monto':<25}{RESET}")
    for i in range(len(matrix_budgets)):
        id=matrix_budgets[i][0]
        category =get_account_by_id(categories,matrix_budgets[i][1])
        amount = "$"+str(matrix_budgets[i][2])
        print(f"{BOLD}{id:<10}{RESET}{category[1]:<25}{amount:<25}")
    return

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

def update_budget(matrix_budgets, matrix_categories):
    get_budgets(matrix_budgets)
    id_budget = int(input("¿Que presupuesto desea actualizar? Indique el numero o escriba 0 para salir: "))
    if id_budget == 0:
        print("\033[32mNo se actualizo ningún presupuesto.\033[0m")
        return

    budget = get_budget_by_id(matrix_budgets, id_budget)
    while budget is None:
        print("\033[31mLa presupuesto no existe.\033[0m")

        id_budget = int(input("¿Que presupuesto desea actualizar? Indique el numero o escriba 0 para salir: "))
        if id_budget == 0:
            print("\033[32mNo se actualizo ningún presupuesto.\033[0m")
            return
                
        budget = get_budget_by_id(matrix_budgets, id_budget)
    
    change_category_for_budget(budget, matrix_categories)
    change_budget_amount(budget)

def change_category_for_budget(budget, matrix_categories):
    change_category = input("Desea cambiar la categoría seleccionada? Escriba 'si' o 'no', sin las comillas")
    while change_category != "si" or change_category != "no":
        print("\033[33mEl valor que ingreso no existe.\033[0m")
        change_category = input("Vuelva a ingresar 'si' o 'no', sin las comillas")
    
    if (change_category == "no"):
        return
    
    get_categories(matrix_categories)
    id_category = int(input("¿Que categoría desea actualizar? Indique el numero o escriba 0 para salir: "))
    if id_category == 0:
        print("\033[32mNo se actualizo ningún presupuesto.\033[0m")
        return
    
    category = get_category_by_id(matrix_categories, id_category)
    while category is None:
        print("\033[31mLa categoría no existe.\033[0m")

        id_category = int(input("¿Que categoría desea actualizar? Indique el numero o escriba 0 para salir: "))
        if id_category == 0:
            print("\033[32mNo se actualizo ninguna categoría.\033[0m")
            return
                
        category = get_category_by_id(matrix_categories, id_category)

    budget[1] = id_category

def change_budget_amount(budget):
    change_budget = input("Desea cambiar el monto de la cuenta? Escriba 'si' o 'no', sin las comillas")
    while change_budget != "si" or change_budget != "no":
        print("\033[33mEl valor que ingreso no existe.\033[0m")
        change_budget = input("Vuelva a ingresar 'si' o 'no', sin las comillas")

    if change_budget == "no":
        return
    
    budget_amount = input("Ingrese un nuevo monto de dinero: ")
    while not budget_amount.isnumeric():
        print("\033[33mEl valor que ingreso no es número.\033[0m")
        budget_amount = input("Ingrese un nuevo monto de dinero: ")
    budget[2] = budget_amount

def add_transaction(name_account, name_category, date, time, amount, description, month, transaction_type="income"):  
    id= create_id(transactions)
    id_account = obtain_id_by_name(accounts, name_account)
    id_category = obtain_id_by_name(categories, name_category)
    # Should throw exceptions
    # if transaction_type==None:transaction_type="income" 
    if (id_account == -1):        
        print(f"\033[31mLa cuenta con ID '{id_account}' no existe. Por favor, cree una.\033[0m")
        return
        
    if (id_category == -1):
        print(f"\033[31mLa categoría '{name_category}' no existe. Por favor, cree una.\033[0m")
        return
    
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
    id = int(input("Que transaccion deseas eliminar? Indique el numero: "))
    
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
    print("="*MAX_SPACES_TRANSACTIONS)
    print(f'{"Transacciones":^110}')
    print("="*MAX_SPACES_TRANSACTIONS)
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
# delete_transaction()
# Ejemplo correcto
add_transaction("Galicia","Sueldo","2-3-2026","20:20",1200000,"Sueldo","Marzo")
add_account("BBVA", 1200000)
add_category("Ropa")
get_categories(categories)