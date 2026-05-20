from traceback import print_list
from styles import print_styles
from helper import create_id, get_raw_by_id, is_word_alpha

def get_categories(matrix_categories):
    """
    matrix_categories: lista de categorías a mostrar
    Retorna: None. Imprime en pantalla la lista de categorías con su ID
    """
    count_matrix= len(matrix_categories)
    print("="*print_styles.MAX_SPACES_CATEGORIES)
    print(f'{"Categorias":^50}')
    print("="*print_styles.MAX_SPACES_CATEGORIES)
    print(f"{print_styles.BOLD_BLUE}Registros Totales: {count_matrix:<40}{print_styles.RESET}")
    print("="*print_styles.MAX_SPACES_CATEGORIES)
    print(f"{print_styles.BOLD}{'Numero':<20}{'Categoria':<30}{print_styles.RESET}")
    for i in range(len(matrix_categories)):
        id=matrix_categories[i]["id"]
        amount = matrix_categories[i]["category"]
        print(f"{print_styles.BOLD}{id:<20}{print_styles.RESET}{amount:<30}")
    return

def add_category(matrix_categories, category_name):
    """
    matrix_categories: lista de categorías a actualizar
    category_name: nombre de la nueva categoría
    Retorna: None. Agrega la nueva categoría si no existe
    """
    try:
        id=create_id(matrix_categories)
        if exists_category(category_name,matrix_categories):
            print(f"{print_styles.RED}La categoria ya existe. Ingrese otra por favor{print_styles.RESET}")
            return
        matrix_categories.append([id, category_name])
        print(f"{print_styles.GREEN}La categoría se ha creado con éxito.{print_styles.RESET}")
    except TypeError:
        print(f"{print_styles.RED}Error: Se esperaba una lista, pero se recibió otro tipo de dato.{print_styles.RESET}")
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error inesperado{print_styles.RESET}")

def delete_category(matrix_categories, matrix_transactions, matrix_budgets):
    """
    matrix_categories: lista de categorías del sistema
    matrix_transactions: lista de transacciones para actualizar en caso de eliminaciones
    matrix_budgets: lista de presupuestos para limpiar categorías eliminadas
    Retorna: None. Elimina una categoría y actualiza transacciones y presupuestos relacionados
    """
    try:
        get_categories(matrix_categories)
        id = int(input("Que categoria deseas eliminar? Indique el numero o escriba 0 para salir: "))
        delete=[]
        index=0
        
        if id == 1:
            print("\033[31mLa categoría deseada no puede ser eliminada.\033[0m")
            return
        
        if id <= 0:
            print("\033[32mNo se elimino ninguna categoria.\033[0m")
            return
        
        # Eliminar la categoría de la transacción
        for transaccion in matrix_transactions:
            if transaccion[2] == id:
                transaccion[2] = 1
        
    
        matrix_budgets[:] = list(filter(lambda x : x[1] != id, matrix_budgets))
        
        for category in matrix_categories:
            if category[0]==id:
                index=matrix_categories.index(category)
                delete=matrix_categories.pop(index)
                print(f"{print_styles.GREEN}Operación realizada con éxito. Categoria eliminada correctamente.{print_styles.RESET}")
                return
        
        print(f"{print_styles.RED}La categoría no existe.{print_styles.RESET}")
    
    except ValueError:
        print(f"{print_styles.RED}Error: Por favor, ingrese un número válido.{print_styles.RESET}")
    except Exception:
        print(f"{print_styles.RED}Error inesperado.{print_styles.RESET}")

def update_category(matrix_categories):    
    """
    matrix_categories: lista de categorías del sistema
    Retorna: None. Solicita al usuario una categoría y actualiza su nombre
    """
    get_categories(matrix_categories)
    category = None
    while True:
        try:        
            id_category = int(input("¿Que categoría desea actualizar? Indique el numero o escriba 0 para salir: "))
                
            if id_category < 0 or id_category > len(matrix_categories):
                print(f"{print_styles.RED}Número invalido. Vuelva a ingresar un ID{print_styles.RESET}")
                continue

            if id_category == 0:
                print(f"{print_styles.YELLOW}No se actualizo ninguna categoría.{print_styles.RESET}")
                return
                
            if id_category == 1:
                print(f"{print_styles.RED}La categoría deseada no puede ser actualizada.{print_styles.RESET}")
                return

            category = get_raw_by_id(matrix_categories, id_category)
            
            if category is not None:                
                change_category(category)
                print(f"{print_styles.GREEN}La categoría deseada puedo ser actualizada.{print_styles.RESET}")
                break
            else:
                print(f"{print_styles.RED}La categoría no existe.{print_styles.RESET}")
        except ValueError:
            print(f"{print_styles.RED}Error: Por favor, ingrese un número entero válido.{print_styles.RESET}")
        except Exception:
            print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")
            break

def change_category(category):
    """
    category: registro de categoría a modificar
    Retorna: None. Solicita un nuevo nombre y actualiza la categoría
    """
    try:
        name_category = input("Ingrese un nuevo nombre de categoría: ")
        while len(name_category) == 0 or not is_word_alpha(name_category):
            print(f"{print_styles.YELLOW}El valor que ingreso no tiene valor o no es una palabra.{print_styles.RESET}")
            name_category = input("Ingrese un nuevo nombre de categoría: ")
        category[1] = name_category
    except TypeError:
        print(f"{print_styles.RED}Error: El formato de la categoría es inválido. Intente nuevamente con otra categoria{print_styles.RESET}")
    except Exception:
        print(f"{print_styles.RED}Error inesperado.{print_styles.RESET}")

def exists_category(category, matrix_categories):
    """
    category: nombre de categoría a buscar
    matrix_categories: lista de categorías existentes
    Retorna: True si la categoría ya existe, False en caso contrario
    """
    category_lower= category.lower()
    exists= list(filter(lambda x:x[1].lower()==category_lower, matrix_categories))
    return True if len(exists) else False