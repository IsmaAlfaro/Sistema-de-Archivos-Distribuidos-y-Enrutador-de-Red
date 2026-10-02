# Sistema de Archivos Distribuido y Enrutador de Red

Proyecto de Investigación Aplicada #2 del curso EIF207 - Estructuras de Datos.
Universidad Nacional, Sección Regional Central Occidente.

Simulación por consola del núcleo lógico de un sistema operativo de red. Cada
servidor administra su propio árbol de archivos y sus credenciales de acceso.
La red representa conexiones entre servidores con latencias en milisegundos.
El objetivo completo incluye diagnóstico de conectividad, enrutamiento de
paquetes por el camino más corto y auditoría de las operaciones.

## Funcionalidades

### Implementadas

- Selección entre tres servidores desde el programa principal.
- Registro e inicio de sesión con credenciales locales por servidor.
- Creación de archivos y carpetas bajo una ruta existente.
- Búsqueda recursiva por nombre y navegación por rutas.
- Visualización del árbol de directorios con indentación.
- Eliminación recursiva del contenido de carpetas; la selección por ruta tiene un ajuste pendiente descrito abajo.
- Registro de servidores en un grafo, evitando nombres duplicados.
- Creación y eliminación de conexiones bidireccionales con latencia positiva.
- Diagnóstico BFS: recorrido, servidores no alcanzables, servidores aislados y estado de conectividad.
- Pruebas de conexiones, eliminación y diagnóstico de red con `assert`.

El módulo de red está disponible mediante `GrafoRed` y sus pruebas. Su integración
con los menús de `main.py` está pendiente. Los usuarios, archivos y conexiones se
mantienen en memoria durante la ejecución.

### Pendientes

- Implementar Dijkstra y reconstruir la ruta de menor latencia.
- Simular el envío de paquetes mostrando cada salto y el costo total.
- Registrar automáticamente fecha, hora y detalle de eventos en `network_audit_log.txt` mediante append.
- Consultar el archivo de auditoría desde el menú.
- Integrar conexiones, diagnóstico y enrutamiento en el menú utilizando los mismos objetos `Servidor`.
- Completar la organización de menús por módulos.
- Corregir la eliminación por ruta: seleccionar al hijo directo de la carpeta padre antes de borrar su subárbol. Actualmente la búsqueda puede eliminar un descendiente de otra ruta con el mismo nombre.
- Validar nombres de archivos y carpetas para rechazar valores vacíos o que contengan `/`.
- Revisar la distribución y el crecimiento de la tabla hash para limitar las colisiones.
- Incorporar y documentar las ampliaciones semanales que publique el docente.

## Estructuras y técnicas implementadas

- **Árbol general:** cada `NodoArchivo` contiene nombre, tipo y lista de hijos. La raíz de cada servidor es `/` y los archivos se mantienen como hojas mediante la operación de agregar hijos.
- **Recursividad:** búsqueda por nombre, visualización y vaciado de subárboles desde los descendientes.
- **Tabla hash manual:** arreglo de listas, función propia basada en la suma de `ord()` y módulo por el tamaño de la tabla. Las colisiones se resuelven mediante encadenamiento.
- **Grafo ponderado no dirigido:** listas paralelas de servidores y adyacencias; cada conexión almacena `(indice_vecino, latencia)` en ambos extremos.
- **BFS:** cola implementada con una lista y un índice de lectura, más una lista de visitados para evitar repeticiones.
- **Excepciones:** las operaciones inválidas de la red lanzan `ValueError`; el menú deberá capturarlas para informar al usuario.

## Ejecución y pruebas

Requiere Python 3. Los módulos actuales no necesitan paquetes externos.
Ejecutar desde la raíz del repositorio:

```bash
python main.py
```

Ejecutar las pruebas de red:

```bash
python -m tests.prueba_red
```

Las pruebas actuales son un script con `assert`, no una suite de `unittest`.
Se ejecutan como módulo para que los imports encuentren `servidor.py` y
`grafo_red.py` desde la raíz. Deben ejecutarse sin la opción `-O`, que desactiva
las aserciones.

En el entorno de desarrollo de Ismael, si el comando `python` no está disponible
en PowerShell, se utiliza la ruta del intérprete instalado:

```powershell
& "C:\msys64\ucrt64\bin\python.exe" main.py
& "C:\msys64\ucrt64\bin\python.exe" -m tests.prueba_red
```

El último mensaje esperado de las pruebas es:

```text
Pruebas de diagnóstico completadas correctamente.
```

### Cobertura actual de las pruebas de red

| Área | Casos comprobados por el script |
|---|---|
| Conexiones | Almacenamiento en ambos sentidos, duplicados directos e inversos, servidor inexistente, conexión consigo mismo y latencias negativas o cero. |
| Eliminación | Borrado en ambos sentidos, conservación de servidores y otras conexiones, enlace inexistente y servidor inexistente. |
| Diagnóstico | Servidor aislado, reconexión de toda la red, componentes separados sin nodos aislados, ciclos sin visitas repetidas y origen inexistente. |

Ismael reportó la ejecución satisfactoria de estas pruebas durante el desarrollo
guiado. Esto verifica los casos anteriores; la integración completa del programa
todavía debe probarse cuando estén disponibles los demás módulos.

## Estructura de módulos

```text
main.py              Selección de servidor, autenticación y menú de archivos.
servidor.py          Árbol y tabla de usuarios locales de cada servidor.
nodo_archivo.py      Nodos, búsqueda, visualización y eliminación recursiva.
tabla_hash.py        Función hash, encadenamiento, registro y autenticación.
grafo_red.py         Servidores, conexiones ponderadas y diagnóstico BFS.
tests/
    __init__.py      Identifica el paquete de pruebas.
    prueba_red.py    Pruebas de conexiones, eliminación y diagnóstico.
.gitignore           Exclusión de cachés de Python.
README.md            Documentación y bitácora de desarrollo e IA.
```

La copia local contiene una carpeta `menus/` vacía, reservada para la organización
de los menús. Por ahora las funciones de menú siguen en `main.py`; Git no registra
carpetas vacías.

## Bitácora de desarrollo

Esta bitácora se elaboró a partir del código y del historial Git local disponible
el 2 de octubre de 2026, junto con la conversación de desarrollo de Ismael.
Las responsabilidades confirmadas son: Alannah desarrolló la base de archivos,
servidores, autenticación y menús; Ismael trabajó la red y su diagnóstico.
Los responsables de enrutamiento y auditoría/integración quedan por confirmar
en esta documentación.

### Módulos de Archivos, Servidores y Autenticación - Alannah

| Fecha | Evidencia Git | Avance documentado |
|---|---|---|
| 2026-09-23 | `4d47cb6`, `c585217`, `249ce92` | Estructura inicial, incorporación de hijos, búsqueda y visualización del árbol. |
| 2026-09-24 | `c29ab3c`, `53567b2`, `2c70199` | Eliminación de nodos, clase `Servidor` y operaciones básicas de creación. |
| 2026-09-24 | `c7c14de`, `2eefe20`, `c8a8fce` | Búsqueda por ruta, manejo de nodos mediante rutas y mejora de la creación. |
| 2026-09-24 | `7969ca7`, `423778a`, `1b59e7d`, `7e33983` | Registro de prompts, tabla hash, importación en servidor y programa principal. |

Estado actual: `NodoArchivo` representa la jerarquía; `Servidor` agrupa el árbol y
las credenciales; `TablaHash` registra y autentica usuarios mediante encadenamiento.
`main.py` expone selección de servidor, registro, inicio de sesión y archivos.

<details>
<summary><strong>Prompts y adaptación al proyecto - Alannah</strong></summary>

Los siguientes prompts se conservan del README original. La adaptación descrita
se observa en el código actual; no se atribuyen pruebas manuales que no hayan sido
reportadas. Se mantiene la numeración original, que no incluía un prompt 9.

| N.º / Función | Prompt utilizado | Adaptación observable |
|---|---|---|
| 1. Modelo de nodo | `Necesito crear una clase NodoArchivo en Python para representar archivos y carpetas mediante un árbol. Cada nodo debe tener un nombre, indicar si es una carpeta y tener una lista de hijos y explícame el código para poder entenderlo.` | `NodoArchivo` contiene `nombre`, `es_carpeta` e `hijos`. |
| 2. Agregar hijos | `Cómo agrego un nodo hijo a una carpeta? Quiero que solamente las carpetas puedan tener hijos y que los archivos se mantengan como nodos hoja.` | `agregar_hijo` verifica `es_carpeta` antes de agregar a la lista. |
| 3. Búsqueda recursiva | `Tengo que implementar una búsqueda recursiva en el árbol para encontrar un archivo o carpeta por su nombre. Explícame cómo funciona la recursividad en este caso.` | `buscar` revisa el nodo actual y después sus descendientes. |
| 4. Visualización | `Cómo muestro en consola toda la estructura del árbol de archivos y carpetas utilizando indentación para distinguir los diferentes niveles` | `mostrar_arbol` recibe el nivel e incrementa la indentación al recorrer hijos. |
| 5. Creación por ruta | `Quiero poder crear archivos y carpetas usando una ruta, ejemplo /Universidad/Tareas. Como hago para buscar la carpeta correspondiente utilizando la ruta y crear el nodo dentro de?` | `Servidor.crear_nodo` localiza la carpeta padre con `buscar_por_ruta`. |
| 6. Nombres repetidos | `Si tengo dos carpetas que se llaman igual pero están en lugares diferentes del árbol, como hago para distinguirlas? Ocupo una funcion que me ayude a verificar que los nombres no sean iguales.` | Se usan rutas y se rechazan nombres repetidos entre hijos de una misma carpeta. |
| 7. Tabla hash | `Necesito usar una tabla hash en Python para guardar usuarios y contraseñas, debe utilizar el nombre del usuario para calcular la posición, me explicas que debo hacer y como hacerlo.` | `TablaHash` usa suma de códigos de caracteres, módulo y listas de colisiones. |
| 8. Usuarios duplicados | `Como hago para verificar que un usuario ya se registro en la tabla hash?` | `registrar_usuario` revisa el bucket correspondiente antes de insertar. |
| 10. Autenticación | `Necesito autenticar un usuario buscando su nombre en la tabla hash y comprobar que la contraseña ingresada coincida con la guardada.` | `autenticar` compara usuario y contraseña en el bucket calculado. |

</details>

### Módulo Red de Servidores y Diagnóstico - Ismael

| Fecha | Evidencia Git | Avance documentado |
|---|---|---|
| 2026-09-25 | `b32f689` | Incorporación de `.gitignore` para los cachés de Python. |
| 2026-10-02 | `f43be98` | Incorporación de `grafo_red.py`, paquete `tests` y pruebas de red. |

Estado actual: `GrafoRed` registra servidores y almacena conexiones bidireccionales
con latencias positivas. Permite agregar y eliminar enlaces y diagnosticar la red
mediante BFS. Devuelve los nombres visitados, los no alcanzables, los aislados y
un booleano que indica si toda la red es alcanzable desde el origen.

La IA propuso fragmentos de implementación, explicaciones y pruebas. Ismael los
incorporó manualmente, solicitó utilizar `ValueError` para duplicados, consultó
el uso de mensajes de retorno y corrigió la indentación y los imports durante
las ejecuciones. La validación de latencia se adaptó para exigir valores mayores
que cero.

<details>
<summary><strong>Prompts y validación humana - Ismael</strong></summary>

Se incluyen extractos textuales de la conversación. Cuando el mensaje dependía
de una captura o del paso anterior, la columna de función aporta el contexto.

| Función | Prompt utilizado / extracto | Adaptación y validación reportada |
|---|---|---|
| Inicio del módulo | `bueno yo me encargo de red de servidores y diagnostico, ahora podemos empezar con esa parte` | Se adoptó un grafo no dirigido con listas paralelas y conexiones por índices. |
| Manejo de errores | `sigamo ese codigo pero cn esta funcion` | Se aportó una versión de `agregar_servidor` con `raise ValueError` para nombres duplicados. |
| Valores de retorno | `es igual al return tur?` | Se comparó `return True` con devolver un mensaje; las operaciones exitosas de modificación devuelven texto. |
| Indentación | `asi?` | Se revisaron capturas y se movieron los `append` fuera del ciclo de detección de duplicados. |
| Pruebas iniciales | `como pruebo` | Se incorporó un script con aserciones para conexiones bidireccionales y entradas inválidas. Se reportó su ejecución satisfactoria. |
| Ejecución | `cual carpeta me pongo para probar` | Se ejecutó desde la raíz y se usó la ruta explícita del intérprete de Python instalado. |
| Organización de pruebas | `meti la prueba a una carpeta y al compilar me sale eso?` | Se creó el paquete `tests` y se cambió la ejecución a `python -m tests.prueba_red` para resolver imports. |
| Eliminación de conexiones | `listo` / `todo bien` | Tras incorporar el método y sus pruebas, se reportó que funcionaron; se comprueban ambos extremos y la conservación de otros enlaces. |
| Diagnóstico BFS | `ya hice el diagnostacar red` / `sip` | Se incorporó el diagnóstico y se confirmó el resultado de las pruebas de aislamiento, conectividad, componentes separados y ciclos. |
| Organización de menús | `tu me recomiendas meter todos los menus en un archivo o un archivo por menu y una carpeta de menus?` | Se propuso separar por área funcional; la carpeta local existe, pero la migración está pendiente. |
| Cachés de Python | `Me podrias decir como ignorar los cahes` | Se agregó `.gitignore` y se verificó con `git status --ignored` que `__pycache__` quedara ignorado. |
| Documentación | `quiero que cambies el readme nuevo usando siempre este tipo obviamente con los datos nuevos` | Se solicitó adaptar el formato del proyecto anterior al código, prompts e historial verificables del proyecto actual. |

</details>

### Módulo Enrutamiento - Responsable por confirmar

Pendiente de implementación: Dijkstra, reconstrucción de la ruta, costo total y
simulación del envío. Deberá consultar las adyacencias de `GrafoRed` y manejar
destinos no alcanzables. Aún no hay un archivo de enrutamiento en la copia revisada.

### Módulo Auditoría y Menús - Responsable por confirmar

Pendiente de implementación: registro con fecha y hora en `network_audit_log.txt`,
consulta del registro e integración de las operaciones de red en los menús.
El menú deberá capturar los `ValueError` y utilizar una instancia compartida de
la red. Cada integrante deberá completar sus propios prompts y validaciones.

### Historial de integraciones observable

| Fecha | Evidencia Git | Operación documentada |
|---|---|---|
| 2026-09-23 | `d2c110f` | Merge del pull request #1 desde `IsmaAlfaro/Alannah`. |
| 2026-09-24 | `280caba` | Merge del pull request #2 desde `IsmaAlfaro/Alannah`. |
| 2026-09-24 | `c778a84` | Merge del pull request #3 desde `IsmaAlfaro/Alannah`. |

Estas entradas proceden del historial local de commits. No constituyen un
registro de todas las operaciones de fetch, push o sincronización remota.

### Registro de commits analizados

| Fecha | Commit | Autor | Mensaje o avance agrupado |
|---|---|---|---|
| 2026-09-14 | `21ed4d4` | Ismael Alfaro Benavides | Initial commit. |
| 2026-09-23 | `4d47cb6`, `c585217`, `249ce92` | alannah-byte | Estructura inicial, hijos, búsqueda y visualización. |
| 2026-09-23 | `d2c110f` | alannah-byte | Merge pull request #1. |
| 2026-09-24 | `c29ab3c`, `53567b2`, `2c70199`, `c7c14de`, `2eefe20`, `c8a8fce` | alannah-byte | Servidor, eliminación, creación y manejo por rutas. |
| 2026-09-24 | `7969ca7`, `423778a`, `1b59e7d`, `7e33983` | alannah-byte | Prompts, tabla hash, importación y main. |
| 2026-09-24 | `280caba` | alannah-byte | Merge pull request #2. |
| 2026-09-24 | `c778a84` | Ismael Alfaro Benavides | Merge pull request #3. |
| 2026-09-25 | `b32f689` | IsmaAlfaro | Ignorar archivos de caché de Python. |
| 2026-10-02 | `f43be98` | IsmaAlfaro | creacion del grafo red, la carpeta de pruebas (Test). |

## Complejidad de las estructuras y algoritmos actuales

### Árbol de directorios

Sea `N` el número de nodos, `H` la altura del árbol y `S` el tamaño del subárbol
que se vacía.

| Operación | Complejidad | Explicación |
|---|---|---|
| Buscar por nombre | O(N) en el peor caso | Puede visitar todos los nodos. La pila recursiva ocupa O(H). |
| Buscar por ruta | O(suma de hijos examinados por nivel) | Cada componente de la ruta se busca secuencialmente entre los hijos del nodo actual. |
| Vaciar un subárbol | O(S) | Visita sus descendientes y limpia las referencias de las listas de hijos; la pila recursiva depende de su altura. |

En Python la memoria se recupera cuando los objetos dejan de estar referenciados;
vaciar las listas elimina los enlaces del árbol, pero otras referencias externas
pueden mantener un objeto vivo.

### Tabla hash

La función implementada es `suma(ord(caracter)) % tamaño`. Sea `L` la longitud del
usuario, `U` la cantidad de usuarios y `k` la cantidad de entradas en su bucket.

| Operación | Complejidad | Explicación |
|---|---|---|
| Calcular hash | O(L) | Recorre los caracteres del nombre de usuario. |
| Registrar o autenticar | O(L + k), considerando comparaciones de longitud acotada | Calcula el índice y recorre únicamente la lista de ese bucket. Las comparaciones de cadenas también dependen de su longitud. |
| Peor caso por colisiones | O(U) respecto a la cantidad de usuarios, con cadenas acotadas | Todos pueden quedar en un mismo bucket. |

El acceso promedio cercano a O(1), para claves de longitud acotada, depende de una
buena distribución y de controlar el factor de carga. La implementación actual
tiene 10 buckets por defecto y no redimensiona automáticamente.

### Grafo y diagnóstico BFS

Sea `V` el número de servidores, `E` el número de conexiones no dirigidas y
`grado(u)` la cantidad de vecinos del servidor `u`.

| Operación | Complejidad | Explicación |
|---|---|---|
| Almacenar el grafo | O(V + E) en memoria | Cada conexión se almacena en ambos extremos. |
| Buscar o agregar servidor | O(V) | La búsqueda por nombre y la comprobación de duplicados son secuenciales. |
| Agregar conexión | O(V + grado(origen)) | Busca ambos índices y comprueba duplicados en los vecinos del origen. |
| Eliminar conexión | O(V + grado(origen) + grado(destino)) | Localiza los servidores y elimina las entradas en ambos extremos. |
| Diagnosticar con BFS | O(V + E) en el peor caso | Visita los vértices alcanzables, recorre sus adyacencias y revisa todos los servidores para elaborar el diagnóstico. |
| Memoria auxiliar del diagnóstico | O(V) | Visitados, cola, recorrido y listas del resultado. |

Un servidor aislado tiene grado cero. Un servidor no alcanzable pertenece a una
zona que no puede recorrerse desde el origen, aunque tenga conexiones con otros
servidores. BFS diagnostica conectividad; no calcula la ruta de menor latencia.
