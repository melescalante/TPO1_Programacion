from Styles import print_styles
from categories import get_categories
from user import get_user_by_id
from accounts import update_account_balance, get_accounts
from helper import create_id, get_raw_by_id, slice_words
from budgets import update_budget_balance, get_budget_by_category

def add_transaction(matrix_transactions, matrix_accounts, matrix_categories,matrix_budgets, id_account, id_category, date, time, amount, description, month, user_id, transaction_type="income"):
    """
    matrix_transactions: lista de transacciones a actualizar
    matrix_accounts: lista de cuentas del sistema
    matrix_categories: lista de categorías del sistema
    matrix_budgets: lista de presupuestos del sistema
    id_account: identificador de la cuenta asociada
    id_category: identificador de la categoría asociada
    date: fecha de la transacción (formato DD-MM-YYYY)
    time: hora de la transacción (formato HH:MM)
    amount: monto de la transacción
    description: descripción de la transacción
    month: mes de la transacción
    user_id: id del usuario
    transaction_type: tipo de transacción ('income' o 'expense')
    Retorna: None. Modifica matrix_transactions agregando nueva transacción y actualiza saldos
    """
    id= create_id(matrix_transactions)
    id_raw_account = get_raw_by_id(matrix_accounts, id_account)[0]
    id_raw_category = get_raw_by_id(matrix_categories, id_category)[0]
    
    id_raw_budget= get_budget_by_category(matrix_budgets,id_raw_category)[0]

    if (id_raw_account is None):        
        print(f"{print_styles.RED}El ID ingresado para la cuenta no existe. Por favor, intente nuevamente.{print_styles.RESET}")
        return
        
    if (id_raw_category is None):
        print(f"{print_styles.RED}El ID ingresado para la categoría no existe. Por favor, intente nuevamente.{print_styles.RESET}")
        return
    
    multiplier = 1
    if transaction_type.lower() == "expense":
        multiplier = -1
    final_amount = amount * multiplier
    
    matrix_transactions.append([id, id_raw_account, id_raw_category, date, time, final_amount, description, month, user_id])
    
    update_account_balance(matrix_accounts, id_raw_account, final_amount)
    update_budget_balance(matrix_budgets,id_raw_budget,final_amount)

def delete_transaction(matrix_transactions, matrix_accounts, matrix_categories, matrix_budgets, id_delete):
    """
    matrix_transactions: lista de transacciones a actualizar
    matrix_accounts: lista de cuentas del sistema
    matrix_categories: lista de categorías del sistema
    matrix_budgets: lista de presupuestos del sistema
    id_delete: identificador de la transacción a eliminar
    Retorna: None. Elimina la transacción y revierte cambios en cuentas y presupuestos
    """
    for transaction in matrix_transactions:
        if transaction[0]==id_delete:
            index=matrix_transactions.index(transaction)
            delete=matrix_transactions.pop(index)
            id_account = delete[1]
            id_category = delete[2]
            id_budget=get_budget_by_category(matrix_budgets,id_category)[0]
            retrieve_total_money = delete[5]
            update_account_balance(matrix_accounts, id_account, -retrieve_total_money)
            update_budget_balance(matrix_budgets,id_budget,-retrieve_total_money)
            get_transactions(matrix_transactions, matrix_accounts, matrix_categories)
            print(f"{print_styles.GREEN}Operación realizada con éxito. Transaccion eliminada correctamente.{print_styles.RESET}")
            return
        
    print(f"{print_styles.RED}Operación realizada sin éxito, el número de ID no existe.{print_styles.RESET}")

def update_account_transaction(transaction, matrix_accounts):
    """
    transaction: transacción a actualizar
    matrix_accounts: lista de cuentas del sistema
    Retorna: None. Modifica la cuenta asociada en la transacción
    """
    while True:
        get_accounts(matrix_accounts)
        new_account_id = int(input("Ingrese el número de la nueva cuenta: "))
        account = get_raw_by_id(matrix_accounts, new_account_id)

        if account is None:
            print(f"{print_styles.YELLOW}El valor que ingresó no es un número válido.{print_styles.RESET}")
            continue

        old_id_account = transaction[1]
        money_transaction = transaction[5]
        update_account_balance(matrix_accounts, old_id_account, -money_transaction)
        update_account_balance(matrix_accounts, new_account_id, money_transaction)
        transaction[1] = new_account_id
        print(f"{print_styles.GREEN}ID de cuenta actualizado.{print_styles.RESET}")
        return

def update_category_transaction(transaction, matrix_categories):
    """
    transaction: transacción a actualizar
    matrix_categories: lista de categorías del sistema
    Retorna: None. Modifica la categoría asociada en la transacción
    """
    while True:
        get_categories(matrix_categories)
        new_category_id = int(input("Ingrese el número de la nueva categoría: "))
        category = get_raw_by_id(matrix_categories, new_category_id)
        
        if category is None:
            print(f"{print_styles.YELLOW}El valor que ingresó no es un número válido.{print_styles.RESET}")
            continue
        
        transaction[2] = new_category_id
        print(f"{print_styles.GREEN}ID de categoría actualizado.{print_styles.RESET}")
        return

def update_date_transaction(transaction):
    """
    transaction: transacción a actualizar
    Retorna: None. Modifica la fecha de la transacción
    """
    new_date = input("Ingrese la nueva fecha (formato: DD-MM-YYYY): ")
    while len(new_date.strip()) == 0:
        print(f"{print_styles.RED}La fecha ingresada no tiene valor.{print_styles.RESET}")
        new_date = input("Ingrese la nueva fecha (formato: DD-MM-YYYY): ")
    transaction[3] = new_date
    print(f"{print_styles.GREEN}Fecha actualizada.{print_styles.RESET}")

def update_time_transaction(transaction):
    """
    transaction: transacción a actualizar
    Retorna: None. Modifica la hora de la transacción
    """
    new_time = input("Ingrese la nueva hora (formato: HH:MM): ")
    while len(new_time) == 0:
        print(f"{print_styles.RED}La hora ingresada no tiene valor.{print_styles.RESET}")
        new_time = input("Ingrese la nueva hora (formato: HH:MM): ")
    transaction[4] = new_time
    print(f"{print_styles.GREEN}Hora actualizada.{print_styles.RESET}")

def update_amount_transaction(transaction, matrix_accounts, matrix_budgets):
    """
    transaction: transacción a actualizar
    matrix_accounts: lista de cuentas del sistema
    matrix_budgets: lista de presupuestos del sistema
    Retorna: None. Modifica el monto de la transacción y actualiza saldos en cuentas y presupuestos
    """
    while True:
        new_amount_str = input("Ingrese el nuevo importe: ")
        not_sign = new_amount_str.replace("-", "", 1)
        if (not not_sign.isdigit()):
            print(f"{print_styles.RED}El importe ingresado no es un digito.{print_styles.RESET}")
            continue
        
        new_amount = int(new_amount_str)
        old_amount = transaction[5]
        id_budget=get_budget_by_category(matrix_budgets,transaction[2])[0]
        difference = new_amount - old_amount
        update_account_balance(matrix_accounts, transaction[1], difference)
        update_budget_balance(matrix_budgets,id_budget,difference)
        
        transaction[5] = new_amount
        print(f"{print_styles.GREEN}Importe actualizado.{print_styles.RESET}")
        return

def update_description_transaction(transaction):
    """
    transaction: transacción a actualizar
    Retorna: None. Modifica la descripción de la transacción
    """
    new_desc = input("Ingrese una nueva descripción: ")
    while len(new_desc) == 0:
        print(f"{print_styles.YELLOW}La descripción ingresada no tiene valor.{print_styles.RESET}")
        new_desc = input("Ingrese una nueva descripción: ")
    transaction[6] = new_desc
    print(f"{print_styles.GREEN}Descripción actualizada.{print_styles.RESET}")

def update_month_transaction(transaction):
    """
    transaction: transacción a actualizar
    Retorna: None. Modifica el mes de la transacción
    """
    new_month = input("Ingrese el nuevo mes: ")
    while len(new_month) == 0 or not new_month.isalpha():
        print(f"{print_styles.RED}El mes ingresado no tiene valor o contiene números.{print_styles.RESET}")
        new_month = input("Ingrese el nuevo mes: ")
    transaction[7] = new_month.capitalize()
    print(f"{print_styles.GREEN}Mes actualizado.{print_styles.RESET}")

def get_transactions(matrix_transactions, matrix_accounts, matrix_categories, dicc_users, predicate = None):
    """
    matrix_transactions: lista de transacciones a mostrar
    matrix_accounts: lista de cuentas para obtener información de cuenta
    matrix_categories: lista de categorías para obtener información de categoría
    dicc_users: diccionario de usuarios
    predicate: función opcional para filtrar transacciones
    Retorna: None. Imprime tabla formateada de transacciones
    """
    count_matrix= len(matrix_transactions)
    
    print("="*print_styles.MAX_SPACES_TRANSACTIONS)
    print(f'{"Transacciones":^125}')
    print("="*print_styles.MAX_SPACES_TRANSACTIONS)
    print(f"{print_styles.BOLD_BLUE}Registros Totales: {count_matrix:<40}{print_styles.RESET}")
    print("="*print_styles.MAX_SPACES_TRANSACTIONS)
    print(f"{print_styles.BOLD}{'Numero':<10}{'Usuario':<15}{'Cuenta':<15}{'Categoria':<15}{'Fecha':<15}{'Hora':<10}{'Monto':<15}{'Descripcion':<30}{'Mes':<15}{print_styles.RESET}")
    for i in range(len(matrix_transactions)):
        if predicate is not None and not predicate(matrix_transactions[i]):
            continue

        id=matrix_transactions[i][0]
        user = get_user_by_id(matrix_transactions[i][-1], dicc_users)["username"]
        user_sliced = slice_words(14, user)
        account = get_raw_by_id(matrix_accounts,matrix_transactions[i][1])
        category = get_raw_by_id(matrix_categories,matrix_transactions[i][2])
        category_sliced= slice_words(14, category[1])
        date =  matrix_transactions[i][3]
        hour =  matrix_transactions[i][4]
        amount = matrix_transactions[i][5]
        amount_str = "$"+ str(abs(matrix_transactions[i][5]))
        description =  matrix_transactions[i][6]
        description_slicing = slice_words(29,description)
        month =  matrix_transactions[i][7]
        underline = print_styles.UNDERLINE_INCOME
        if amount < 0:
            underline = print_styles.UNDERLINE_EXPENSE
        print(f"{underline}{id:<10}{user_sliced:<15}{account[1]:<15}{category_sliced:<15}{date:<15}{hour:<10}{amount_str:<15}{description_slicing:<30}{month:<15}{print_styles.RESET}")
    print()

def get_transactions_by_category(matrix_transactions, matrix_accounts, matrix_categories):
    """
    matrix_transactions: lista de transacciones a filtrar
    matrix_accounts: lista de cuentas del sistema
    matrix_categories: lista de categorías del sistema
    Retorna: None. Solicita categoría al usuario e imprime transacciones filtradas
    """
    get_categories(matrix_categories)
    print(" ")
    id_category = int(input(f"{print_styles.BOLD_BLUE}Buscar en sus transacciones por la categoria (Ingrese el numero):{print_styles.RESET} "))
    transactions_by_category = list(filter(lambda x:x[2]==id_category, matrix_transactions))
    if len(transactions_by_category)==0:
        print(f"{print_styles.RED}No hay transacciones con dicha categoria.{print_styles.RESET}")
        return
    get_transactions(transactions_by_category, matrix_accounts, matrix_categories)

def get_transaction_by_user_input(matrix_Transactions):
    """
    matrix_Transactions: lista de transacciones disponibles
    Retorna: transacción seleccionada por el usuario o None si cancela
    """
    while True:
        id_transaction = int(input("¿Qué transacción desea actualizar? Indique el numero o escriba 0 para salir: "))
        if id_transaction < 0 or id_transaction > len(matrix_Transactions):
            print(f"{print_styles.RED}La transacción no existe.{print_styles.RESET}")
            continue

        if id_transaction == 0:
            print(f"{print_styles.GREEN}No se actualizó ninguna transacción.{print_styles.RESET}")
            return None

        transaction = get_raw_by_id(matrix_Transactions, id_transaction)
        
        if transaction is None:
            print(f"{print_styles.RED}La transacción no existe. Intente de nuevo.{print_styles.RESET}")
            continue

        return transaction
    
def calculate_percentage_of_category(matrix_transactions):
    """
    matrix_transactions: lista de transacciones a analizar
    Retorna: tupla (filter_transactions, total) donde filter_transactions es lista de diccionarios
    con estructura {'category': id, 'registers': [...], 'total': suma_monto} y total es cantidad total de transacciones
    """
    filter_transactions = []
    categories_proccess = set()
    total=len(matrix_transactions)
    for i in range(len(matrix_transactions)):
        current_category = matrix_transactions[i][2]

        if current_category not in categories_proccess:
            filtered = list(filter(lambda x: x[2] == current_category, matrix_transactions))
            total_amount = sum(map(lambda x: x[5], filtered))
            category={
                "category":current_category,
                "registers":filtered,
                "total":total_amount
            }
            filter_transactions.append(category)
            categories_proccess.add(current_category)

    return filter_transactions, total

def get_percentage_of_category(filter_transactions, count_matrix, matrix_categories):
    """
    dicc: lista de diccionarios con {'category': ..., 'registers': [...]}
    count_matrix: total general de transacciones (el len de la matriz original)
    """
    print("=" * 110)
    print(f"{'Reporte de Porcentajes por Categoria':^110}")
    print("=" * 110)
    print(f"{print_styles.BOLD_BLUE}Registros Totales: {count_matrix}{print_styles.RESET}")
    print("-" * 110)
    print(f"{print_styles.BOLD}{'Categoría':<25} | {'Cant.':<8} | {'Porcentaje':<15} | {'Dinero I/E':<15}| {'Transc. Minima':<15} | {'Transc. Maxima':<15}{print_styles.RESET} ")
    print("-" * 110)

    for item in filter_transactions:
        name_category= get_raw_by_id(matrix_categories,item["category"])[1]
        name_sliced=slice_words(25,name_category)
        cant_registros_cat = len(item["registers"])
        percentage = (cant_registros_cat / count_matrix) * 100
        val_max = max(map(lambda x: x[5], item["registers"]))
        val_min = min(map(lambda x: x[5], item["registers"]))
        if percentage > 50:
            color_p = print_styles.RED    
        elif percentage > 20:
            color_p = print_styles.YELLOW
        else:
            color_p = print_styles.GREEN
        if item["total"]>0:
            color_amount= print_styles.GREEN  
        else:
            color_amount= print_styles.RED  
            
        print(f"{print_styles.BOLD}{name_sliced:<25}{print_styles.RESET} | {cant_registros_cat:<8} | {color_p}{percentage/100:<15.2%}{print_styles.RESET} | {color_amount}{abs(item["total"]):<14}{print_styles.RESET} | {abs(val_max):<15} | {abs(val_min):<15}")
    print()