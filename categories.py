from styles import print_styles
from helper import create_id, get_raw_by_id, json_loader
file_categories='json/categories.json'
def get_categories(data_categories):
    """
    data_categories: lista de categorías a mostrar
    Retorna: None. Imprime en pantalla la lista de categorías con su ID
    """
    count_matrix= len(data_categories)
    print("="*print_styles.MAX_SPACES_CATEGORIES)
    print(f'{"Categorias":^50}')
    print("="*print_styles.MAX_SPACES_CATEGORIES)
    print(f"{print_styles.BOLD_BLUE}Registros Totales: {count_matrix:<40}{print_styles.RESET}")
    print("="*print_styles.MAX_SPACES_CATEGORIES)
    print(f"{print_styles.BOLD}{'Numero':<20}{'Categoria':<30}{print_styles.RESET}")
    for i in range(len(data_categories)):
        id=data_categories[i]["id"]
        amount = data_categories[i]["category"]
        print(f"{print_styles.BOLD}{id:<20}{print_styles.RESET}{amount:<30}")
    return

def add_category(data_categories, category_name):
    """
    data_categories: lista de categorías a actualizar
    category_name: nombre de la nueva categoría
    Retorna: None. Agrega la nueva categoría si no existe
    """
    try:
        id=create_id(data_categories)
        if exists_category(category_name,data_categories):
            print(f"{print_styles.RED}La categoria ya existe. Ingrese otra por favor{print_styles.RESET}")
            return
        dicc_category={
            "id":id,
            "category":category_name,
        }
        data_categories.append(dicc_category)
        json_loader(file_categories,data_categories)
        print(f"{print_styles.GREEN}La categoría se ha creado con éxito.{print_styles.RESET}")
    except TypeError:
        print(f"{print_styles.RED}Error: Se esperaba una lista, pero se recibió otro tipo de dato.{print_styles.RESET}")
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error inesperado{print_styles.RESET}")

def delete_category(data_categories, data_transactions, data_budgets):
    """
    data_categories: lista de categorías del sistema
    data_transactions: lista de transacciones para actualizar en caso de eliminaciones
    data_budgets: lista de presupuestos para limpiar categorías eliminadas
    Retorna: None. Elimina una categoría y actualiza transacciones y presupuestos relacionados
    """
    try:
        get_categories(data_categories)
        id = int(input("Que categoria deseas eliminar? Indique el numero o escriba 0 para salir: "))
        delete=[]
        index=0
        
        if id == 1:
            print(f"{print_styles.RED}La categoría deseada no puede ser eliminada.{print_styles.RESET}")
            return
        
        if id <= 0:
            print(f"{print_styles.GREEN}No se elimino ninguna categoria.{print_styles.RESET}")
            return
        
        # Eliminar la categoría de la transacción
        for transaccion in data_transactions:
            if transaccion["id_category"] == id:
                transaccion["id_category"] = 1
        
    
        data_budgets[:] = list(filter(lambda x : x["id_category"] != id, data_budgets))
        
        for category in data_categories:
            if category["id"]==id:
                index=data_categories.index(category)
                delete=data_categories.pop(index)
                json_loader(file_categories,data_categories)
                print(f"{print_styles.GREEN}Operación realizada con éxito. Categoria eliminada correctamente.{print_styles.RESET}")
                return
        
        print(f"{print_styles.RED}La categoría no existe.{print_styles.RESET}")
    
    except ValueError:
        print(f"{print_styles.RED}Error: Por favor, ingrese un número válido.{print_styles.RESET}")
    except Exception:
        print(f"{print_styles.RED}Error inesperado.{print_styles.RESET}")

def update_category(data_categories):    
    """
    data_categories: lista de categorías del sistema
    Retorna: None. Solicita al usuario una categoría y actualiza su nombre
    """
    get_categories(data_categories)
    category = None
    while True:
        try:        
            id_category = int(input("¿Que categoría desea actualizar? Indique el numero o escriba 0 para salir: "))
                
            if id_category < 0 or id_category > len(data_categories):
                print(f"{print_styles.RED}Número invalido. Vuelva a ingresar un ID{print_styles.RESET}")
                continue

            if id_category == 0:
                print(f"{print_styles.YELLOW}No se actualizo ninguna categoría.{print_styles.RESET}")
                return
                
            if id_category == 1:
                print(f"{print_styles.RED}La categoría deseada no puede ser actualizada.{print_styles.RESET}")
                return

            category = get_raw_by_id(data_categories, id_category)
            
            if category is not None:                
                change_category(category,data_categories)
                print(f"{print_styles.GREEN}La categoría deseada puedo ser actualizada.{print_styles.RESET}")
                break
            else:
                print(f"{print_styles.RED}La categoría no existe.{print_styles.RESET}")
        except ValueError:
            print(f"{print_styles.RED}Error. Por favor, ingrese un número entero válido.{print_styles.RESET}")
        except Exception:
            print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")
            break

def change_category(category,data_categories):
    """
    category: registro de categoría a modificar
    data_categories: array de categorias en el sistema
    Retorna: None. Solicita un nuevo nombre y actualiza la categoría
    """
    try:
        name_category = input("Ingrese un nuevo nombre de categoría: ")
        while len(name_category.strip())== 0:
            print(f"{print_styles.YELLOW}El valor que ingreso no tiene valor o no es una palabra.{print_styles.RESET}")
            name_category = input("Ingrese un nuevo nombre de categoría: ")
        category["category"] = name_category
        json_loader(file_categories,data_categories)
    except TypeError:
        print(f"{print_styles.RED}Error: El formato de la categoría es inválido. Intente nuevamente con otra categoria{print_styles.RESET}")
    except Exception:
        print(f"{print_styles.RED}Error inesperado.{print_styles.RESET}")

def exists_category(category, data_categories):
    """
    category: nombre de categoría a buscar
    data_categories: lista de categorías existentes
    Retorna: True si la categoría ya existe, False en caso contrario
    """
    category_lower= category.lower()
    exists= list(filter(lambda x:x["category"].lower()==category_lower, data_categories))
    return True if len(exists) else False