from datetime import datetime, time
from pickle import TRUE

from transactions import *
from budgets import *
from categories import *
from accounts import *
from user import *
from analytics import *
from helper import *
from permissions import has_permission

# Permissions
READ=1
READ_WRITE=2

file_users = 'txt/users.txt'
# Rutas de json
file_accounts='json/accounts.json'
file_categories='json/categories.json'
file_budgets='json/budgets.json'
file_transactions='json/transactions.json'

print("¡Bienvenido/a al sistema de Gestor de Gastos!\n")

user = read_users()[0]
while user==None:
    user=login()

print(user)

#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():

    #-------------------------------------------------
    # Bloque de menú
    #----------------------------------------------------------------------------------------------
    while True:
        can_read = has_permission(user, READ)
        can_write = has_permission(user, READ_WRITE)
        valid_options = ["0","1"]
        if can_write: valid_options.append(["4", "5"])
        if can_read: valid_options.extend(["2", "3", "6", "7"])

        while True:
            options = 6
            print()
            print("---------------------------")
            print("MENÚ PRINCIPAL")
            print("---------------------------")
            print(f"{print_styles.BOLD}[1]{print_styles.RESET} Gestión de Usuarios")
            print(f"{print_styles.BOLD}[2]{print_styles.RESET} Gestión de Transacciones")
            print(f"{print_styles.BOLD}[3]{print_styles.RESET} Gestión de Categorías")
            print(f"{print_styles.BOLD}[4]{print_styles.RESET} Gestión de Presupuestos")
            print(f"{print_styles.BOLD}[5]{print_styles.RESET} Gestión de Cuentas")
            print(f"{print_styles.BOLD}[6]{print_styles.RESET} Resumen")

            print("---------------------------")
            print(f"{print_styles.BOLD}[0]{print_styles.RESET} Salir del programa")
            print("---------------------------")
            print()
            
            option = input("Seleccione una opción: ")
            if option in [str(i) for i in range(0, options + 1)]:
                break
            else:
                input("Opción inválida. Presione ENTER para volver a seleccionar.")
        print()

        if option == "0": # Opción salir del programa
            exit() # También puede ser sys.exit() para lo cual hay que importar el módulo sys

        elif option == "1":   # Opción 1 --> Gestión de Usuarios
            while True:
                while True:
                    options = 5
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Usuarios")
                    print("---------------------------")
                    print(f"{print_styles.BOLD}[1]{print_styles.RESET} Mostrar Usuarios")
                    print(f"{print_styles.BOLD}[2]{print_styles.RESET} Añadir Usuario")
                    permission = has_permission(user, READ_WRITE)
                    if permission:
                        print(f"{print_styles.BOLD}[3]{print_styles.RESET} Eliminar Usuario")
                        print(f"{print_styles.BOLD}[4]{print_styles.RESET} Actualizar Contraseña")
                        print(f"{print_styles.BOLD}[5]{print_styles.RESET} Actualizar Username")
                    print("---------------------------")
                    print(f"{print_styles.BOLD}[0]{print_styles.RESET} Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    option = input("Seleccione una opción: ")
                    if option in [str(i) for i in range(0, options + 1)]:
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if option == "0":
                    break

                if option == "1":
                    permission = has_permission(user, READ)
                    if not permission:
                        break
                    show_users()

                elif option == "2":
                    permission = has_permission(user, READ)
                    if not permission:
                        break
                    username = ""
                    email = ""
                    while True:
                        if username == "":
                            username = input(f"{print_styles.BOLD}Ingrese el username: {print_styles.RESET}").strip()

                        if not validate_email(email):
                            email = input(f"{print_styles.BOLD}Ingrese el email: {print_styles.RESET}").strip()
                            if not validate_email(email):
                                print(f"{print_styles.RED}El email no cumple los parametros requeridos.{print_styles.RESET}")
                                continue

                        password = input(f"{print_styles.BOLD}Ingrese la contraseña: {print_styles.RESET}").strip()
                        if not validate_password(password):
                            print(f"{print_styles.RED}La contraseña no cumple los parametros requeridos.{print_styles.RESET}")
                            print(f"{print_styles.YELLOW}Tiene que tener mínimo entre 8-20 carácteres.{print_styles.RESET}")
                            continue

                        if not username or not email or not password:
                            print(f"{print_styles.YELLOW}Todos los campos son obligatorios.{print_styles.RESET}")
                        else:
                            add_user(username, email, password)
                            print(f"{print_styles.GREEN}Se añadió correctamente al usuario.{print_styles.RESET}")
                            break

                elif option == "3":
                    permission = has_permission(user, READ_WRITE)
                    if not permission:
                        break
                    try:
                        show_users()
                        user_id = int(input("Ingrese el id del usuario a eliminar: "))
                        if user_id == user['id']:
                            print(f"{print_styles.RED}No se puede eliminar al usuario actual, debe salir de la sesión e ingresar con otro usuario admin.{print_styles.RESET}")
                            break
                        delete_user(user_id)
                    except ValueError:
                        print(f"{print_styles.RED}Debes ingresar un número válido.{print_styles.RESET}")

                elif option == "4":
                    permission = has_permission(user, READ_WRITE)
                    if not permission:
                        break
                    try:
                        show_users()
                        user_id = int(input(f"{print_styles.BOLD}Ingrese el id del usuario: {print_styles.RESET}"))
                        new_password = input(f"{print_styles.BOLD}Ingrese la nueva contraseña: {print_styles.RESET}").strip()
                        if not validate_password(new_password):
                            print(f"{print_styles.RED}La contraseña no cumple los parametros requeridos.{print_styles.RESET}")
                            print(f"{print_styles.YELLOW}Tiene que tener mínimo entre 8-20 carácteres.{print_styles.RESET}")
                            continue
                        if not new_password:
                            print(f"{print_styles.YELLOW}La contraseña no puede estar vacía.{print_styles.RESET}")
                        else:
                            update_user_password(user_id, new_password)
                            print(f"{print_styles.GREEN}Contraseña actualizada correctamente.{print_styles.RESET}")
                    except ValueError:
                        print(f"{print_styles.RED}Debes ingresar un número válido.{print_styles.RESET}")
                    except:
                        print(f"{print_styles.RED}Ocurrió un error al intentar actualizar la contraseña.{print_styles.RESET}")

                elif option == "5":
                    permission = has_permission(user, READ_WRITE)
                    if not permission:
                        break
                    try:
                        show_users()
                        user_id = int(input(f"{print_styles.BOLD}Ingrese el id del usuario: {print_styles.RESET}"))
                        new_username = input(f"{print_styles.BOLD}Ingrese el nuevo username: {print_styles.RESET}").strip()
                        if not new_username:
                            print(f"{print_styles.YELLOW}El username no puede estar vacío.{print_styles.RESET}")
                        else:
                            update_user_username(user_id, new_username)
                            print(f"{print_styles.GREEN}Nombre de usuario actualizado correctamente.{print_styles.RESET}")
                    except ValueError:
                        print(f"{print_styles.RED}Debes ingresar un número válido.{print_styles.RESET}")
                    except:
                        print(f"{print_styles.RED}Ocurrió un error al intentar actualizar en usuario.{print_styles.RESET}")

                input("Presione ENTER para volver a seleccionar.")

        elif option == "2":   # Opción 2 --> Gestión de transacciones
            while True:
                while True:
                    options = 6
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Transacciones")
                    print("---------------------------")
                    if can_read:
                        print(f"{print_styles.BOLD}[1]{print_styles.RESET} Mostrar Transacciones")
                        print(f"{print_styles.BOLD}[2]{print_styles.RESET} Añadir Transacciones")            
                        if can_write:
                            print(f"{print_styles.BOLD}[3]{print_styles.RESET} Actualizar Transacciones")
                            print(f"{print_styles.BOLD}[4]{print_styles.RESET} Eliminar Transacciones")
                        print(f"{print_styles.BOLD}[5]{print_styles.RESET} Ver Transacciones por Categoria")
                        print(f"{print_styles.BOLD}[6]{print_styles.RESET} Ver Transacciones por usuario")
                    print("---------------------------")
                    print(f"{print_styles.BOLD}[0]{print_styles.RESET} Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    option = input("Seleccione una opción: ")
                    
                    if option in valid_options: 
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if option == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif option == "1":   # Opción 1
                    permission= has_permission(user,READ)
                    if permission:
                        data_transactions = json_reader(file_transactions)
                        data_accounts = json_reader(file_accounts)
                        data_categories = json_reader(file_categories)
                        get_transactions(data_transactions, data_accounts, data_categories)
                elif option == "2":   # Opción 2
                    permission = has_permission(user,READ)
                    if permission:
                        while True:

                            while True:
                                sub_options = 2
                                print()
                                print("---------------------------")
                                print("MENÚ PRINCIPAL > Gestión de Transacciones > Añadir")
                                print("---------------------------")
                                print(f"{print_styles.BOLD}[1]{print_styles.RESET} Opción 1 (Ingreso)")
                                print(f"{print_styles.BOLD}[2]{print_styles.RESET} Opción 2 (Egreso)")
                                print("---------------------------")
                                print(f"{print_styles.BOLD}[0]{print_styles.RESET} Volver al menú anterior")
                                print("---------------------------")
                                print()
                                
                                sub_option = input("Seleccione una opción: ")
                                if sub_option in [str(i) for i in range(0, sub_options + 1)]: 
                                    break
                                else:
                                    input("Opción inválida. Presione ENTER para volver a seleccionar.")
                            print()

                            if sub_option == "0":
                                break # Vuelve al menú de Gestión de Transacciones
                            
                            actual_date = datetime.now().date()
                            print(f"Su fecha actual es: {print_styles.YELLOW}{actual_date}{print_styles.RESET}, presione Enter si desea dejar la fecha actual")
                            date = input("Ingrese la fecha (formato: YYYY-MM-DD): ")
                            if len(date) == 0:
                                date = str(actual_date)
                            else:
                                message, is_valid = validate_date(date)
                                if not is_valid:
                                    print(f"{print_styles.RED}{message}{print_styles.RESET}")
                                    break
                            
                            parse_time = time(datetime.now().hour, datetime.now().minute)
                            print(f"Su hora actual es: {print_styles.YELLOW}{str(parse_time)[0:-3]}{print_styles.RESET}, presione Enter si desea dejar la hora actual")
                            actual_time = input("Ingrese la hora (formato: HH:MM): ")
                            if len(actual_time) == 0:
                                actual_time = str(parse_time)[0:-3]
                            else:
                                message, is_valid = validate_hour(actual_time)
                                if not is_valid:
                                    print(f"{print_styles.RED}{message}{print_styles.RESET}")
                                    break
                            try:
                                data_accounts = json_reader(file_accounts)
                                if data_accounts == None:
                                    break
                                get_accounts(data_accounts)
                                id_account = int(input("Ingrese el número de la cuenta: "))
                                if id_account>len(data_accounts) or id_account<=0:
                                    print(f"{print_styles.RED}Numero de cuenta invalida.Por favor ingrese una cuenta existente.{print_styles.RESET}")
                                    break
                                
                                data_categories = json_reader(file_categories)
                                if data_categories == None:
                                    break

                                get_categories(data_categories)
                                id_category = int(input("Ingrese el número de la categoria: "))
                                if id_category>len(data_categories) or id_category<=0:
                                    print(f"{print_styles.RED}Numero de categoria invalida.Por favor ingrese una categoria existente.{print_styles.RESET}")
                                    break
                                amount = int(input("Ingrese el importe: "))
                                descripcion = input("Ingrese la descripcion: ")
                                
                                data_transactions = json_reader(file_transactions)
                                if data_transactions == None:
                                    break

                                data_budgets = json_reader(file_budgets)
                                if data_budgets == None:
                                    break

                                if sub_option == "1":
                                    add_transaction(data_transactions, data_accounts, data_categories, data_budgets, id_account, id_category, date, actual_time, amount, descripcion, user["id"])
                                elif sub_option == "2":
                                    add_transaction(data_transactions, data_accounts, data_categories, data_budgets, id_account, id_category, date, actual_time, amount, descripcion, user["id"], "Expense")
                            except ValueError:                                                  
                                print(f"{print_styles.RED}Debes ingresar un número.{print_styles.RESET}")
                                break
                            except:
                                print(f"{print_styles.RED}Ha ocurrido un error.{print_styles.RESET}")
                                break
                                                       
                elif option == "3":   # Opción 3
                    permission = has_permission(user,READ_WRITE)
                    if permission:                        
                        data_transactions = json_reader(file_transactions)
                        data_accounts = json_reader(file_accounts)
                        data_categories = json_reader(file_categories)
                        data_budgets = json_reader(file_budgets)
                        
                        if (data_transactions or data_accounts or data_categories or data_budgets) == None:
                            break

                        get_transactions(data_transactions, data_accounts, data_categories)
                        transaction = get_transaction_by_user_input(data_transactions)

                        while transaction is not None:
                            print(f"\033[1;34m¿Qué campo de la transacción deseas actualizar?{print_styles.RESET}")
                            print(f"{print_styles.BOLD}[1]{print_styles.RESET} Cuenta")
                            print(f"{print_styles.BOLD}[2]{print_styles.RESET} Categoría")
                            print(f"{print_styles.BOLD}[3]{print_styles.RESET} Fecha")
                            print(f"{print_styles.BOLD}[4]{print_styles.RESET} Hora")
                            print(f"{print_styles.BOLD}[5]{print_styles.RESET} Importe")
                            print(f"{print_styles.BOLD}[6]{print_styles.RESET} Descripción")
                            print(f"{print_styles.BOLD}[0]{print_styles.RESET} Guardar y salir")
                            
                            sub_option = input("Seleccione una opción: ")
                            
                            if sub_option == "1":
                                update_account_transaction(transaction, data_transactions, data_accounts)
                            elif sub_option == "2":
                                update_category_transaction(transaction, data_transactions, data_categories)
                            elif sub_option == "3":
                                update_date_transaction(transaction, data_transactions)
                            elif sub_option == "4":
                                update_time_transaction(transaction, data_transactions)
                            elif sub_option == "5":
                                update_amount_transaction(transaction, data_transactions, data_accounts, data_budgets)
                            elif sub_option == "6":
                                update_description_transaction(transaction, data_transactions)
                            elif sub_option == "0":
                                print(f"{print_styles.GREEN}La transacción se actualizó con éxito.{print_styles.RESET}")
                                break
                            else:
                                print(f"{print_styles.RED}Opción no válida. Intente nuevamente.{print_styles.RESET}")
                elif option == "4":   # Opción 4
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        data_transactions = json_reader(file_transactions)
                        data_accounts = json_reader(file_accounts)
                        data_categories = json_reader(file_categories)
                        data_budgets = json_reader(file_budgets)
                        get_transactions(data_transactions, data_accounts, data_categories)

                        try: 
                            id = int(input("Que transaccion deseas eliminar? Indique el número o escriba 0 para salir: "))
                            while id < 0 or id > data_transactions[-1]['id']:
                                if id == 0:
                                    break
                                print(f"{print_styles.RED}El número ingresado no es válido.{print_styles.RESET}")
                                id = int(input("Que transaccion deseas eliminar? Indique el número o escriba 0 para salir: "))
                        except ValueError:
                            print(f"{print_styles.RED}Debes ingresar un número.{print_styles.RESET}")
                            break
                        except:
                            print(f"{print_styles.RED}Ha ocurrido un error.{print_styles.RESET}")
                            break
                            
                        if id != 0:
                            delete_transaction(data_transactions, data_accounts, data_categories, data_budgets, id)
                        else:
                            print(f"{print_styles.GREEN}No se elimino ninguna transacción.{print_styles.RESET}")
                elif option == "5":
                    permission = has_permission(user,READ)
                    if permission:
                        data_transactions = json_reader(file_transactions)
                        data_accounts = json_reader(file_accounts)
                        data_categories = json_reader(file_categories)
                        get_transactions_by_category(data_transactions, data_accounts, data_categories)
                elif option == "6":
                    permission = has_permission(user,READ)
                    try:
                        if permission:
                            show_users()
                            users = read_users()
                            id_input = int(input("Elige el número de usuario para mostrar sus transacciones: "))
                            while (id_input < 0 or id_input > users[-1]['id']):
                                if id_input == 0:
                                    break
                                print(f"{print_styles.RED}El usuario seleccionado no existe.{print_styles.RESET}")
                                id_input = int(input("Intente nuevamente: "))                    
                    except ValueError:
                        print(f"{print_styles.RED}Debes ingresar un número.{print_styles.RESET}")
                        break
                    except:
                        print(f"{print_styles.RED}Ha ocurrido un error.{print_styles.RESET}")
                        break

                    data_transactions = json_reader(file_transactions)
                    data_accounts = json_reader(file_accounts)
                    data_categories = json_reader(file_categories)
                    get_transactions(data_transactions, data_accounts, data_categories, lambda transaction: transaction['id_user'] == id_input)
                                                                                
                input("Presione ENTER para volver a seleccionar.")
        
        elif option == "3":   # Opción 3 --> Gestión de categorías

            while True:
                while True:
                    options = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Categorías")
                    print("---------------------------")
                    if can_read:
                        print(f"{print_styles.BOLD}[1]{print_styles.RESET} Mostrar Categorías")
                        print(f"{print_styles.BOLD}[2]{print_styles.RESET} Añadir Categoría")
                        if can_write:
                            print(f"{print_styles.BOLD}[3]{print_styles.RESET} Actualizar Categoría")
                            print(f"{print_styles.BOLD}[4]{print_styles.RESET} Eliminar Categoría")
                    print("---------------------------")
                    print(f"{print_styles.BOLD}[0]{print_styles.RESET} Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    option = input("Seleccione una opción: ")
                    if option in valid_options: 
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if option == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif option == "1":   # Opción 1
                    permission= has_permission(user,READ)
                    if permission:
                        categories=json_reader(file_categories)
                        get_categories(categories)
                elif option == "2":   # Opción 2
                    permission= has_permission(user,READ)
                    if permission:
                        category = input("Ingrese el nombre de la categoria: ")
                        while not category:
                            print(f"{print_styles.YELLOW}El nombre de la categoría no puede estar vacío.{print_styles.RESET}")
                            category = input("Ingrese el nombre de la categoria: ").strip()
                        categories=json_reader(file_categories)
                        add_category(categories, category)

                elif option == "3":   # Opción 3
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        categories=json_reader(file_categories)
                        update_category(categories)

                elif option == "4":   # Opción 4
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        transactions=json_reader(file_transactions)
                        budgets2=json_reader(file_budgets)
                        categories=json_reader(file_categories)
                        delete_category(categories, transactions, budgets2)
                                                        
                input("Presione ENTER para volver a seleccionar.")

        elif option == "4":   # Opción 4 --> Gestión de Presupuestos

            while True:
                while True:
                    options = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Presupuestos")
                    print("---------------------------")
                    if can_read:
                        print(f"{print_styles.BOLD}[1]{print_styles.RESET} Mostrar Presupuestos")
                        print(f"{print_styles.BOLD}[2]{print_styles.RESET} Añadir Presupuesto")
                        if can_write:
                            print(f"{print_styles.BOLD}[3]{print_styles.RESET} Actualizar Presupuestos")
                            print(f"{print_styles.BOLD}[4]{print_styles.RESET} Eliminar Presupuesto")
                    print("---------------------------")
                    print(f"{print_styles.BOLD}[0]{print_styles.RESET} Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    option = input("Seleccione una opción: ")
                    if option in valid_options: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if option == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif option == "1":   # Opción 1
                    permission = has_permission(user, READ)
                    if permission:
                        budgets2=json_reader(file_budgets)
                        categories=json_reader(file_categories)
                        get_budgets(budgets2, categories)
                elif option == "2":   # Opción 2
                    permission = has_permission(user, READ)
                    if permission:
                        budgets2=json_reader(file_budgets)
                        categories=json_reader(file_categories)
                        get_categories(categories)
                        while True:
                            try:

                                category_id = int(input("Ingrese el ID de la categoría: "))
                                break
                            except ValueError:
                                print(f"{print_styles.RED}Debe ingresar un numero valido de categoria.{print_styles.RESET}")
                            except Exception:
                                print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")
                                break
                        while True:
                            try:
                                limit_amount = int(input("Ingrese el monto limite para la categoría: "))
                                break
                            except ValueError:
                                print(f"{print_styles.RED}Debe ingresar un numero para el presupuesto.{print_styles.RESET}")
                            except Exception:
                                print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")
                                break
                        create_budget(budgets2, category_id, limit_amount, categories)

                elif option == "3":   # Opción 3
                    permission = has_permission(user, READ_WRITE)
                    if permission:                 
                        budgets2=json_reader(file_budgets)
                        categories=json_reader(file_categories)
                        get_budgets(budgets2, categories)
                        budget = get_budget_by_user_input(budgets2)

                        while budget is not None:
                            print("\033[1;34m¿Qué campo del presupuesto deseas actualizar?\033[0m")
                            print(f"{print_styles.BOLD}[1]{print_styles.RESET} Categoría")
                            print(f"{print_styles.BOLD}[2]{print_styles.RESET} Monto")
                            print(f"{print_styles.BOLD}[0]{print_styles.RESET} Guardar y salir")

                            option = input("Seleccione una opción: ")

                            if option == "1":
                                update_category_for_budget(budget, budgets2, categories)
                            elif option == "2":
                                update_budget_amount(budget, budgets2)
                            elif option == "0":
                                print("\033[32mEl presupuesto se actualizó con éxito.\033[0m")
                                break
                            else:
                                print("\033[31mOpción no válida. Intente nuevamente.\033[0m")

                elif option == "4":   # Opción 4
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        budgets2=json_reader(file_budgets)
                        categories=json_reader(file_categories)
                        delete_budget(budgets2, categories)
                                                        
                input("Presione ENTER para volver a seleccionar.")

        elif option == "5":   # Opción 5 --> Gestión de cuentas

            while True:
                while True:
                    options = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Cuentas")
                    print("---------------------------")
                    if can_read:
                        print(f"{print_styles.BOLD}[1]{print_styles.RESET} Mostrar Cuentas")
                        print(f"{print_styles.BOLD}[2]{print_styles.RESET} Añadir Cuentas")
                        if can_write:
                            print(f"{print_styles.BOLD}[3]{print_styles.RESET} Actualizar Cuentas")
                            print(f"{print_styles.BOLD}[4]{print_styles.RESET} Eliminar Cuentas")
                    print("---------------------------")
                    print(f"{print_styles.BOLD}[0]{print_styles.RESET} Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    option = input("Seleccione una opción: ")
                    if option in valid_options: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if option == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif option == "1":   # Opción 1
                    permission = has_permission(user,READ)
                    if permission:
                        accounts=json_reader(file_accounts)
                        get_accounts(accounts)
                elif option == "2":   # Opción 2
                    permission = has_permission(user,READ)
                   
                    if permission:
                        while True:
                            account_name = input("Ingrese el nombre de la cuenta: ").strip()
                            if account_name:  
                                break
                            print(f"{print_styles.RED}Error: El nombre de la cuenta no puede estar vacío.{print_styles.RESET}")
                        while True:
                            try:
                                total_money = int(input("Ingrese el monto de la cuenta: "))
                                break
                            except ValueError:
                                print(f"{print_styles.RED}Error: Debes ingresar un numero.{print_styles.RESET}")
                        accounts=json_reader(file_accounts)
                        add_account(accounts, account_name, total_money)    

                elif option == "3":   # Opción 3
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        accounts=json_reader(file_accounts)
                        get_accounts(accounts)

                        account = get_account_by_user_input(accounts)

                        while account is not None:
                            print(f"{print_styles.BOLD_BLUE}¿Qué campo de la cuenta deseas actualizar?{print_styles.RESET}")
                            print(f"{print_styles.BOLD}[1]{print_styles.RESET} Nombre")
                            print(f"{print_styles.BOLD}[2]{print_styles.RESET} Monto")
                            print(f"{print_styles.BOLD}[0]{print_styles.RESET} Guardar y salir")
                            
                            option = input("Selecciona una opción: ")
                            
                            if option == "1":
                                update_name_account(account,accounts)
                                
                            elif option == "2":
                                update_money_account(account,accounts)
                            elif option == "0":
                                print(f"{print_styles.GREEN}La cuenta se actualizó con éxito.{print_styles.RESET}")
                                break
                            else:
                                print(f"{print_styles.RED}Opción no válida. Intente nuevamente.{print_styles.RESET}")

                elif option == "4":   # Opción 4
                    permission = has_permission(user,READ_WRITE)
                    if permission:                        
                        allow_delete = input(f"{print_styles.YELLOW}Se borraran todas las transacciones relacionadas a esta cuenta{print_styles.RESET}, ¿desea proseguir? y/n: ")

                        while allow_delete != 'y' and allow_delete != 'n':
                            print(f"\n{print_styles.RED}No se reconoce el carácter{print_styles.RESET}")
                            allow_delete = input("¿Desea proseguir? y/n: ")

                        if (allow_delete == 'n'):
                            print(f"\n{print_styles.GREEN}No se borrará ninguna cuenta.{print_styles.RESET}")
                            break                        
                        accounts=json_reader(file_accounts)
                        get_accounts(accounts)
                        while True:
                            id_account_text = input("Que cuenta deseas eliminar? Indique el numero o escriba 0 para salir: ").strip()

                            if id_account_text == "":
                                print(f"{print_styles.RED}Debe ingresar un número válido.{print_styles.RESET}")
                                continue

                            try:
                                id_account = int(id_account_text)
                            except ValueError:
                                print(f"{print_styles.RED}Debe ingresar un número válido.{print_styles.RESET}")
                                continue

                            if id_account == 0:
                                print(f"{print_styles.GREEN}No se elimino ninguna cuenta.{print_styles.RESET}")
                                break

                            if id_account < 0 or id_account > len(accounts):
                                print(f"{print_styles.RED}Cuenta invalida. Debe ingresar una cuenta existente.{print_styles.RESET}")
                                continue
                            break

                        if id_account != 0:
                            transactions=json_reader(file_transactions)
                            related_accounts_transaction = list(filter(lambda x: x["id_account"] == id_account, transactions))
                            accounts=json_reader(file_accounts)
                            budgets=json_reader(file_budgets)
                            categories=json_reader(file_categories)
                            
                            for actual_transaction in related_accounts_transaction:
                                delete_transaction(transactions, accounts, categories, budgets, actual_transaction['id'])
                            delete_account(accounts, id_account)
                            
                        else:
                            print(f"{print_styles.GREEN}No se elimino ninguna cuenta.{print_styles.RESET}")

                input("Presione ENTER para volver a seleccionar.")

        elif option == "6":   # Opción 6 --> Resumen

            while True:
                while True:
                    options = 2
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Resumen")
                    print("---------------------------")
                    print(f"{print_styles.BOLD}[1]{print_styles.RESET} Ver resumen de gastos totales")
                    print(f"{print_styles.BOLD}[2]{print_styles.RESET} Ver resumen de gastos por categoría")
                    print("---------------------------")
                    print(f"{print_styles.BOLD}[0]{print_styles.RESET} Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    option = input("Seleccione una opción: ")
                    if option in [str(i) for i in range(0, options + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if option == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif option == "1":
                    accounts=json_reader(file_accounts)
                    transactions=json_reader(file_transactions)
                    categories=json_reader(file_categories)

                    total_balance = sum_accounts_amount(accounts)
                    print(f"Saldo total de todas las cuentas: ${total_balance}")

                    total, month = total_last_month(transactions)
                    print(f"Total Gastado en el mes de {month}: {total}")
                    print(f"Promedio de total gastado por mes: {average_month(transactions)}")
                    print(f"Categoria con mas gastos: {get_higher_expense(transactions, categories, 'id_category')['category']}")
                    print(f"Cuenta con mas gastos: {get_higher_expense(transactions, accounts, 'id_account')['account']}")
                elif option == "2":
                    transactions=json_reader(file_transactions)
                    categories=json_reader(file_categories)
                    
                    filter_transactions, total = calculate_percentage_of_category(transactions)
                    get_percentage_of_category(filter_transactions, total, categories)                
                
                input("Presione ENTER para volver a seleccionar.")
              
        print("\n\n")


# Punto de entrada al programa
main()