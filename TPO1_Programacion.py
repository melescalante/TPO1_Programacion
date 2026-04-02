from matrix import accounts, transactions, categories, budgets

def get_budgets(matrix_budgets):
    print("="*MAX_SPACES_BUDGETS)
    print(f'{"Presupuestos":^60}')
    print("="*MAX_SPACES_BUDGETS)
    print(f"{BOLD}{'Numero':<10}{'Categoria':<25}{'Monto':<25}{RESET}")
    for i in range(len(matrix_budgets)):
        id=matrix_budgets[i][0]
        category = get_by_id(categories,matrix_budgets[i][1])
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

def delete_budget(matrix_budgets, id):
    if id == 0:
        return
    
    budget_deleted = None
    index = -1
    
    for budget in matrix_budgets:
        if (budget[0] == id):
            index = matrix_budgets.index(budget)
            budget_deleted = matrix_budgets.pop(index)
            break
    
    # Debería estar afuera
    print("\033[32mOperación realizada con éxito. Presupuesto eliminado correctamente.\033[0m")	
    print(index, budget_deleted)
    return index, budget_deleted 

def update_budget(matrix_budgets, matrix_categories):
    get_budgets(matrix_budgets)
    id_budget = int(input("¿Qué presupuesto desea actualizar? Indique el número o escriba 0 para salir: "))    
    if id_budget == 0:
        print("\033[32mNo se actualizó ningún presupuesto.\033[0m")
        return
    
    budget = get_by_id(matrix_budgets, id_budget)
    while budget is None:
        print("\033[31mEl presupuesto no existe.\033[0m")
        
        id_budget = int(input("¿Qué presupuesto desea actualizar? Indique el número o escriba 0 para salir: "))
        while id_budget < 0 or id_budget >= matrix_budgets[-1][0]:
            print("\033[31mEntrada inválida. Debe ingresar un número.\033[0m")
            id_budget = int(input("¿Qué presupuesto desea actualizar? Indique el número o escriba 0 para salir: "))
            
        if id_budget == 0:
            print("\033[32mNo se actualizó ningún presupuesto.\033[0m")
            return
                
        budget = get_by_id(matrix_budgets, id_budget)
    
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
    id_category = int(input("¿Qué categoría desea asignar? Indique el número o escriba 0 para cancelar: "))
    if id_category == 0:
        print("\033[32mNo se actualizó la categoría.\033[0m")
        return
    
    category = get_by_id(matrix_categories, id_category)
    while category is None:
        print("\033[31mLa categoría no existe.\033[0m")

        id_category = int(input("¿Por cuál categoría desea actualizar? Indique el numero o escriba 0 para salir: "))
        if id_category == 0:
            print("\033[32mNo se actualizo la categoría.\033[0m")
            return
                
        category = get_by_id(matrix_categories, id_category)

    budget[1] = id_category
    print("\033[32mCategoría actualizada.\033[0m")

def change_budget_amount(budget):
    budget_amount = input("Ingrese el nuevo monto del presupuesto: ")
    while not budget_amount.isnumeric():
        print("\033[33mEl valor que ingresó no es un número válido.\033[0m")
        budget_amount = input("Ingrese el nuevo monto del presupuesto: ")
        
    budget[2] = int(budget_amount)
    print("\033[32mMonto actualizado.\033[0m")

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
    get_transactions(transactions)
    id = int(input("Que transaccion deseas eliminar? Indique el numero o escriba 0 para salir: "))
    if id == 0:
        print("\033[32mNo se elimino ninguna transacción.\033[0m")
        return
    for transaction in transactions:
        if transaction[0]==id:
            index=transactions.index(transaction)
            delete=transactions.pop(index)
            id_account = delete[1]
            total_money = delete[5]
            revert_money_account(accounts, id_account, total_money)
            get_transactions(transactions)
            print("\033[32mOperación realizada con éxito. Transaccion eliminada correctamente.\033[0m")
            return
        
    print("\033[31mOperación realizada sin éxito, el número de ID no existe.\033[0m")

def update_transaction(matrix_transactions, matrix_accounts, matrix_categories):
    get_transactions(matrix_transactions)
    
    id_transaction = int(input("¿Qué transacción desea actualizar? Indique el numero o escriba 0 para salir: "))
    if id_transaction == 0:
        print("\033[32mNo se actualizó ninguna transacción.\033[0m")
        return

    transaction = get_by_id(matrix_transactions, id_transaction)
    while transaction is None:
        print("\033[31mLa transacción no existe.\033[0m")
        id_transaction = int(input("¿Qué transacción desea actualizar? Indique el numero o escriba 0 para salir: "))
        if id_transaction == 0:
            print("\033[32mNo se actualizó ninguna transacción.\033[0m")
            return
        transaction = get_by_id(matrix_transactions, id_transaction)

    while True:
        print("\033[1;34m¿Qué campo de la transacción deseas actualizar?\033[0m")
        print("1. Cuenta")
        print("2. Categoría")
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
            change_amount_transaction(transaction, matrix_accounts)
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
        revert_money_account(accounts, old_id_account, money_transaction)
        revert_money_account(accounts, new_account_id, -money_transaction)
        transaction[1] = new_account_id
        print("\033[32mID de cuenta actualizado.\033[0m")

def change_category_transaction(transaction, matrix_categories):
    while True:
        get_categories(matrix_categories)
        new_category_id = input("Ingrese la nueva categoría: ")
        category = get_by_id(matrix_categories, new_category_id)
        
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

def change_amount_transaction(transaction, matrix_accounts):
    new_amount = int(input("Ingrese el nuevo importe: "))
    if new_amount:
        old_amount = transaction[5]
        revert_money_account(matrix_accounts, transaction[1], old_amount)
        revert_money_account(matrix_accounts, transaction[1], -new_amount)
        transaction[5] = new_amount
        print("\033[32mImporte actualizado.\033[0m")

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

def get_transactions(matrix_transactions):
    RESET = "\033[0m"
    BOLD  = "\033[1m"
    print("="*MAX_SPACES_TRANSACTIONS)
    print(f'{"Transacciones":^130}')
    print("="*MAX_SPACES_TRANSACTIONS)
    print(f"{BOLD}{'Numero':<10}{'Cuenta':<15}{'Categoria':<15}{'Fecha':<15}{'Hora':<10}{'Monto':<15}{'Descripcion':<30}{'Mes':<15}{RESET}")
    for i in range(len(matrix_transactions)):
        id=matrix_transactions[i][0]
        account = get_by_id(accounts,matrix_transactions[i][1])
        category = get_by_id(categories,matrix_transactions[i][2])
        date =  matrix_transactions[i][3]
        hour =  matrix_transactions[i][4]
        amount = matrix_transactions[i][5]
        amount_str = "$"+ str(matrix_transactions[i][5])
        description =  matrix_transactions[i][6]
        description_slicing = f"{description[:25]}..." if len(description) > 25 else description
        month =  matrix_transactions[i][7]
        underline = UNDERLINE_INCOME
        if amount < 0:
            underline = UNDERLINE_EXPENSE
        print(f"{underline}{id:<10}{account[1]:<15}{category[1]:<15}{date:<15}{hour:<10}{amount_str:<15}{description_slicing:<30}{month:<15}{RESET}")
    print()

# Ejemplo con excepcion
add_transaction("Galicia","1","2-3-2026","20:20",1200000,"Sueldo","Marzo")
# Ejemplo correcto
add_transaction("Galicia","Sueldo","2-3-2026","20:20",1200000,"Sueldo","Marzo")
add_account("BBVA", 1200000)
add_category("Ropa")

# update_account(accounts)
# get_accounts(accounts)

# update_category(categories)
# get_categories(categories)

# update_budget(budgets, categories)

get_accounts(accounts)
# update_transaction(transactions, accounts, categories)
get_transactions(transactions)

# delete_account()
# delete_budget()
# get_budgets(budgets)

delete_category(transactions, budgets)
# get_budgets(budgets)
get_transactions(transactions)
# delete_transaction()
# get_accounts(accounts)
