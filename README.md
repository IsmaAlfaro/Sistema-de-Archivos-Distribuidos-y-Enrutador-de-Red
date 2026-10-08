# Sistema de Archivos Distribuido y Enrutador de Red

Proyecto de Investigación Aplicada #2 del curso EIF207 - Estructuras de Datos.
Universidad Nacional, Sección Regional Central Occidente.

Simulación por consola del núcleo lógico de un sistema operativo de red. Cada
servidor administra su propio árbol de archivos y sus credenciales de acceso.
La red representa conexiones entre servidores con latencias en milisegundos.
El objetivo completo incluye diagnóstico de conectividad, enrutamiento de
paquetes por el camino más corto, auditoría de las operaciones y validación
mediante pruebas automatizadas.

## Funcionalidades

### Implementadas

- Selección entre tres servidores desde el programa principal.
- Registro e inicio de sesión con credenciales locales por servidor.
- Creación de archivos y carpetas bajo una ruta existente.
- Búsqueda recursiva por nombre y navegación por rutas.
- Visualización del árbol de directorios con indentación.
- Eliminación recursiva del contenido de carpetas.
- Registro de servidores en un grafo, evitando nombres duplicados.
- Creación y eliminación de conexiones bidireccionales con latencia positiva.
- Diagnóstico BFS: recorrido, servidores no alcanzables, servidores aislados
  y estado de conectividad.
- Enrutamiento de menor costo con Dijkstra sobre el grafo de red.
- Simulación del envío de paquetes mostrando cada salto y la latencia total.
- Registro automático de eventos en `network_audit_log.txt` con fecha y hora.
- Consulta del historial de auditoría desde el menú principal y el menú de red.
- Menú de administración de red integrado en `main.py`, con selección mediante
  `match/case` y manejo de errores.
- Pruebas de conexiones, eliminación, diagnóstico, enrutamiento y auditoría.

El menú principal permite acceder a los servidores o administrar la red.
`main()` crea una única instancia de `GrafoRed` con los mismos objetos `Servidor`
utilizados para autenticación y archivos, y la pasa a `menu_red(red)`.
Los usuarios, archivos y conexiones se mantienen en memoria durante la ejecución;
la red no se vuelve a crear al abrir el submenú.

### Pendientes

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
- **Dijkstra:** cálculo de la ruta de menor latencia entre origen y destino, reconstrucción del camino y cálculo del costo total. El módulo `enrutamiento.py` usa índices del grafo y evita la manipulación directa de `GrafoRed`.
- **Auditoría:** `auditoria.py` registra eventos con fecha y hora en `network_audit_log.txt` y ofrece lectura total o filtrada por fecha desde el menú.
- **Excepciones:** las operaciones inválidas de la red lanzan `ValueError`; `menu_red` las captura para informar al usuario. También maneja errores al convertir la latencia a número.
- **Selección con `match/case`:** el menú de red ofrece agregar conexiones, eliminarlas, diagnosticar, simular tránsito y volver al menú principal.

## Ejecución y pruebas

Requiere Python 3.10 o superior por el uso de `match/case` en el menú de red.
Los módulos actuales no necesitan paquetes externos.
Ejecutar desde la raíz del repositorio:

```bash
python main.py
```

Ejecutar las pruebas del grafo y diagnóstico:

```bash
python -m tests.prueba_red
```

Ejecutar las pruebas de enrutamiento cuando estén disponibles en el paquete:

```bash
python -m tests.prueba_enrutamiento
```

Las pruebas actuales son un script con `assert`, no una suite de `unittest`.
Se ejecutan como módulo para que los imports encuentren `servidor.py`,
`grafo_red.py` y `enrutamiento.py` desde la raíz. Deben ejecutarse sin la opción
`-O`, que desactiva las aserciones.

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
| Enrutamiento | Ruta directa y por varios saltos, menor latencia, sin ruta, origen = destino, servidor inexistente y latencias decimales. |

Ismael reportó la ejecución satisfactoria de estas pruebas durante el desarrollo
guiado. Esto verifica los casos anteriores; la integración completa del programa
sigue validándose en la ejecución interactiva del menú.

### Validación manual del menú de red

Ismael ejecutó `main.py` y compartió capturas de las siguientes comprobaciones:

| Acción desde el menú | Resultado observado |
|---|---|
| Conectar Servidor 1 con Servidor 2, con latencia 10 ms. | Mensaje de conexión agregada con latencia `10.0`. |
| Conectar Servidor 2 con Servidor 3, con latencia 15 ms. | Mensaje de conexión agregada con latencia `15.0`. |
| Diagnosticar desde Servidor 1 con ambos enlaces. | Recorrido `Servidor 1 -> Servidor 2 -> Servidor 3`, red conectada y ningún servidor aislado o no alcanzable. |
| Diagnosticar después de eliminar el enlace entre Servidor 2 y Servidor 3. | Recorrido `Servidor 1 -> Servidor 2`, red desconectada y Servidor 3 identificado como aislado y no alcanzable. |
| Simular envío de paquete de Servidor 1 a Servidor 3. | Se elige la ruta de menor latencia y se muestran los saltos con el costo total. |

El orden mostrado es el recorrido de visita BFS, no una ruta de envío de paquetes.
La comprobación manual de salir del submenú y volver a entrar conservando las
conexiones fue propuesta, pero todavía no se ha reportado su resultado.

## Estructura de módulos

```text
main.py              Menú principal, autenticación, archivos, red y auditoría.
servidor.py          Árbol y tabla de usuarios locales de cada servidor.
nodo_archivo.py      Nodos, búsqueda, visualización y eliminación recursiva.
tabla_hash.py        Función hash, encadenamiento, registro y autenticación.
grafo_red.py         Servidores, conexiones ponderadas y diagnóstico BFS.
enrutamiento.py      Ruta de menor latencia con Dijkstra y simulación de paquetes.
auditoria.py         Registro y consulta de eventos del sistema en network_audit_log.txt.
tests/
    __init__.py      Identifica el paquete de pruebas.
    prueba_red.py    Pruebas de conexiones, eliminación y diagnóstico.
    prueba_enrutamiento.py  Pruebas de Dijkstra y envío de paquetes.
.gitignore           Exclusión de cachés de Python.
README.md            Documentación y bitácora de desarrollo e IA.
network_audit_log.txt Registro histórico generado por la auditoría.
```

La copia local contiene una carpeta `menus/` vacía, reservada para la organización
de los menús. Por ahora las funciones de menú siguen en `main.py`; Git no registra
carpetas vacías.

## Bitácora de desarrollo

Esta bitácora se elaboró a partir del código y del historial Git local disponible
el 3 de octubre de 2026, junto con la conversación de desarrollo de Ismael.
Las responsabilidades confirmadas son: Alannah desarrolló la base de archivos,
servidores, autenticación y menús iniciales; Ismael trabajó la red, su diagnóstico
y la conexión del menú de red con el menú principal. El trabajo de enrutamiento y
auditoría quedó integrado como parte de la evolución final del proyecto.

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

### Módulo Red de Servidores y Diagnóstico - Ismael

| Fecha | Evidencia Git | Avance documentado |
|---|---|---|
| 2026-09-25 | `b32f689` | Incorporación de `.gitignore` para los cachés de Python. |
| 2026-10-02 | `f43be98` | Incorporación de `grafo_red.py`, paquete `tests` y pruebas de red. |
| 2026-10-02 | `cab1d01` | Organización del README con funcionalidades, bitácora, prompts y complejidades. |
| 2026-10-03 | `4290ba8` | Integración de `menu_red` con `match/case` en `main.py` y acceso desde el menú principal. |
| 2026-10-03 | `2fd3211` | Actualización del README con la integración del menú de red y las comprobaciones manuales. |

Estado actual: `GrafoRed` registra servidores y almacena conexiones bidireccionales
con latencias positivas. Permite agregar y eliminar enlaces y diagnosticar la red
mediante BFS. Devuelve los nombres visitados, los no alcanzables, los aislados y
un booleano que indica si toda la red es alcanzable desde el origen.

### Módulo Enrutamiento - Carlos Víquez

Estado actual: `enrutamiento.py` calcula la ruta de menor latencia con Dijkstra
implementado manualmente sobre las listas `servidores` y `adyacencias` de
`GrafoRed`, sin modificar ese módulo. Funciones: `buscar_minimo_no_visitado`,
`dijkstra`, `reconstruir_ruta`, `calcular_ruta` y `simular_envio_paquete`.
Maneja origen o destino inexistentes (`ValueError`), origen igual al destino
y destino sin ruta. El menú de red tiene la opción 4 para simular el envío.

Pruebas: `python -m tests.prueba_enrutamiento` (ruta directa, varios saltos,
elección de menor latencia, sin ruta, origen = destino, servidor inexistente,
red vacía y latencias decimales).

Complejidad: Dijkstra con búsqueda lineal del mínimo es O(V²) en tiempo y O(V)
en memoria auxiliar.

### Módulo Auditoría y Menús - Responsable por confirmar

Estado actual: `auditoria.py` registra cada acción con fecha y hora en
`network_audit_log.txt` y permite consultarlo desde el menú principal.
Los eventos incluyen los orígenes de las operaciones, la acción ejecutada y la
marca temporal exacta. El módulo se activa sólo cuando el sistema está en uso
regular y se puede desactivar para pruebas unitarias.

El menú de conexiones y diagnóstico ya está integrado por Ismael en `main.py`,
captura `ValueError` y utiliza una instancia compartida de la red. La
separación en carpetas y la finalización de menús se realizará posteriormente.

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
| 2026-10-02 | `cab1d01` | IsmaAlfaro | readme limpio |
| 2026-10-03 | `4290ba8` | IsmaAlfaro | integracion de menu red a el menu en main |
| 2026-10-03 | `2fd3211` | IsmaAlfaro | Actualizar README con integracion del menu de red |

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
| Registrar o autenticar | O(L + k), considerando comparaciones de longitud acotada | Calcula el índice y recorre únicamente la lista de ese bucket. Las comparaciones de cadenas también dependen de la longitud. |
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

### Enrutamiento por costo mínimo

Dijkstra se ejecuta sobre el grafo no dirigido con pesos de latencia.
Cada conexión tiene un costo positivo y el algoritmo mantiene las distancias
mínimas conocidas hasta cada vértice.

| Operación | Complejidad | Explicación |
|---|---|---|
| Dijkstra | O(V²) con la implementación actual | Se busca el mínimo no visitado en cada iteración. |
| Reconstrucción de la ruta | O(V) | Retrocede desde el destino usando los predecesores. |
| Memoria auxiliar | O(V) | Distancias, visitados y predecesores. |

El módulo `enrutamiento.py` devuelve la ruta exacta y la latencia total para
poder simular el tránsito por el camino óptimo.
