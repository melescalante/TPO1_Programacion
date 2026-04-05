from data import accounts, transactions, categories, budgets
from transactions import *
from budgets import *
from categories import *
from accounts import *
from user import *


#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    #-------------------------------------------------
    # Inicialización de variables
    #----------------------------------------------------------------------------------------------
    clientes = {...}


    #-------------------------------------------------
    # Bloque de menú
    #----------------------------------------------------------------------------------------------
    while True:
        while True:
            opciones = 4
            print()
            print("---------------------------")
            print("MENÚ PRINCIPAL")
            print("---------------------------")
            print("[1] Gestión de Transacciones")
            print("[2] Gestión de Categorías")
            print("[3] Gestión de Presupuestos")
            print("[4] Gestión de Cuentas")
            print("---------------------------")
            print("[0] Salir del programa")
            print("---------------------------")
            print()
            
            opcion = input("Seleccione una opción: ")
            if opcion in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                break
            else:
                input("Opción inválida. Presione ENTER para volver a seleccionar.")
        print()

        if opcion == "0": # Opción salir del programa
            exit() # También puede ser sys.exit() para lo cual hay que importar el módulo sys

        elif opcion == "1":   # Opción 1
            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Transacciones")
                    print("---------------------------")
                    print("[1] Mostrar Transacciones")
                    print("[2] Añadir Transacciones")
                    print("[3] Actualizar Transacciones")
                    print("[4] Eliminar Transacciones")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    opcion = input("Seleccione una opción: ")
                    if opcion in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcion == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif opcion == "1":   # Opción 1
                    get_transactions(transactions)
                elif opcion == "2":   # Opción 2
                    name_account = input("Ingrese el nombre de la cuenta: ")
                    name_category = input("Ingrese la categoria: ")
                    date = input("Ingrese la fecha: ")
                    time = input("Ingrese la hora: ")
                    amount = int(input("Ingrese el importe: "))
                    descripcion = input("Ingrese la descripcion: ")
                    month = input("Ingrese el mes: ")                    
                    add_transaction(name_account,name_category,date,time,amount,descripcion,month)

                elif opcion == "3":   # Opción 3

                    update_transaction(transactions,accounts,categories)
                elif opcion == "4":   # Opción 4
                    delete_transaction()

        elif opcion == "2":   # Opción 2

            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Categorías")
                    print("---------------------------")
                    print("[1] Mostrar Categorías")
                    print("[2] Añadir Categoría")
                    print("[3] Actualizar Categoría")
                    print("[4] Eliminar Categoría")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    opcion = input("Seleccione una opción: ")
                    if opcion in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcion == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif opcion == "1":   # Opción 1
                    get_categories(categories)
                elif opcion == "2":   # Opción 2
                    categoria = input("Ingrese el nombre de la categoria: ")
                    add_category(categoria)

                elif opcion == "3":   # Opción 3
                    update_category(categories)

                elif opcion == "4":   # Opción 4
                    delete_category(transactions,budgets)

        elif opcion == "3":   # Opción 3

            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Presupuestos")
                    print("---------------------------")
                    print("[1] Mostrar Presupuestos")
                    print("[2] Añadir Presupuesto")
                    print("[3] Actualizar Presupuestos")
                    print("[4] Eliminar Presupuesto")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    opcion = input("Seleccione una opción: ")
                    if opcion in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcion == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif opcion == "1":   # Opción 1
                    get_budgets(budgets)
                elif opcion == "2":   # Opción 2
                    get_categories(categories)
                    category_id = int(input("Ingrese el ID de la categoría: "))
                    limit_amount = int(input("Ingrese el monto limite para la categoría: "))
                    create_budget(category_id, limit_amount, categories)

                elif opcion == "3":   # Opción 3
                    update_budget(budgets,categories)

                elif opcion == "4":   # Opción 4
                    delete_budget(budgets)

        elif opcion == "4":   # Opción 4

            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Cuentas")
                    print("---------------------------")
                    print("[1] Mostrar Cuentas")
                    print("[2] Añadir Cuentas")
                    print("[3] Actualizar Cuentas")
                    print("[4] Eliminar Cuentas")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    opcion = input("Seleccione una opción: ")
                    if opcion in [str(i) for i in range(0, opciones + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcion == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif opcion == "1":   # Opción 1
                    get_accounts(accounts)
                elif opcion == "2":   # Opción 2
                    account_name = input("Ingrese el nombre de la cuenta: ")
                    total_money = input("Ingrese el monto de la cuenta: ")
                    add_account(account_name, total_money)

                elif opcion == "3":   # Opción 3
                    update_account(accounts)

                elif opcion == "4":   # Opción 4
                    delete_account()

        print("\n\n")


# Punto de entrada al programa
main()