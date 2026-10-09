# Sistema de Archivos Distribuido y Enrutador de Red

Proyecto de Investigación Aplicada #2 del curso EIF207 - Estructuras de Datos.
Universidad Nacional, Sección Regional Central Occidente.

Simulación por consola del núcleo lógico de un sistema operativo de red. Cada
servidor administra un árbol de archivos y una tabla local de credenciales. La red
conecta los servidores mediante enlaces ponderados por latencia. Incluye BFS para
diagnóstico, Dijkstra para rutas óptimas y un archivo de auditoría de operaciones.

## Funcionalidades

### Implementadas

- Selección entre tres servidores con archivos y usuarios independientes.
- Registro e inicio de sesión mediante tabla hash manual con encadenamiento.
- Normalización de espacios exteriores del usuario al registrar y autenticar.
- Captura de contraseñas con asteriscos, Retroceso y Enter en la consola de Windows.
- Selección de servidores con manejo de entradas no numéricas y números fuera de rango.
- Creación de carpetas y archivos, rechazando nombres vacíos, solo espacios o con `/`.
- Búsqueda recursiva por nombre y navegación por rutas.
- Visualización del árbol con indentación.
- Eliminación por ruta exacta: selección del hijo directo y vaciado recursivo en cascada.
- Grafo ponderado no dirigido mediante listas de adyacencia.
- Creación y eliminación de conexiones con latencias finitas y positivas.
- BFS con recorrido, no alcanzables, aislados y estado de conectividad.
- Dijkstra manual, reconstrucción de ruta y simulación de envío con saltos y costo total.
- Auditoría de creación/eliminación de nodos, conexiones, rutas, altas de usuarios y accesos exitosos o fallidos.
- Consulta del log completo, desde una fecha o para una fecha específica.
- Manejo de errores de escritura de auditoría en los menús operativos.
- Menús principal, archivos, autenticación y red con `match/case`.

`main()` crea una sola red con los mismos objetos `Servidor` utilizados por los
menús de archivos y autenticación. La pasa a `menuRed(red)` sin reconstruirla al
entrar o salir. Usuarios, nodos y conexiones se mantienen en memoria durante la
ejecución; el historial de auditoría persiste en `network_audit_log.txt`.

La auditoría se activa después de crear los servidores iniciales. El diagnóstico
BFS no registra un evento actualmente. Su recorrido no es una ruta de envío.

### Pendientes conocidos

- Rechazar credenciales vacías y validar el tamaño inicial de la tabla hash.
- Definir el tratamiento de saltos de línea en los datos de auditoría. La lectura admite `~` en la acción, pero no un origen con ese separador ni eventos multilínea.
- Diferenciar un log vacío de un log cuyos registros fueron todos omitidos por formato inválido.
- Controlar el factor de carga de la tabla hash y considerar módulo en cada paso del hash para acotar el acumulador.
- Reutilizar validación de fechas, simplificar consultas dinámicas de funciones y mejorar portabilidad de la limpieza de consola (`cls`).
- Separar menús por carpetas después de estabilizar la integración.
- Completar las bitácoras de IA de cada integrante y revisar las ampliaciones semanales del docente.

## Estructuras y técnicas implementadas

- **Árbol general:** `NodoArchivo` guarda nombre, tipo y lista de hijos; cada servidor tiene raíz `/`.
- **Recursividad:** búsqueda por nombre, visualización y vaciado desde los descendientes antes de retirar su carpeta.
- **Tabla hash manual:** buckets con listas de colisiones y hash polinómico de base 7, que considera el orden de los caracteres.
- **Grafo ponderado no dirigido:** listas paralelas `servidores` y `adyacencias`; cada vecino se representa como `(indice_vecino, latencia)`.
- **BFS:** cola implementada con lista e índice de lectura y marcas de visitados para evitar repeticiones.
- **Dijkstra:** selección lineal del mínimo no visitado, relajación y reconstrucción con predecesores.
- **Auditoría:** append UTF-8 con fecha y hora. Revisa solo el último byte antes de escribir para no unir registros, sin leer todo el historial.
- **Excepciones:** los menús distinguen operaciones inválidas (`ValueError`) y fallos del archivo de auditoría (`OSError`).

## Ejecución y pruebas

Requiere **Windows y Python 3.10 o superior**. No hay dependencias externas.
La captura con asteriscos utiliza `msvcrt.getwch`; ejecutar en una terminal real,
como la terminal integrada de VS Code. La máscara oculta la escritura en pantalla,
pero no cambia el almacenamiento en memoria de las contraseñas.
Ejecutar desde la raíz del repositorio:

```bash
python main.py
```

Pruebas disponibles:

```bash
python -m tests.prueba_red
python -m tests.practica_enrutamiento
python -m tests.prueba_arbol
python prueba_hash.py
python -m unittest tests.test_integracion -v
```

Las tres primeras son scripts con `assert`; ejecutarlas sin `-O`, que desactiva
las aserciones. `prueba_hash.py` es una demostración por consola; la suite de
integración añade comprobaciones automatizadas del hash y de los módulos combinados.
La prueba de enrutamiento se movió de `practica_grafo.py` a
`tests/practica_enrutamiento.py`; no existe `tests/prueba_enrutamiento.py`.

En PowerShell, si `python` no resuelve el intérprete instalado en el entorno de Ismael:

```powershell
& "C:\msys64\ucrt64\bin\python.exe" main.py
& "C:\msys64\ucrt64\bin\python.exe" -B -m tests.prueba_red
& "C:\msys64\ucrt64\bin\python.exe" -B -m tests.practica_enrutamiento
& "C:\msys64\ucrt64\bin\python.exe" -B -m tests.prueba_arbol
& "C:\msys64\ucrt64\bin\python.exe" -B -m unittest tests.test_integracion -v
```

`-B` evita generar cachés. Los scripts parten con auditoría desactivada; las
pruebas de integración usan archivos temporales o simulaciones y no escriben en
el historial real del proyecto.

### Cobertura de las pruebas

| Área | Comprobaciones |
|---|---|
| Red | Enlaces en ambos sentidos, duplicados, extremos inexistentes, autoenlaces, eliminación y preservación de otros enlaces. |
| BFS | Aislados, red conectada, componentes separados, ciclos y origen inexistente. |
| Dijkstra | Rutas directas e indirectas, costo mínimo, ruta inversa, destino desconectado, origen igual al destino, red vacía, predecesores y decimales. |
| Árbol | Rutas exactas, nombres repetidos en distintas ramas, cascada con referencias débiles y rechazo de nombres inválidos. |
| Integración | Hash con orden y colisiones, latencias no finitas, escritura/lectura de auditoría, filtros por fecha y manejo de fallos del log en los menús. |

Resultado de la verificación de esta integración: los scripts de red,
enrutamiento y árbol pasaron; la demostración del hash ejecutó correctamente.
La suite `tests.test_integracion` incluye 12 pruebas, con subcasos para
ocho operaciones de menú con fallos simulados de auditoría, captura con asteriscos,
Retroceso, teclas especiales, normalización de usuarios y selección de servidores.
Las pruebas simulan tanto `input()` como la captura oculta para no esperar teclado.
Esto cubre los casos
descritos, no elimina los pendientes conocidos de validación indicados arriba.

### Validación manual reportada

| Integrante / acción | Resultado observado |
|---|---|
| Ismael: conectar 1–2 con 10 ms y 2–3 con 15 ms. | Conexiones agregadas y recorrido BFS `Servidor 1 -> Servidor 2 -> Servidor 3`. |
| Ismael: eliminar el enlace 2–3 y diagnosticar desde 1. | Servidor 3 aislado y no alcanzable. |
| Carlos: agregar además el enlace 1–3 con 30 ms y simular envío de 1 a 3. | Dijkstra elige 1–2–3 con costo 25 ms, mostrando cada salto. |
| Ismael: registrar `Ana~Maria` y consultar auditoría. | Nombre y fecha se muestran sin romper el formato. |
| Ismael: eliminar una carpeta con descendientes. | Eliminación en cascada reportada; las pruebas automatizadas comprueban también la selección por ruta. |

## Estructura de módulos

```text
main.py                    Menús y construcción de los componentes compartidos.
servidor.py                Árbol y usuarios locales de cada servidor.
nodo_archivo.py            Nodos, búsqueda, visualización y vaciado recursivo.
tabla_hash.py              Hash manual, colisiones, registro y autenticación.
grafo_red.py               Única implementación oficial del grafo y BFS.
enrutamiento.py            Dijkstra, reconstrucción y simulación de envío.
auditoria.py               Escritura del log, lectura y filtros por fecha.
prueba_hash.py             Demostración de distribución y autenticación.
tests/
    __init__.py            Paquete de pruebas.
    prueba_red.py          Conexiones y diagnóstico.
    practica_enrutamiento.py  Pruebas de rutas y envío.
    prueba_arbol.py        Rutas, cascada y nombres inválidos.
    test_integracion.py    Regresiones de la combinación de ramas.
.gitignore                 Exclusión de cachés de Python.
README.md                  Documentación y bitácora.
network_audit_log.txt       Historial de auditoría de la ejecución interactiva.
```

La implementación alternativa `grafo.py` se retiró siguiendo el cambio de Carlos;
no era utilizada por `main.py` ni por Dijkstra. La carpeta local `menus/` sigue
reservada para una organización posterior; Git no registra carpetas vacías.

## Bitácora de desarrollo

Actualización del **8 de octubre de 2026**: integración de `origin/main` en
`Ismael-Dev`, tomando como referencias `009e9d5` y `8068b6e`. Carlos ya estaba
integrado en main mediante el PR #10. La comparación se hizo sobre código e
historial Git, no únicamente sobre las descripciones del README.

### Módulos de Archivos, Servidores y Autenticación - Alannah

| Fecha | Evidencia Git | Avance documentado |
|---|---|---|
| 2026-09-23 | `4d47cb6`, `c585217`, `249ce92` | Estructura inicial, hijos, búsqueda y visualización. |
| 2026-09-24 | `c29ab3c`, `53567b2`, `2c70199`, `c7c14de`, `2eefe20`, `c8a8fce` | Servidor, eliminación, creación y manejo de rutas. |
| 2026-09-24 | `7969ca7`, `423778a`, `1b59e7d`, `7e33983` | Prompts, tabla hash e integración inicial con main. |
| 2026-09-28 | `2aa4b35`, `5d4caea`, `8f4e3ca` | Grafo alternativo, prompts y actualización de main. |

Estado actual: se conserva la base de árboles, usuarios y servidores, con las
correcciones posteriores de Ismael y Carlos para eliminar por ruta exacta y
validar nombres. Andrés incorporó el contexto del servidor a los eventos de usuarios.

<details>
<summary><strong>Prompts y adaptación al proyecto - Alannah</strong></summary>

Prompts conservados del README original. Las adaptaciones se observan en código;
no se atribuyen pruebas manuales no reportadas. La numeración original omitía el 9.

| N.º / Función | Prompt utilizado | Adaptación observable |
|---|---|---|
| 1. Nodo | `Necesito crear una clase NodoArchivo en Python para representar archivos y carpetas mediante un árbol. Cada nodo debe tener un nombre, indicar si es una carpeta y tener una lista de hijos y explícame el código para poder entenderlo.` | Atributos `nombre`, `es_carpeta` e `hijos`. |
| 2. Hijos | `Cómo agrego un nodo hijo a una carpeta? Quiero que solamente las carpetas puedan tener hijos y que los archivos se mantengan como nodos hoja.` | `agregar_hijo` comprueba el tipo. |
| 3. Búsqueda | `Tengo que implementar una búsqueda recursiva en el árbol para encontrar un archivo o carpeta por su nombre. Explícame cómo funciona la recursividad en este caso.` | Recorrido del nodo y sus descendientes. |
| 4. Visualización | `Cómo muestro en consola toda la estructura del árbol de archivos y carpetas utilizando indentación para distinguir los diferentes niveles` | Indentación por nivel. |
| 5. Rutas | `Quiero poder crear archivos y carpetas usando una ruta, ejemplo /Universidad/Tareas. Como hago para buscar la carpeta correspondiente utilizando la ruta y crear el nodo dentro de?` | Localización de la carpeta padre. |
| 6. Duplicados | `Si tengo dos carpetas que se llaman igual pero están en lugares diferentes del árbol, como hago para distinguirlas? Ocupo una funcion que me ayude a verificar que los nombres no sean iguales.` | Rutas y rechazo de nombres repetidos dentro del mismo padre. |
| 7. Hash | `Necesito usar una tabla hash en Python para guardar usuarios y contraseñas, debe utilizar el nombre del usuario para calcular la posición, me explicas que debo hacer y como hacerlo.` | Buckets y encadenamiento manual. |
| 8. Registro | `Como hago para verificar que un usuario ya se registro en la tabla hash?` | Búsqueda de duplicados en su bucket. |
| 10. Autenticación | `Necesito autenticar un usuario buscando su nombre en la tabla hash y comprobar que la contraseña ingresada coincida con la guardada.` | Comparación de credenciales en el bucket calculado. |

</details>

### Módulo Red de Servidores y Diagnóstico - Ismael

| Evidencia Git | Avance documentado |
|---|---|
| `b32f689` | Ignorado de cachés. |
| `f43be98` | Grafo por listas y pruebas de red. |
| `cab1d01`, `a683f82` | Documentación y plan de mejoras. |
| `4290ba8` | Integración inicial del menú de red. |
| `2fd3211`, `6a92be2` | Actualización del README y sus commits. |
| `8068b6e` | Comentarios, correcciones, optimización de auditoría y menús con match/case. |
| `77b8d4c` | Unificación de las mejoras de Ismael y Carlos y pruebas de integración. |
| `a6ea90f` | Normalización del usuario con strip y conversión segura en el selector de servidores. |

Se conservan su validación de latencias finitas, comentarios de funciones, manejo
de errores de auditoría y menús. La escritura del log ya no lee todo el historial;
la lectura conserva `~` dentro de la acción y omite registros inválidos con aviso.

<details>
<summary><strong>Prompts y validación humana - Ismael</strong></summary>

Extractos de la conversación; algunos requieren el contexto de capturas o pasos anteriores.

| Función | Prompt utilizado / extracto | Adaptación y validación |
|---|---|---|
| Inicio | `bueno yo me encargo de red de servidores y diagnostico, ahora podemos empezar con esa parte` | Grafo no dirigido con listas paralelas. |
| Errores | `sigamo ese codigo pero cn esta funcion` | Se adoptó ValueError para duplicados. |
| Retornos | `es igual al return tur?` | Se eligieron mensajes de confirmación para operaciones exitosas. |
| Sangría | `asi?` | Se revisaron capturas y se movió la inserción fuera del ciclo de duplicados. |
| Pruebas | `como pruebo` | Script con aserciones y ejecución reportada por el usuario. |
| Ejecución | `cual carpeta me pongo para probar` | Uso de raíz del repositorio e intérprete instalado. |
| Imports | `meti la prueba a una carpeta y al compilar me sale eso?` | Paquete tests y ejecución como módulo. |
| Eliminación | `listo` / `todo bien` | Pruebas reportadas de eliminación de enlaces. |
| BFS | `ya hice el diagnostacar red` / `sip` | Pruebas de aislamiento, componentes y ciclos. |
| Menús | `tu me recomiendas meter todos los menus en un archivo o un archivo por menu y una carpeta de menus?` | Organización por áreas prevista para una etapa posterior. |
| Integración | `lo que vamos a hacer es hacer todo y depues sepepararlo a carpetas, podrias mostrarme no cambiando codigo internamente que haria yo para conectarlo a la funcionalidad del main` (espaciado normalizado) | Menú en main con una red compartida. |
| Match/case | `podrias hacer el menu de red con switch, quiero ver como se implementa en python` | Selección de opciones con match/case. |
| Validación manual | `y para provarlo` | Capturas de enlaces, BFS y servidor aislado. |
| Cachés | `Me podrias decir como ignorar los cahes` | .gitignore y comprobación con Git. |
| README | `quiero que cambies el readme nuevo usando siempre este tipo obviamente con los datos nuevos` | Formato del proyecto anterior con evidencias del actual. |
| Revisión | `ahora si observa todo el proyecto y dime que errores hay, o optimzaciones o cambios para hacer` | Revisión y reproducción de errores en memoria. |
| Plan | `okey actualiza el readme con todo lo nuevo y despues me vas guiando para ir poco a poco con todo lo que hay que arreglar, optimizar o mejorar` | Correcciones aplicadas manualmente y comprobadas por etapas. |
| Comentarios | `quiero primero que hagas el favor de ponerle comentarios a todo el codigo eso puedes hacerlo tu` (extracto, espaciado normalizado) | IA documentó funciones; se comparó la estructura sintáctica para comprobar que la lógica no cambiara. |
| Unificación | `tu podrias hacerme el favor de unir lo que recomendaste a mi rama? para despues subirlo al main?` | Integración autorizada de las mejoras de ambas ramas, resolución por archivo y pruebas de regresión. |
| Contraseñas | `con asteriscos` | Captura manual con getwch, edición con Retroceso y máscara en consola; pruebas actualizadas para simular el teclado. |
| Publicación | `analisa el mi rama y si ya no hay cambios muy drasticos subela al main` | Revisión contra main y verificación de las pruebas antes de publicar los cambios pendientes. |

</details>

### Módulo Enrutamiento y Validaciones - Carlos Víquez

| Evidencia Git | Avance documentado |
|---|---|
| `7b2b2e9`, `6cbf398` | Dijkstra, reconstrucción y pruebas; PR #6. |
| `d2a7a6e`, `588c5d6` | Integración de envío en el menú; PR #7. |
| `43f7049` | Eliminación exacta, nombres válidos, hash de base 7, pruebas del árbol y organización de enrutamiento. |
| `b6b317a` | PR #10: incorporación de esos arreglos a main. |
| `f84ccd8`, `009e9d5` | Actualizaciones del README en main. |

`enrutamiento.py` trabaja con índices sobre `GrafoRed`. Distingue servidores
inexistentes, destinos desconectados y origen igual al destino; devuelve ruta,
latencias por salto y costo total. La lógica coincide en las dos ramas comparadas.
La unificación conserva además las validaciones y pruebas de Carlos.

Pendiente documental: Carlos debe aportar los prompts utilizados y sus
adaptaciones; no se reconstruyen conversaciones que no fueron compartidas.

### Módulo Auditoría y Menús - Andrés Segura

| Fecha según historial Git consultado | Evidencia Git | Avance documentado |
|---|---|---|
| 2026-10-04 | `5c5ddc8`, `68cd354`, `49fd4f7`, `8f4f1c6`, `2b33a6f` | Creación y ajustes del módulo funcional de auditoría. |
| 2026-10-04 | `d10e57b`, `1c5e75c`, `395b044`, `6498d88`, `c2b9979`, `9f8204d` | Eventos de enrutamiento, conexiones y archivos. |
| 2026-10-05 | `f7a1e2b` | Actualización de la presentación de auditoría. |
| 2026-10-06 | `ffcb377`, `d712c5a` | Eventos de usuarios y contexto del servidor. |
| 2026-10-06 | `67fb847`, `e31456d`, `04fb76c` | Filtros de fecha, activación del log y actualización de menús. |

Se conserva el motor de auditoría, su configuración para pruebas y los filtros
por fecha. Ismael mejoró posteriormente la escritura, lectura tolerante y manejo
de errores desde los menús. Andrés debe completar sus prompts y validaciones
reportadas. Los eventos de autenticación se generan en `TablaHash`, no en BFS.

### Historial de integraciones observable

| Evidencia Git | Operación documentada |
|---|---|
| `21ed4d4` | Commit inicial. |
| `d2c110f`, `280caba`, `c778a84`, `803e085` | PRs #1–#4 desde Alannah. |
| `c98a289` | Integración de main en Carlos. |
| `10f6e2f`, `6cbf398`, `588c5d6` | PRs #5–#7 desde Carlos. |
| `7cf499e`, `888f9a8` | PRs #8–#9 desde Andrés-Dev. |
| `43f7049`, `b6b317a` | Validaciones y pruebas de Carlos; integración por PR #10. |
| `a683f82`, `8068b6e` | Avances de Ismael posteriores a la base común `888f9a8`. |
| `f84ccd8`, `009e9d5` | Documentación posterior al PR #10 en main. |
| `77b8d4c`, `a6ea90f`, `6e07e43` | Unificación, validaciones posteriores e integración de Ismael-Dev en main mediante PR #11. |

Las tablas de módulos y esta sección identifican los commits revisados. No son
un registro de todas las operaciones de fetch o push.

### Resolución de la integración actual

| Área | Decisión |
|---|---|
| Menús, auditoría y validación de latencias | Conservar las mejoras de Ismael. |
| Eliminación por ruta | Ambas ramas tenían la misma corrección; mantenerla con comentarios. |
| Creación de nodos y hash | Incorporar validación de nombres y fórmula de Carlos. |
| Pruebas | Conservar el árbol de Carlos y reunir enrutamiento en tests, manteniendo comentarios. |
| Grafo alternativo | Aceptar su eliminación: el sistema usa grafo_red.py. |
| README | Reconciliar estado actual y conservar prompts y aportes de todos, sin marcar pendientes como resueltos. |

## Plan de correcciones y mejoras

| Estado | Área |
|---|---|
| Integrado | Selección del hijo directo y eliminación recursiva en cascada. |
| Integrado | Rechazo de nombres de nodos inválidos. |
| Integrado | Latencias finitas y positivas. |
| Integrado | Lectura del log con ~ dentro de la acción y omisión de líneas inválidas. |
| Integrado | Escritura sin lectura completa del historial y manejo de OSError en menús. |
| Integrado | Hash que considera el orden, pruebas del árbol y una sola clase de grafo oficial. |
| Integrado | Usuario normalizado, selector numérico robusto y contraseña con asteriscos en Windows. |
| Pendiente | Credenciales vacías y tamaño de tabla. |
| Pendiente | Datos multilínea de auditoría y distinción entre log vacío y log sin entradas válidas. |
| Pendiente | Factor de carga, acumulador hash acotado, portabilidad y organización por carpetas. |

## Complejidad de las estructuras y algoritmos

### Árbol de directorios

Sea N el número de nodos, H su altura y S el tamaño del subárbol eliminado.

| Operación | Complejidad | Explicación |
|---|---|---|
| Buscar por nombre | O(N) en el peor caso | Recorrido recursivo; pila O(H). |
| Buscar por ruta | O(suma de hijos examinados por nivel) | Cada componente se localiza entre hijos directos. |
| Vaciar subárbol | O(S) | Procesa descendientes y limpia sus enlaces; pila según altura. |

Python recupera los objetos cuando dejan de existir referencias a ellos. Las
pruebas de cascada usan referencias débiles para comprobar esa condición.

### Tabla hash

La fórmula acumula `suma = suma * 7 + ord(letra)` y devuelve `suma % tamaño`.
Realiza L iteraciones para un usuario de longitud L. Como el módulo se aplica
al final, el entero crece; para claves muy largas el costo aritmético no es
constante. Aplicarlo en cada paso es una optimización pendiente equivalente.

Registrar y autenticar recorren el bucket calculado. Para cadenas acotadas y
buena distribución el acceso puede ser cercano a O(1) promedio; en el peor caso
se recorren U usuarios. Hay 10 buckets por defecto y no existe redimensionamiento.

### Grafo, BFS y Dijkstra

V es el número de servidores y E el de conexiones no dirigidas.

| Operación | Complejidad |
|---|---|
| Almacenar el grafo | O(V + E) memoria; cada arista se guarda en ambos extremos. |
| Buscar/agregar servidor | O(V) por búsqueda de nombre. |
| Agregar conexión | O(V + grado(origen)). |
| Eliminar conexión | O(V + grado(origen) + grado(destino)). |
| BFS | O(V + E) tiempo en el peor caso y O(V) memoria auxiliar. |
| Dijkstra | O(V² + E), equivalente a O(V²) para este grafo simple; O(V) memoria auxiliar. |
| Reconstruir ruta | O(V) en el peor caso. |

### Auditoría

| Operación | Complejidad |
|---|---|
| Registrar evento | O(L) respecto al tamaño del evento; revisa como máximo un byte previo, sin recorrer el historial. |
| Leer registros | O(B) para cargar un archivo de B caracteres, más interpretación de campos. |
| Filtrar por fecha | O(R) comparaciones para R registros, además de la lectura. |

La escritura del log añade su costo de E/S a las operaciones auditadas. La
simulación es secuencial; no implementa coordinación de escritores concurrentes.
