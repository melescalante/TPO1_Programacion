from styles import print_styles
from categories import get_categories
from helper import create_id, get_raw_by_id, json_loader
from functools import reduce


def update_budget_balance(data_budgets, id_budget, amount):
    """
    data_budgets: lista de presupuestos a actualizar
    id_budget: identificador del presupuesto
    amount: monto a sumar o restar al presupuesto
    Retorna: None. Modifica el saldo del presupuesto correspondiente
    """
    for budget in data_budgets:
        if budget['id'] == id_budget:
            budget['amount'] += amount
            json_loader('json/budgets.json', data_budgets)
            return

def get_budget_by_user_input(data_budgets):
    """
    data_budgets: lista de presupuestos disponibles
    Retorna: presupuesto seleccionado por el usuario o None si cancela
    """
    while True:
        try: 
            id_budget = int(input("¿Qué presupuesto desea actualizar? Indique el número o escriba 0 para salir: "))    
            
            if id_budget < 0 or id_budget > data_budgets[-1]["id"]:
                print("\033[31mEntrada inválida. Debe ingresar un número.\033[0m")
                continue

            if id_budget == 0:
                print("\033[32mNo se actualizó ningún presupuesto.\033[0m")
                return

            budget = get_raw_by_id(data_budgets, id_budget)
            
            if budget is None:
                print(f"{print_styles.RED}El presupuesto no existe. Intente de nuevo.{print_styles.RESET}")
                continue

            return budget
        except ValueError:
            print(f"{print_styles.RED}Debes ingresar un número.{print_styles.RESET}")
        except:
            print(f"{print_styles.RED}Ha ocurrido un error.{print_styles.RESET}")
            break

        
def get_budgets(data_budgets, data_categories):
    """
    data_budgets: lista de presupuestos a mostrar
    data_categories: lista de categorías para resolver nombres
    Retorna: None. Imprime una tabla de presupuestos
    """
    count_matrix= len(data_budgets)
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f'{"Presupuestos":^60}')
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f"{print_styles.BOLD_BLUE}Registros Totales: {count_matrix:<40}{print_styles.RESET}")
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f"{print_styles.BOLD}{'Numero':<10}{'Categoria':<25}{'Monto':<25}{print_styles.RESET}")
    for i in range(len(data_budgets)):
        id=data_budgets[i]["id"]
        category = get_raw_by_id(data_categories,data_budgets[i]["id_category"])
        amount = data_budgets[i]["amount"]
        amount_str = "$"+str(data_budgets[i]["amount"])
        underline = print_styles.UNDERLINE_INCOME
        if amount<0:
            underline = print_styles.UNDERLINE_EXPENSE
        print(f"{underline}{id:<10}{category["category"]:<25}{amount_str:<25}{print_styles.RESET}")
    

def create_budget(data_budgets, category_id, limit_amount, data_categories):
    """
    data_budgets: lista de presupuestos a actualizar
    category_id: identificador de la categoría para el presupuesto
    limit_amount: monto límite asignado al presupuesto
    data_categories: lista de categorías existentes
    Retorna: None. Agrega un nuevo presupuesto si la categoría existe y el monto es válido
    """
    id_budget = create_id(data_budgets)
    category = get_raw_by_id(data_categories, category_id)

    if category is None:
        print("\033[31mLa categoría no existe. Por favor, cree una.\033[0m")
        return
    
    id_category = category["id"]
    if exists_budget(id_category,data_budgets):
        print(f"{print_styles.RED}La categoria ya tiene un presupuesto existente. Ingrese otra por favor{print_styles.RESET}")
        return
    if limit_amount < 0:
        print("\033[31mEl presupuesto a asignar debe ser positivo.\033[0m")
        return
    
    data_budgets.append({"id": id_budget, "id_category": id_category, "amount": limit_amount})
    json_loader('json/budgets.json', data_budgets)
    print(f"{print_styles.GREEN}Se ha creado el presupuesto correctamente.{print_styles.RESET}")


def delete_budget(data_budgets, data_categories):    
    """
    data_budgets: lista de presupuestos disponibles
    data_categories: lista de categorías para mostrar antes de eliminar
    Retorna: None. Elimina el presupuesto seleccionado por el usuario
    """
    try:
        get_budgets(data_budgets, data_categories)    
        id = int(input("Ingrese el id o 0 para no eliminar ningún presupuesto: "))

        if id <= 0:
            return
        
        budget_deleted = None
        index = -1
        
        for budget in data_budgets:
            if (budget["id"] == id):
                index = data_budgets.index(budget)
                data_budgets.pop(index)
                json_loader('json/budgets.json', data_budgets)
                print("\033[32mOperación realizada con éxito. Presupuesto eliminado correctamente.\033[0m")
                return
        
        print("\033[31mNo se encontró el presupuesto a eliminar.\033[0m")    
    except ValueError:
        print(f"{print_styles.RED}Debes ingresar un número.{print_styles.RESET}")
    except:
        print(f"{print_styles.RED}Ha ocurrido un error.{print_styles.RESET}")

def update_category_for_budget(budget, data_budgets, data_categories):
    """
    budget: registro de presupuesto a actualizar
    data_categories: lista de categorías válidas
    data_budgets: lista de presupuestos existentes
    Retorna: None. Actualiza la categoría asignada al presupuesto
    """
    try: 
        get_categories(data_categories)
        id_category = int(input("¿Qué categoría desea asignar? Indique el número o escriba 0 para cancelar: "))
        if id_category == 0:
            print("\033[32mNo se actualizó la categoría.\033[0m")
            return
        
        category = get_raw_by_id(data_categories, id_category)
        while category is None:
            print("\033[31mLa categoría no existe.\033[0m")

            id_category = int(input("¿Por cuál categoría desea actualizar? Indique el numero o escriba 0 para salir: "))
            if id_category == 0:
                print("\033[32mNo se actualizo la categoría.\033[0m")
                return
            category = get_raw_by_id(data_categories, id_category)
        
        if exists_budget(id_category, data_budgets):
            print(f"{print_styles.RED}La categoria ya tiene un presupuesto existente. Ingrese otra por favor{print_styles.RESET}")
            return

        budget["id_category"] = id_category
        json_loader('json/budgets.json', data_budgets)
        print("\033[32mCategoría actualizada.\033[0m")
    except ValueError:
        print(f"{print_styles.RED}Debes ingresar un número.{print_styles.RESET}")
    except:
        print(f"{print_styles.RED}Ha ocurrido un error.{print_styles.RESET}")

def update_budget_amount(budget, data_budgets):
    """
    budget: registro de presupuesto a modificar
    data_budgets: lista de presupuestos existentes
    Retorna: None. Solicita y actualiza el monto del presupuesto
    """
    try: 
        budget_amount = input("Ingrese el nuevo monto del presupuesto: ")
        while not budget_amount.isnumeric():
            print("\033[33mEl valor que ingresó no es un número válido.\033[0m")
            budget_amount = input("Ingrese el nuevo monto del presupuesto: ")
        
        budget["amount"] = int(budget_amount)
        json_loader('json/budgets.json', data_budgets)
        print("\033[32mMonto actualizado.\033[0m")
    except ValueError:
        print(f"{print_styles.RED}Debes ingresar un número.{print_styles.RESET}")
    except:
        print(f"{print_styles.RED}Ha ocurrido un error.{print_styles.RESET}")

def get_budget_by_category(data_budgets,id_category):
    """
    data_budgets: lista de presupuestos existentes
    id_category: identificador de categoría a buscar
    Retorna: registro del presupuesto asociado a la categoría
    """
    register= reduce(lambda x,y: y if y['id_category']==id_category else x, data_budgets)
    return register

def exists_budget(id_category, data_budgets):
    """
    id_category: id de categoría a buscar
    data_budgets: lista de budgets existentes
    Retorna: True si la categoría ya existe en un presupuesto, False en caso contrario
    """
    exists= list(filter(lambda x:x["id_category"]==id_category, data_budgets))
    return True if len(exists) else False