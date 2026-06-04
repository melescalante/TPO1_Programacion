from datetime import datetime, time
from styles import print_styles
from categories import get_categories
from user import get_user_by_id
from accounts import update_account_balance, get_accounts
from helper import create_id, get_raw_by_id, slice_words, validate_date, validate_hour, json_loader
from budgets import update_budget_balance, get_budget_by_category

def add_transaction(data_transactions, data_accounts, data_categories, data_budgets, id_account, id_category, date, time, amount, description, id_user, transaction_type="income"):
    """
    data_transactions: lista de transacciones a actualizar
    data_accounts: lista de cuentas del sistema
    data_categories: lista de categorías del sistema
    data_budgets: lista de presupuestos del sistema
    id_account: identificador de la cuenta asociada
    id_category: identificador de la categoría asociada
    date: fecha de la transacción (formato DD-MM-YYYY)
    time: hora de la transacción (formato HH:MM)
    amount: monto de la transacción
    description: descripción de la transacción
    id_user: id del usuario
    transaction_type: tipo de transacción ('income' o 'expense')
    Retorna: None. Modifica data_transactions agregando nueva transacción y actualiza saldos
    """
    id = create_id(data_transactions)
    id_raw_account = get_raw_by_id(data_accounts, id_account)["id"]
    id_raw_category = get_raw_by_id(data_categories, id_category)["id"]
    
    id_raw_budget = get_budget_by_category(data_budgets,id_raw_category)["id"]

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
    
    data_transactions.append({'id': id, 
        'id_account': id_raw_account, 
        'id_category': id_raw_category, 
        'date': date, 
        'time': time, 
        'amount': final_amount, 
        'description': description, 
        'id_user': id_user
    })
    json_loader('json/transactions.json', data_transactions)
    
    update_account_balance(data_accounts, id_raw_account, final_amount)
    update_budget_balance(data_budgets, id_raw_budget, final_amount)
    print(f"{print_styles.GREEN}La transacción fue agregada correctamente.{print_styles.RESET}")

def delete_transaction(data_transactions, data_accounts, data_categories, data_budgets, id_delete):
    """
    data_transactions: lista de transacciones a actualizar
    data_accounts: lista de cuentas del sistema
    data_categories: lista de categorías del sistema
    data_budgets: lista de presupuestos del sistema
    id_delete: identificador de la transacción a eliminar
    Retorna: None. Elimina la transacción y revierte cambios en cuentas y presupuestos
    """
    for transaction in data_transactions:
        if transaction['id']==id_delete:
            index = data_transactions.index(transaction)
            delete = data_transactions.pop(index)
            id_account = delete['id_account']
            id_category = delete['id_category']
            id_budget = get_budget_by_category(data_budgets,id_category)['id']
            retrieve_total_money = delete['amount']
            update_account_balance(data_accounts, id_account, -retrieve_total_money)
            update_budget_balance(data_budgets,id_budget,-retrieve_total_money)
            get_transactions(data_transactions, data_accounts, data_categories)
            json_loader('json/transactions.json', data_transactions)
            print(f"{print_styles.GREEN}Operación realizada con éxito. Transaccion eliminada correctamente.{print_styles.RESET}")
            return
        
    print(f"{print_styles.RED}Operación realizada sin éxito, el número de ID no existe.{print_styles.RESET}")

def update_account_transaction(transaction, data_transactions, data_accounts):
    """
    transaction: transacción a actualizar
    data_accounts: lista de cuentas del sistema
    data_transactions: lista de transacciones del sistema
    Retorna: None. Modifica la cuenta asociada en la transacción
    """
    while True:
        try:
            get_accounts(data_accounts)
            new_account_id = int(input("Ingrese el número de la nueva cuenta: "))
            account = get_raw_by_id(data_accounts, new_account_id)

            if account is None:
                print(f"{print_styles.YELLOW}El valor que ingresó no es un número válido.{print_styles.RESET}")
                continue

            old_id_account = transaction['id_account']
            money_transaction = transaction['amount']
            update_account_balance(data_accounts, old_id_account, -money_transaction)
            update_account_balance(data_accounts, new_account_id, money_transaction)
            transaction['id_account'] = new_account_id
            json_loader('json/transactions.json', data_transactions)
            print(f"{print_styles.GREEN}ID de cuenta actualizado.{print_styles.RESET}")
            return
        except ValueError:
            print(f"{print_styles.RED}Debes ingresar un número.{print_styles.RESET}")
        except:
            print(f"{print_styles.RED}Ha ocurrido un error.{print_styles.RESET}")
            break
            

def update_category_transaction(transaction, data_transactions, data_categories):
    """
    transaction: transacción a actualizar
    data_categories: lista de categorías del sistema
    Retorna: None. Modifica la categoría asociada en la transacción
    """
    while True:
        try:
            get_categories(data_categories)
            new_category_id = int(input("Ingrese el número de la nueva categoría: "))
            category = get_raw_by_id(data_categories, new_category_id)
            
            if category is None:
                print(f"{print_styles.YELLOW}El valor que ingresó no es un número válido.{print_styles.RESET}")
                continue
            
            transaction['id_category'] = new_category_id
            json_loader('json/transactions.json', data_transactions)
            print(f"{print_styles.GREEN}ID de categoría actualizado.{print_styles.RESET}")
            return        
        except ValueError:
            print(f"{print_styles.RED}Debes ingresar un número.{print_styles.RESET}")
        except:
            print(f"{print_styles.RED}Ha ocurrido un error.{print_styles.RESET}")
            break

def update_date_transaction(transaction, data_transactions):
    """
    transaction: transacción a actualizar
    Retorna: None. Modifica la fecha de la transacción
    """
    actual_date = datetime.now().date()
    print(f"Su fecha actual es: {print_styles.YELLOW}{actual_date}{print_styles.RESET}, presione Enter si desea dejar la fecha actual")
    date = input("Ingrese la fecha (formato: YYYY-MM-DD): ")
    if len(date) == 0:
        date = str(actual_date)
    else:
        message, is_valid = validate_date(date)
        if not is_valid:
            print(f"{print_styles.RED}{message}{print_styles.RESET}")
            return
    transaction['date'] = date
    json_loader('json/transactions.json', data_transactions)    
    print(f"{print_styles.GREEN}Fecha actualizada.{print_styles.RESET}")

def update_time_transaction(transaction, data_transactions):
    """
    transaction: transacción a actualizar
    Retorna: None. Modifica la hora de la transacción
    """
    parse_time = time(datetime.now().hour, datetime.now().minute)
    print(f"Su hora actual es: {print_styles.YELLOW}{str(parse_time)[0:-3]}{print_styles.RESET}, presione Enter si desea dejar la hora actual")
    actual_time = input("Ingrese la hora (formato: HH:MM): ")
    if len(actual_time) == 0:
        actual_time = str(parse_time)[0:-3]
    else:
        message, is_valid = validate_hour(actual_time)
        if not is_valid:
            print(f"{print_styles.RED}{message}{print_styles.RESET}")
            return
    transaction['time'] = actual_time
    json_loader('json/transactions.json', data_transactions)  
    print(f"{print_styles.GREEN}Hora actualizada.{print_styles.RESET}")

def update_amount_transaction(transaction, data_transactions, data_accounts, data_budgets):
    """
    transaction: transacción a actualizar
    data_accounts: lista de cuentas del sistema
    data_budgets: lista de presupuestos del sistema
    Retorna: None. Modifica el monto de la transacción y actualiza saldos en cuentas y presupuestos
    """
    while True:
        try:
            new_amount = int(input("Ingrese el nuevo importe: "))
            old_amount = transaction['amount']
            id_budget = get_budget_by_category(data_budgets, transaction['id_category'])['id']

            if id_budget == None:
                print(f"{print_styles.RED}El ID del presupuesto ingresado no existe.{print_styles.RESET}")
                return

            difference = new_amount - old_amount
            update_account_balance(data_accounts, transaction['id_account'], difference)
            update_budget_balance(data_budgets, id_budget, difference)
            
            transaction['amount'] = new_amount
            json_loader('json/transactions.json', data_transactions)  
            print(f"{print_styles.GREEN}Importe actualizado.{print_styles.RESET}")
            return
        except ValueError:
            print(f"{print_styles.RED}El valor ingresado no es un digito.{print_styles.RESET}")
        except:
            print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")

def update_description_transaction(transaction, data_transactions):
    """
    transaction: transacción a actualizar
    Retorna: None. Modifica la descripción de la transacción
    """
    new_desc = input("Ingrese una nueva descripción: ")
    while len(new_desc) == 0:
        print(f"{print_styles.YELLOW}La descripción ingresada no tiene valor.{print_styles.RESET}")
        new_desc = input("Ingrese una nueva descripción: ")
    transaction['description'] = new_desc
    json_loader('json/transactions.json', data_transactions)  
    print(f"{print_styles.GREEN}Descripción actualizada.{print_styles.RESET}")

def get_transactions(data_transactions, matrix_accounts, matrix_categories, predicate = None):
    """
    data_transactions: lista de transacciones a mostrar
    matrix_accounts: lista de cuentas para obtener información de cuenta
    matrix_categories: lista de categorías para obtener información de categoría
    predicate: función opcional para filtrar transacciones
    Retorna: None. Imprime tabla formateada de transacciones
    """
    count_matrix= len(data_transactions)
    
    print("="*print_styles.MAX_SPACES_TRANSACTIONS)
    print(f'{"Transacciones":^125}')
    print("="*print_styles.MAX_SPACES_TRANSACTIONS)
    print(f"{print_styles.BOLD_BLUE}Registros Totales: {count_matrix:<40}{print_styles.RESET}")
    print("="*print_styles.MAX_SPACES_TRANSACTIONS)
    print(f"{print_styles.BOLD}{'Numero':<10}{'Usuario':<15}{'Cuenta':<15}{'Categoria':<15}{'Fecha':<15}{'Hora':<10}{'Monto':<15}{'Descripcion':<30}{print_styles.RESET}")
    for i in range(len(data_transactions)):
        if predicate is not None and not predicate(data_transactions[i]):
            continue

        id = data_transactions[i]["id"]
        user = get_user_by_id(data_transactions[i]["id_user"])["username"]
        user_sliced = slice_words(14, user)
        account = get_raw_by_id(matrix_accounts,data_transactions[i]["id_account"])
        category = get_raw_by_id(matrix_categories,data_transactions[i]["id_category"])
        category_sliced= slice_words(14, category["category"])
        date =  data_transactions[i]["date"]
        hour =  data_transactions[i]["time"]
        amount = data_transactions[i]["amount"]
        amount_str = "$"+ str(abs(amount))
        description =  data_transactions[i]["description"]
        description_slicing = slice_words(29, description)
        underline = print_styles.UNDERLINE_INCOME
        if amount < 0:
            underline = print_styles.UNDERLINE_EXPENSE
        print(f"{underline}{id:<10}{user_sliced:<15}{account["account"]:<15}{category_sliced:<15}{date:<15}{hour:<10}{amount_str:<15}{description_slicing:<30}{print_styles.RESET}")
    print()

def get_transactions_by_category(data_transactions, data_accounts, data_categories):
    """
    data_transactions: lista de transacciones a filtrar
    matrix_accounts: lista de cuentas del sistema
    data_categories: lista de categorías del sistema
    Retorna: None. Solicita categoría al usuario e imprime transacciones filtradas
    """
    try:
        get_categories(data_categories)
        print(" ")
        id_category = int(input(f"{print_styles.BOLD_BLUE}Buscar en sus transacciones por la categoria (Ingrese el numero):{print_styles.RESET} "))
        transactions_by_category = list(filter(lambda x: x['id_category'] == id_category, data_transactions))
        if len(transactions_by_category) == 0:
            print(f"{print_styles.RED}No hay transacciones con dicha categoria.{print_styles.RESET}")
            return
        get_transactions(transactions_by_category, data_accounts, data_categories)
    except ValueError:
        print(f"{print_styles.RED}Debes ingresar un número.{print_styles.RESET}")
    except:
        print(f"{print_styles.RED}Ha ocurrido un error.{print_styles.RESET}")

def get_transaction_by_user_input(data_transactions):
    """
    data_transactions: lista de transacciones disponibles
    Retorna: transacción seleccionada por el usuario o None si cancela
    """
    while True:
        try:
            id_transaction = int(input("¿Qué transacción desea actualizar? Indique el numero o escriba 0 para salir: "))
            if id_transaction < 0 or id_transaction > len(data_transactions):
                print(f"{print_styles.RED}La transacción no existe.{print_styles.RESET}")
                continue

            if id_transaction == 0:
                print(f"{print_styles.GREEN}No se actualizó ninguna transacción.{print_styles.RESET}")
                return None

            transaction = get_raw_by_id(data_transactions, id_transaction)
            
            if transaction is None:
                print(f"{print_styles.RED}La transacción no existe. Intente de nuevo.{print_styles.RESET}")
                continue

            return transaction        
        except ValueError:
            print(f"{print_styles.RED}Debes ingresar un número.{print_styles.RESET}")
        except:
            print(f"{print_styles.RED}Ha ocurrido un error.{print_styles.RESET}")
            break
    
def calculate_percentage_of_category(data_transactions):
    """
    data_transactions: lista de transacciones a analizar
    Retorna: tupla (filter_transactions, total) donde filter_transactions es lista de diccionarios
    con estructura {'category': id, 'registers': [...], 'total': suma_monto} y total es cantidad total de transacciones
    """
    filter_transactions = []
    categories_proccess = set()
    total=len(data_transactions)
    
    try:
        for i in range(len(data_transactions)):
            current_category = data_transactions[i]['id_category']

            if current_category not in categories_proccess:
                filtered = list(filter(lambda x: x['id_category'] == current_category, data_transactions))
                total_amount = sum(map(lambda x: x['amount'], filtered))
                category={
                    "category":current_category,
                    "registers":filtered,
                    "total":total_amount
                }
                filter_transactions.append(category)
                categories_proccess.add(current_category)

        return filter_transactions, total
    except TypeError:
        print(f"{print_styles.RED}No se ingresó una matriz.{print_styles.RESET}")
    except:
        print(f"{print_styles.RED}Ha ocurrido un error.{print_styles.RESET}")

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
        name_category= get_raw_by_id(matrix_categories,item["category"])['category']
        name_sliced=slice_words(25,name_category)
        cant_registros_cat = len(item["registers"])
        percentage = (cant_registros_cat / count_matrix) * 100
        val_max = max(map(lambda x: x['amount'], item["registers"]))
        val_min = min(map(lambda x: x['amount'], item["registers"]))
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