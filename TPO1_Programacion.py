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

def get_by_id(matrix, id):
    for raw in matrix:
        if raw[0] == id:
            return raw
    return None

def get_accounts(matrix_account):
    print("="*MAX_SPACES_BUDGETS)
    print(f'{"Cuentas":^60}')
    print("="*MAX_SPACES_BUDGETS)
    print(f"{BOLD}{'Numero':<20}{'Nombre Cuenta':<30}{'Dinero':<30}{RESET}")
    for i in range(len(matrix_account)):
        id=matrix_account[i][0]
        name = matrix_account[i][1]
        amount = "+"+str(matrix_account[i][2])
        print(f"{BOLD}{id:<20}{RESET}{name:<30}{amount:<30}")
    return

def update_account(matrix_accounts):
    id_account = input("¿Que cuenta desea actualizar? Indique el numero o escriba 0 para salir: ")
    while not id_account.isnumeric():
        print("\033[31mEntrada inválida. Debe ingresar un número.\033[0m")
        id_account = input("¿Que cuenta desea actualizar? Indique el numero o escriba 0 para salir: ")

    if id_account == 0:
        print("\033[32mNo se actualizo ninguna cuenta.\033[0m")
        return

    account = get_by_id(matrix_accounts, id_account)
    while account is None:
        print("\033[31mLa cuenta no existe.\033[0m")

        id_account = input("¿Que cuenta desea actualizar? Indique el numero o escriba 0 para salir: ")
        while not id_account.isnumeric():
            print("\033[31mEntrada inválida. Debe ingresar un número.\033[0m")
            id_account = input("¿Que cuenta desea actualizar? Indique el numero o escriba 0 para salir: ")
            
        if id_account == 0:
            print("\033[32mNo se actualizo ninguna cuenta.\033[0m")
            return
                
        account = get_by_id(matrix_accounts, id_account)

    while True:
        print("\033[1;34m¿Qué campo de la cuenta deseas actualizar?\033[0m")
        print("1. Nombre")
        print("2. Monto")
        print("0. Guardar y salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            change_name_account(account)
        elif opcion == "2":
            change_money_account(account)
        elif opcion == "0":
            print("\033[32mLa cuenta se actualizó con éxito.\033[0m")
            return
        else:
            print("\033[31mOpción no válida. Intente nuevamente.\033[0m")

def change_name_account(account):
    name_account = input("Ingrese un nuevo nombre de cuenta: ")
    while len(name_account) == 0 or name_account.isalpha():
        print("\033[33mEl nombre que ingreso no tiene valor o no es una palabra.\033[0m")
        name_account = input("Ingrese un nuevo nombre de cuenta: ")
    account[1] = name_account

def change_money_account(account):            
    total_money = input("Ingrese un nuevo monto de dinero: ")
    while not (total_money.isnumeric()):
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
    
def update_money_account(accounts, id_account, total_money):
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
        category =get_by_id(categories,matrix_budgets[i][1])
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
    id_budget = input("¿Qué presupuesto desea actualizar? Indique el número o escriba 0 para salir: ")
    while not id_budget.isnumeric():
        print("\033[31mEntrada inválida. Debe ingresar un número.\033[0m")
        id_budget = input("¿Qué presupuesto desea actualizar? Indique el número o escriba 0 para salir: ")
    
    if id_budget == 0:
        print("\033[32mNo se actualizó ningún presupuesto.\033[0m")
        return
    
    budget = get_budget_by_id(matrix_budgets, id_budget)
    while budget is None:
        print("\033[31mEl presupuesto no existe.\033[0m")
        
        id_budget = input("¿Qué presupuesto desea actualizar? Indique el número o escriba 0 para salir: ")
        while not id_budget.isnumeric():
            print("\033[31mEntrada inválida. Debe ingresar un número.\033[0m")
            id_budget = input("¿Qué presupuesto desea actualizar? Indique el número o escriba 0 para salir: ")
            
        if id_budget == 0:
            print("\033[32mNo se actualizó ningún presupuesto.\033[0m")
            return
                
        budget = get_budget_by_id(matrix_budgets, id_budget)
    
    while True:
        print("\033[1;34m¿Qué campo del presupuesto deseas actualizar?\033[0m")
        print("1. Categoría")
        print("2. Monto")
        print("0. Guardar y salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            change_category_for_budget(budget, matrix_categories)
        elif opcion == "2":
            change_budget_amount(budget)
        elif opcion == "0":
            print("\033[32mEl presupuesto se actualizó con éxito.\033[0m")
            return
        else:
            print("\033[31mOpción no válida. Intente nuevamente.\033[0m")

def change_category_for_budget(budget, matrix_categories):
    get_categories(matrix_categories)
    id_category = input("¿Qué categoría desea asignar? Indique el número o escriba 0 para cancelar: ")
    while not id_category.isnumeric():
        print("\033[31mEntrada inválida. Debe ingresar un número.\033[0m")
        id_category = input("¿Qué categoría desea asignar? Indique el número o escriba 0 para cancelar: ")

    if id_category == 0:
        print("\033[32mNo se actualizó la categoría.\033[0m")
        return
    
    category = get_category_by_id(matrix_categories, id_category)
    while category is None:
        print("\033[31mLa categoría no existe.\033[0m")
        
        id_category = input("¿Qué categoría desea asignar? Indique el número o escriba 0 para cancelar: ")
        while not id_category.isnumeric():
            print("\033[31mEntrada inválida. Debe ingresar un número.\033[0m")
            id_category = input("¿Qué categoría desea asignar? Indique el número o escriba 0 para cancelar: ")
            
        if id_category == 0:
            print("\033[32mNo se actualizó la categoría.\033[0m")
            return
                
        category = get_category_by_id(matrix_categories, id_category)

    budget[1] = id_category
    print("\033[32mCategoría actualizada.\033[0m")

def change_budget_amount(budget):
    budget_amount = input("Ingrese el nuevo monto del presupuesto: ")
    while not (budget_amount.isnumeric()):
        print("\033[33mEl valor que ingresó no es un número válido.\033[0m")
        budget_amount = input("Ingrese el nuevo monto del presupuesto: ")
        
    budget[2] = int(budget_amount)
    print("\033[32mMonto actualizado.\033[0m")

def get_transaction_by_id(matrix, target_id):
    return

def add_transaction(name_account, name_category, date, time, amount, description, month, transaction_type="income"):  
    id= create_id(transactions)
    id_account = obtain_id_by_name(accounts, name_account)
    id_category = obtain_id_by_name(categories, name_category)

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
            update_money_account(accounts, id_account, total_money)
            print_transactions(transactions)
            print("\033[32mOperación realizada con éxito.\033[0m")
            return
        
    print("\033[31mOperación realizada sin éxito, el número de ID no existe.\033[0m")

def update_transaction(matrix_transactions, matrix_accounts, matrix_categories):
    print_transactions(matrix_transactions)
    
    id_transaction = int(input("¿Qué transacción desea actualizar? Indique el numero o escriba 0 para salir: "))
    if id_transaction == 0:
        print("\033[32mNo se actualizó ninguna transacción.\033[0m")
        return

    transaction = get_transaction_by_id(matrix_transactions, id_transaction)
    while transaction is None:
        print("\033[31mLa transacción no existe.\033[0m")
        id_transaction = int(input("¿Qué transacción desea actualizar? Indique el numero o escriba 0 para salir: "))
        if id_transaction == 0:
            print("\033[32mNo se actualizó ninguna transacción.\033[0m")
            return
        transaction = get_transaction_by_id(matrix_transactions, id_transaction)

    while True:
        print("\033[1;34m¿Qué campo de la transacción deseas actualizar?\033[0m")
        print("1. ID Cuenta")
        print("2. ID Categoría")
        print("3. Fecha")
        print("4. Hora")
        print("5. Importe")
        print("6. Descripción")
        print("7. Mes")
        print("0. Guardar y salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            change_account_transaction(transaction, matrix_accounts)
        elif opcion == "2":
            change_category_transaction(transaction, matrix_categories)
        elif opcion == "3":
            change_date_transaction(transaction)
        elif opcion == "4":
            change_time_transaction(transaction)
        elif opcion == "5":
            change_amount_transaction(transaction)
        elif opcion == "6":
            change_description_transaction(transaction)
        elif opcion == "7":
            change_month_transaction(transaction)
        elif opcion == "0":
            print("\033[32mLa transacción se actualizó con éxito.\033[0m")
            return
        else:
            print("\033[31mOpción no válida. Intente nuevamente.\033[0m")

def change_account_transaction(transaction, matrix_accounts):
    while True:
        new_account_id = input("Ingrese la nueva cuenta: ")
        account = get_by_id(matrix_accounts, new_account_id)

        if account is None:
            print("\033[33mEl valor que ingresó no es un número válido.\033[0m")
            pass

        old_id_account = transactions[1]
        money_transaction = transactions[5]
        update_money_account(accounts, old_id_account, money_transaction)
        update_money_account(accounts, new_account_id, -money_transaction)
        transaction[1] = new_account_id
        print("\033[32mID de cuenta actualizado.\033[0m")

def change_category_transaction(transaction, matrix_categories):
    while True:
        get_categories(matrix_categories)
        new_category_id = input("Ingrese la nueva categoría: ")
        category = get_category_by_id(matrix_categories, new_category_id)
        
        if category is None:
            print("\033[33mEl valor que ingresó no es un número válido.\033[0m")
            pass
        
        transaction[2] = new_category_id
        print("\033[32mID de categoría actualizado.\033[0m")

def change_date_transaction(transaction):
    new_date = input("Ingrese la nueva fecha (formato: DD-MM-YYYY): ")
    while len(new_date.strip()) == 0:
        print("\033[33mLa fecha ingresada no tiene valor.\033[0m")
        new_date = input("Ingrese la nueva fecha (formato: DD-MM-YYYY): ")
    transaction[3] = new_date
    print("\033[32mFecha actualizada.\033[0m")

def change_time_transaction(transaction):
    new_time = input("Ingrese la nueva hora (formato: HH:MM): ")
    while len(new_time) == 0:
        print("\033[33mLa hora ingresada no tiene valor.\033[0m")
        new_time = input("Ingrese la nueva hora (formato: HH:MM): ")
    transaction[4] = new_time
    print("\033[32mHora actualizada.\033[0m")

def change_amount_transaction(transaction):
    while True:
        new_amount = input("Ingrese el nuevo importe: ")
        if new_amount.isnumeric():
            transaction[5] = new_amount
            print("\033[32mImporte actualizado.\033[0m")
            return
        print("\033[33mEl valor que ingresó no es un número válido.\033[0m")

def change_description_transaction(transaction):
    new_desc = input("Ingrese una nueva descripción: ")
    while len(new_desc) == 0:
        print("\033[33mLa descripción ingresada no tiene valor.\033[0m")
        new_desc = input("Ingrese una nueva descripción: ")
    transaction[6] = new_desc
    print("\033[32mDescripción actualizada.\033[0m")

def change_month_transaction(transaction):
    new_month = input("Ingrese el nuevo mes: ")
    while len(new_month) == 0 or not new_month.isalpha():
        print("\033[33mEl mes ingresado no tiene valor o contiene números.\033[0m")
        new_month = input("Ingrese el nuevo mes: ")
    transaction[7] = new_month.capitalize()
    print("\033[32mMes actualizado.\033[0m")

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
get_accounts(accounts)
update_account(accounts)
update_budget(budgets, categories)
update_category(categories)
update_transaction(transactions, accounts, categories)