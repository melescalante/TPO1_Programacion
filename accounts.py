from Styles import print_styles
from helper import create_id, get_raw_by_id

def add_account(matrix_accounts, account_name, total_money):
    id=create_id(matrix_accounts)
    for account in matrix_accounts:
        if account[1] == account_name:
            return
    matrix_accounts.append([id, account_name, total_money])
 
def get_accounts(matrix_account):
    count_matrix= len(matrix_account)
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f'{"Cuentas":^60}')
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f"{print_styles.BOLD_BLUE}Registros Totales: {count_matrix:<40}{print_styles.RESET}")
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f"{print_styles.BOLD}{'Numero':<10}{'Nombre Cuenta':<25}{'Dinero':<25}{print_styles.RESET}")
    for i in range(len(matrix_account)):
        id=matrix_account[i][0]
        name = matrix_account[i][1]
        amount=matrix_account[i][2]
        amount_str = "$"+str(matrix_account[i][2])
        underline = print_styles.UNDERLINE_INCOME
        if amount<0:
            underline= print_styles.UNDERLINE_EXPENSE
        print(f"{underline}{id:<10}{name:<25}{amount_str:<25}{print_styles.RESET}")
    return

def update_account(matrix_accounts):
    get_accounts(matrix_accounts)
    id_account = int(input("¿Que cuenta desea actualizar? Indique el numero o escriba 0 para salir: "))
    if id_account == 0:
        print(f"{print_styles.GREEN}No se actualizo ninguna cuenta.{print_styles.RESET}")
        return

    account = get_raw_by_id(matrix_accounts, id_account)
    while account is None:
        print(f"{print_styles.RED}La cuenta no existe.{print_styles.RESET}")

        id_account = int(input("¿Que cuenta desea actualizar? Indique el numero o escriba 0 para salir: "))            
        if id_account == 0:
            print(f"{print_styles.GREEN}No se actualizo ninguna cuenta.{print_styles.RESET}")
            return
                
        account = get_raw_by_id(matrix_accounts, id_account)

    while True:
        print(f"{print_styles.BOLD_BLUE}¿Qué campo de la cuenta deseas actualizar?{print_styles.RESET}")
        print("1. Nombre")
        print("2. Monto")
        print("0. Guardar y salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            change_name_account(account)
        elif opcion == "2":
            change_money_account(account)
        elif opcion == "0":
            print(f"{print_styles.GREEN}La cuenta se actualizó con éxito.{print_styles.RESET}")
            return
        else:
            print(f"{print_styles.RED}Opción no válida. Intente nuevamente.{print_styles.RESET}")

def change_name_account(account):
    name_account = input("Ingrese un nuevo nombre de cuenta: ")
    while len(name_account) == 0 or not name_account.isalpha():
        print(f"{print_styles.YELLOW}El nombre que ingreso no tiene valor o no es una palabra.{print_styles.RESET}")
        name_account = input("Ingrese un nuevo nombre de cuenta: ")
    account[1] = name_account

def change_money_account(account):            
    total_money = input("Ingrese un nuevo monto de dinero: ")
    while not total_money.isnumeric():
        print(f"{print_styles.YELLOW}El valor que ingreso no es número o es menor a 0.{print_styles.RESET}")
        total_money = input("Ingrese un nuevo monto de dinero: ")
    account[2] = int(total_money)

def delete_account(matrix_accounts):
    get_accounts(matrix_accounts)
    id = int(input("Que cuenta deseas eliminar? Indique el numero o escriba 0 para salir: "))
    delete=[]
    index=0
    if id == 0:
        print(f"{print_styles.GREEN}No se elimino ninguna cuenta.{print_styles.RESET}")
        return
    for acc in matrix_accounts:
        if acc[0]==id:
            index=matrix_accounts.index(acc)
            delete=matrix_accounts.pop(index)
            print(f"{print_styles.GREEN}Operación realizada con éxito. Cuenta eliminada correctamente.{print_styles.RESET}")
            return
    print()
    
def update_account_balance(matrix_accounts, id_account, amount):
    for account in matrix_accounts:
        if account[0] == id_account:
            account[2] += amount
            return
        

