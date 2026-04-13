from Styles import print_styles
from categories import get_categories
from accounts import update_account_balance, get_accounts
from helper import create_id, get_raw_by_id, slice_words
from budgets import update_budget_balance, get_budget_by_category

def add_transaction(matrix_transactions, matrix_accounts, matrix_categories,matrix_budgets, id_account, id_category, date, time, amount, description, month, transaction_type="income"):  
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
    
    matrix_transactions.append([id, id_raw_account, id_raw_category, date, time, final_amount, description, month])
    
    update_account_balance(matrix_accounts, id_raw_account, final_amount)
    update_budget_balance(matrix_budgets,id_raw_budget,final_amount)

def delete_transaction(matrix_transactions, matrix_accounts, matrix_categories, matrix_budgets):
    get_transactions(matrix_transactions, matrix_accounts, matrix_categories)
    id = int(input("Que transaccion deseas eliminar? Indique el numero o escriba 0 para salir: "))
    if id == 0:
        print(f"{print_styles.GREEN}No se elimino ninguna transacción.{print_styles.RESET}")
        return
    for transaction in matrix_transactions:
        if transaction[0]==id:
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

def change_account_transaction(transaction, matrix_accounts):
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

def change_category_transaction(transaction, matrix_categories):
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

def change_date_transaction(transaction):
    new_date = input("Ingrese la nueva fecha (formato: DD-MM-YYYY): ")
    while len(new_date.strip()) == 0:
        print(f"{print_styles.RED}La fecha ingresada no tiene valor.{print_styles.RESET}")
        new_date = input("Ingrese la nueva fecha (formato: DD-MM-YYYY): ")
    transaction[3] = new_date
    print(f"{print_styles.GREEN}Fecha actualizada.{print_styles.RESET}")

def change_time_transaction(transaction):
    new_time = input("Ingrese la nueva hora (formato: HH:MM): ")
    while len(new_time) == 0:
        print(f"{print_styles.RED}La hora ingresada no tiene valor.{print_styles.RESET}")
        new_time = input("Ingrese la nueva hora (formato: HH:MM): ")
    transaction[4] = new_time
    print(f"{print_styles.GREEN}Hora actualizada.{print_styles.RESET}")

def change_amount_transaction(transaction, matrix_accounts, matrix_budgets):
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

def change_description_transaction(transaction):
    new_desc = input("Ingrese una nueva descripción: ")
    while len(new_desc) == 0:
        print(f"{print_styles.YELLOW}La descripción ingresada no tiene valor.{print_styles.RESET}")
        new_desc = input("Ingrese una nueva descripción: ")
    transaction[6] = new_desc
    print(f"{print_styles.GREEN}Descripción actualizada.{print_styles.RESET}")

def change_month_transaction(transaction):
    new_month = input("Ingrese el nuevo mes: ")
    while len(new_month) == 0 or not new_month.isalpha():
        print(f"{print_styles.RED}El mes ingresado no tiene valor o contiene números.{print_styles.RESET}")
        new_month = input("Ingrese el nuevo mes: ")
    transaction[7] = new_month.capitalize()
    print(f"{print_styles.GREEN}Mes actualizado.{print_styles.RESET}")

def get_transactions(matrix_transactions, matrix_accounts, matrix_categories, predicate = None):
    count_matrix= len(matrix_transactions)
    
    print("="*print_styles.MAX_SPACES_TRANSACTIONS)
    print(f'{"Transacciones":^125}')
    print("="*print_styles.MAX_SPACES_TRANSACTIONS)
    print(f"{print_styles.BOLD_BLUE}Registros Totales: {count_matrix:<40}{print_styles.RESET}")
    print("="*print_styles.MAX_SPACES_TRANSACTIONS)
    print(f"{print_styles.BOLD}{'Numero':<10}{'Cuenta':<15}{'Categoria':<15}{'Fecha':<15}{'Hora':<10}{'Monto':<15}{'Descripcion':<30}{'Mes':<15}{print_styles.RESET}")
    for i in range(len(matrix_transactions)):
        if predicate is not None and not predicate(matrix_transactions[i]):
            continue

        id=matrix_transactions[i][0]
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
        print(f"{underline}{id:<10}{account[1]:<15}{category_sliced:<15}{date:<15}{hour:<10}{amount_str:<15}{description_slicing:<30}{month:<15}{print_styles.RESET}")
    print()

def get_transactions_by_category(matrix_transactions, matrix_accounts, matrix_categories):
    get_categories(matrix_categories)
    print(" ")
    id_category = int(input(f"{print_styles.BOLD_BLUE}Buscar en sus transacciones por la categoria (Ingrese el numero):{print_styles.RESET} "))
    transactions_by_category=list(filter(lambda x:x[2]==id_category, matrix_transactions))
    if len(transactions_by_category)==0:
        print(f"{print_styles.RED}No hay transacciones con dicha categoria.{print_styles.RESET}")
        return
    get_transactions(transactions_by_category, matrix_accounts, matrix_categories)