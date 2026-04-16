from datetime import datetime, date, time

def create_id(matrix):
    """
    matrix: lista de elementos existente
    Retorna: un nuevo identificador basado en el tamaño de la matriz
    """
    id=len(matrix) + 1
    return id

def get_raw_by_id(matrix, id):
    """
    matrix: lista de registros donde el primer elemento es el id
    id: identificador a buscar
    Retorna: el registro que coincide con el id o None si no existe
    """
    for raw in matrix:
        if raw[0] == id:
            return raw
    return None

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
    parse_hour = datetime.strptime(hour_input, "%H:%M").time()
    
    actual_hour = time(datetime.now().hour, datetime.now().minute)
    
    if parse_hour > actual_hour:
        return "Inválida. La hora ingresada es mayor a la actual", False
    
    return "", True

def validate_date(date_input):
    """
    date_input: fecha en formato YYYY-MM-DD
    Retorna: tupla (mensaje, bool) indicando si la fecha es válida y está dentro del rango permitido
    """
    parse_date = datetime.strptime(date_input, "%Y-%m-%d").date()
    
    min_limit = date(1980, 1, 1)
    max_limit = datetime.today().date()
    
    if parse_date < min_limit:
        return f"[{date_input}] Inválida: Es anterior a 1980.", False
    elif parse_date > max_limit:
        return f"[{date_input}] Inválida: Es una fecha futura.", False
    
    return "", True
    
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

def get_month(value_month):
    """
    value_month: número de mes del 1 al 12
    Retorna: nombre del mes en español o mensaje de error si no existe
    """
    return months.get(value_month, "No existe el mes ingresado")