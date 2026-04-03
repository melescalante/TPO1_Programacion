from Styles import print_styles
from categories import get_categories
from accounts import revert_money_account
from matrix import transactions, categories, accounts
from helper import create_id, get_by_id, obtain_id_by_name

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
    print("="*print_styles.MAX_SPACES_TRANSACTIONS)
    print(f'{"Transacciones":^130}')
    print("="*print_styles.MAX_SPACES_TRANSACTIONS)
    print(f"{print_styles.BOLD}{'Numero':<10}{'Cuenta':<15}{'Categoria':<15}{'Fecha':<15}{'Hora':<10}{'Monto':<15}{'Descripcion':<30}{'Mes':<15}{print_styles.RESET}")
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
        underline = print_styles.UNDERLINE_INCOME
        if amount < 0:
            underline = print_styles.UNDERLINE_EXPENSE
        print(f"{underline}{id:<10}{account[1]:<15}{category[1]:<15}{date:<15}{hour:<10}{amount_str:<15}{description_slicing:<30}{month:<15}{print_styles.RESET}")
    print()

def get_transactions_by_category(matrix_transactions,matrix_categories):
    get_categories(matrix_categories)
    id_category=int(input("Buscar en sus transacciones por la categoria(Ingrese el numero) :"))
    transactions_by_category=list(filter(lambda x:x[2]==id_category, matrix_transactions))
    if len(transactions_by_category)==0:
        print(f"{print_styles.RED}No hay transacciones con dicha categoria.")
        return
    get_transactions(transactions_by_category)