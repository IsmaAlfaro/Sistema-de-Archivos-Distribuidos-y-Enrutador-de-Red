
from tabla_hash import TablaHash

t = TablaHash()
print([t.funcion_hash(x) for x in ["ana", "naa", "aan"]])

t.registrar_usuario("ana", "1234")
print(t.autenticar("ana", "1234"))    # debe dar True
print(t.autenticar("ana", "mala"))    # debe dar False