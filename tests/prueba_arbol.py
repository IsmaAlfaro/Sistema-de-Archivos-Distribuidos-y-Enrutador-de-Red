import gc
import weakref

from estructuras.servidor import Servidor

# 1. Mismo nombre en otra rama: solo se borra el de la ruta indicada.
s = Servidor("S")
s.crear_nodo("c", True)
s.crear_nodo("docs", True, "/c")     # /c/docs
s.crear_nodo("docs", True)           # /docs
assert s.eliminar_nodo("/docs") is True
assert s.buscar_por_ruta("/docs") is None
assert s.buscar_por_ruta("/c/docs") is not None

# 2. Ruta inexistente, aunque haya un homónimo más profundo.
s = Servidor("S")
s.crear_nodo("c", True)
s.crear_nodo("docs", True, "/c")
assert s.eliminar_nodo("/docs") is False
assert s.buscar_por_ruta("/c/docs") is not None

# 3. Cascada sin huérfanos: los nodos eliminados dejan de existir en memoria.
s = Servidor("S")
s.crear_nodo("A", True)
s.crear_nodo("B", True, "/A")
s.crear_nodo("f.txt", False, "/A/B")
refs = [weakref.ref(s.buscar_por_ruta(r)) for r in ("/A", "/A/B", "/A/B/f.txt")]
assert s.eliminar_nodo("/A") is True
gc.collect()
assert all(r() is None for r in refs)

# 4. Nombres inválidos: vacío, solo espacios o con "/".
s = Servidor("S")
assert s.crear_nodo("", True) is False
assert s.crear_nodo("   ", False) is False
assert s.crear_nodo("a/b", True) is False
assert s.raiz.hijos == []             # no se creó ningún nodo
assert s.crear_nodo("ok", True) is True

print("Pruebas de árbol completadas correctamente.")
