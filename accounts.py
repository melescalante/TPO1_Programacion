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

def get_account_by_user_input(matrix_accounts):
    while True:
        id_account = int(input("¿Que cuenta desea actualizar? Indique el numero o escriba 0 para salir: "))
        
        if id_account < 0 or id_account > len(matrix_accounts):
            print(f"{print_styles.RED}Entrada inválida. Debe ingresar un número.{print_styles.RESET}")
            continue

        if id_account == 0:
            print(f"{print_styles.GREEN}No se actualizó ninguna cuenta.{print_styles.RESET}")
            return None

        account = get_raw_by_id(matrix_accounts, id_account)
        if account is None:
            print(f"{print_styles.RED}La cuenta no existe.{print_styles.RESET}")
            continue

        return account

def update_name_account(account):
    name_account = input("Ingrese un nuevo nombre de cuenta: ")
    while len(name_account) == 0 or not name_account.isalpha(): # bug, no admite espacios
        print(f"{print_styles.YELLOW}El nombre que ingreso no tiene valor o no es una palabra.{print_styles.RESET}")
        name_account = input("Ingrese un nuevo nombre de cuenta: ")
    account[1] = name_account

def update_money_account(account):            
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
        

