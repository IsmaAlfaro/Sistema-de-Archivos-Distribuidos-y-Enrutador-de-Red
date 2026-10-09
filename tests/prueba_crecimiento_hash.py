from auditoria import configurar_auditoria
from tabla_hash import TablaHash


configurar_auditoria(False)
tabla = TablaHash()

# Siete usuarios todavía caben sin superar el límite.
for numero in range(7):
    assert tabla.registrar_usuario(
        f"usuario{numero}", f"Clave{numero}"
    )

assert tabla.cantidad == 7
assert tabla.tamaño == 10

# Un duplicado no debe aumentar el contador ni cambiar la contraseña.
assert tabla.registrar_usuario("usuario0", "OtraClave") is False
assert tabla.cantidad == 7
assert tabla.tamaño == 10

# El octavo usuario provoca el crecimiento de 10 a 20.
assert tabla.registrar_usuario("usuario7", "Clave7")
assert tabla.cantidad == 8
assert tabla.tamaño == 20

print("Primer crecimiento: 10 ->", tabla.tamaño)

# Los usuarios anteriores deben seguir autenticándose.
for numero in range(8):
    assert tabla.autenticar(f"usuario{numero}", f"Clave{numero}")

assert tabla.autenticar("usuario0", "OtraClave") is False

# Llegar a 16 usuarios provoca otro crecimiento: 20 -> 40.
for numero in range(8, 16):
    assert tabla.registrar_usuario(
        f"usuario{numero}", f"Clave{numero}"
    )

assert tabla.cantidad == 16
assert tabla.tamaño == 40

# Comprobar que todos siguen presentes, sin pérdidas ni duplicaciones.
assert sum(len(lista) for lista in tabla.tabla) == 16

for numero in range(16):
    assert tabla.autenticar(f"usuario{numero}", f"Clave{numero}")

print("Segundo crecimiento: 20 ->", tabla.tamaño)
print("Pruebas de crecimiento de la tabla hash completadas.")