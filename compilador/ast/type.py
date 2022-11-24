from enum import Enum

# A built-in primitive type (int, bool, str, etc).
class BuiltinType(Enum):
    BOOLEAN = 'booleano'
    STRING = 'cadena'
    CHAR = 'caracter'
    INT = 'entero'
    VOID = 'vacio'

Type = BuiltinType
