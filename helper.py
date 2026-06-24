from datetime import datetime, date, time
from styles import print_styles
import json

months = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

def create_id(array):
    """
    matrix: lista de elementos existente
    Retorna: un nuevo identificador basado en el tamaño de la matriz
    """
    id=array[-1]["id"] + 1
    return id

def get_raw_by_id(matrix, id):
    """
    matrix: lista de registros donde el primer elemento es el id
    id: identificador a buscar
    Retorna: el registro que coincide con el id o None si no existe
    """
    return get_raw(matrix, id, 0)

def get_raw(matrix, id, index=0):
    """
    Obtener una lista de registros mediante recursion
    matrix: lista de registros donde el primer elemento es el id
    id: identificador a buscar
    Retorna: el registro que coincide con el id o None si no existe
    """
    if index >= len(matrix) or index < 0:
        return None

    if matrix[index]["id"] == id:
        return matrix[index]
        
    return get_raw(matrix, id, index + 1)

def slice_words(length, word):
    """
    length: longitud máxima permitida
    word: texto a truncar
    Retorna: palabra truncada con '...' si excede la longitud, o la palabra original
    """
    sliced_word=f"{word[:length-3]}..." if len(word)>length else word
    return sliced_word

def is_word_alpha(word):
    """
    word: texto a validar
    Retorna: True si la palabra contiene al menos una letra y no tiene caracteres no alfabéticos
    """
    has_letters = False

    for car in word:
        if car == " ":
            continue

        if not car.isalpha():
            return False
    
        has_letters = True

    return has_letters

def validate_hour(hour_input):
    """
    hour_input: hora en formato HH:MM
    Retorna: tupla (mensaje, bool) indicando si la hora es válida y si no es futura
    """
    try:
        parse_hour = datetime.strptime(hour_input, "%H:%M").time()
        
        actual_hour = time(datetime.now().hour, datetime.now().minute)
        
        if parse_hour > actual_hour:
            return "Inválida. La hora ingresada es mayor a la actual", False
        
        return "", True
    except ValueError:
        return "Formato de hora inválido. Use HH:MM", False
    except:
        return "Ocurrió un error inesperado", False

def validate_date(date_input):
    """
    date_input: fecha en formato YYYY-MM-DD
    Retorna: tupla (mensaje, bool) indicando si la fecha es válida y está dentro del rango permitido
    """
    try:
        parse_date = datetime.strptime(date_input, "%Y-%m-%d").date()
        
        min_limit = date(1980, 1, 1)
        max_limit = datetime.today().date()
        
        if parse_date < min_limit:
            return f"[{date_input}] Inválida: Es anterior a 1980.", False
        elif parse_date > max_limit:
            return f"[{date_input}] Inválida: Es una fecha futura.", False
        
        return "", True
    except ValueError:
        return "Formato de fecha inválido. Use YYYY-MM-DD", False
    except:
        return "Ocurrió un error inesperado", False

def json_reader(file):
    '''
    Lee el contenido de un archivo en formato JSON.

    file: ruta del archivo JSON que se desea leer
    Retorna: Los datos cargados desde el archivo, o None si ocurre un error
    '''
    try:
        with open(file,'r', encoding="UTF-8") as file_information:
            data=json.load(file_information)
            return data
    except FileNotFoundError:
        print(f"{print_styles.RED}No se ha encontrado el archivo. Intente mas tarde.{print_styles.RESET}")
        return None
    except OSError:
        print(f"{print_styles.RED}Ocurrió un error inesperado en el sistema al abrir el archivo.{print_styles.RESET}")
        return None
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")
        return None

def json_loader(file, data):
    """
    Guarda datos estructurados en un archivo en formato JSON.

    file: ruta del archivo donde se guardarán los datos
    data: estructura de datos que se va a almacenar
    Retorna: None
    """
    try:
        with open(file,'w', encoding="UTF-8") as file_information:
            json.dump(data,file_information,ensure_ascii=False,indent=4)
    except OSError:
        print(f"{print_styles.RED}Error del sistema al acceder al archivo.{print_styles.RESET}")
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")
    
        
def get_month(value_month):
    """
    value_month: número de mes del 1 al 12
    Retorna: nombre del mes en español o mensaje de error si no existe
    """
    return months.get(value_month, "No existe el mes ingresado")