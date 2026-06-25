from helper import create_id, validate_date, slice_words, get_raw_by_id
from permissions import has_permission

def test_create_id_retorna_siguiente_id():
    lista = [{"id": 1}, {"id": 2}, {"id": 3}]
    resultado = create_id(lista)
    assert resultado == 4, "create_id debe retornar el id del último elemento + 1"


def test_validate_date_rechaza_fecha_futura():
    mensaje, es_valida = validate_date("2099-01-01")
    assert es_valida == False, "Una fecha futura no debe ser válida"


def test_slice_words_trunca_texto_largo():
    resultado = slice_words(10, "Hola Mundo Como Estas")
    assert resultado == "Hola Mu...", "Un texto más largo que el límite debe quedar truncado con '...'"


def test_get_raw_by_id_retorna_elemento_correcto():
    lista = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}, {"id": 3, "nombre": "Pedro"}]
    resultado = get_raw_by_id(lista, 2)
    assert resultado == {"id": 2, "nombre": "Luis"}, "Debe retornar el elemento cuyo id coincide"


def test_has_permission_usuario_no_tiene_permiso_admin():
    usuario = {"id": 3, "rol": "user", "username": "Test", "password": "1234", "email": "test@test.com"}
    resultado = has_permission(usuario, 2)  # 2 = nivel admin (READ_WRITE)
    assert resultado == False, "Un usuario con rol 'user' no debe tener permiso de admin"

