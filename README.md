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
- Menú modular de auditoría integrado con opciones de lectura total, por fecha
  y desde una fecha en adelante.
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

### Validación manual del menú de red

Carlos ejecutó `main.py` y compartió capturas de las siguientes comprobaciones:

| Acción desde el menú | Resultado observado |
|---|---|
| Conectar Servidor 1 con Servidor 2, con latencia 10 ms. | Mensaje de conexión agregada con latencia `10.0`. |
| Conectar Servidor 2 con Servidor 3, con latencia 15 ms. | Mensaje de conexión agregada con latencia `15.0`. |
| Conectar Servidor 1 con Servidor 3, con latencia 30 ms. | Mensaje de conexión agregada con latencia `30.0`. |
| Diagnosticar desde Servidor 1 con ambos enlaces. | Recorrido `Servidor 1 -> Servidor 2 -> Servidor 3`, red conectada y ningún servidor aislado o no alcanzable. |
| Diagnosticar después de eliminar el enlace entre Servidor 2 y Servidor 3. | Recorrido `Servidor 1 -> Servidor 2`, red desconectada y Servidor 3 identificado como aislado y no alcanzable. |
| Simular envío de paquete de Servidor 1 a Servidor 3. | Se elige la ruta de menor latencia `Servidor 1 -> Servidor 2 -> Servidor 3` (25.0 ms) sobre la conexión directa de 30 ms. Se muestran los saltos con el costo total. |

El orden mostrado en el diagnóstico es el recorrido de visita BFS, no una ruta de envío de paquetes.

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
el 8 de octubre de 2026, junto con la conversación de desarrollo de cada integrante.
Las responsabilidades confirmadas son: Alannah desarrolló la base de archivos,
servidores, autenticación y menús iniciales; Ismael trabajó la red, su diagnóstico
y la conexión del menú de red con el menú principal; Carlos implementó el
enrutamiento por menor latencia con Dijkstra y su integración en el menú;
Andrés desarrolló el motor de auditoría, mejoró los menús y la captura de eventos
en todos los módulos.

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

| Fecha | Evidencia Git | Avance documentado |
|---|---|---|
| 2026-10-03 | `7b2b2e9` | Creación de `enrutamiento.py` con funciones de Dijkstra, reconstrucción de ruta y simulación de paquetes. |
| 2026-10-03 | `6cbf398` | Merge pull request #6: enrutamiento creado con tests. |
| 2026-10-03 | `d2a7a6e` | Cambios en `main.py` para integrar menú de enrutamiento. |
| 2026-10-03 | `588c5d6` | Merge pull request #7: cambios en main y readme. |

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

### Módulo Auditoría y Menús - Andrés Segura

| Fecha | Evidencia Git | Avance documentado |
|---|---|---|
| 2026-10-05 | `5c5ddc8` | Creación de `auditoria.py` con esqueleto inicial del módulo. |
| 2026-10-05 | `68cd354` | Decisión de mantener auditoría como módulo de funciones en lugar de clase. |
| 2026-10-05 | `49fd4f7` | Implementación de la lógica del método registrador de eventos. |
| 2026-10-05 | `2b33a6f` | Implementación de la lógica de lectura de datos desde el archivo de auditoría. |
| 2026-10-05 | `f7a1e2b` | Ajuste del formato de salida de `leer_registro`. |
| 2026-10-05 | `8f4f1c6` | Actualización del motor de auditoría con interruptor manual y método de configuración para pruebas. |
| 2026-10-05 | `9f8204d` | Implementación del registro de eventos en `servidor.py` para acciones de archivo y autenticación. |
| 2026-10-05 | `395b044` | Implementación del registro de eventos en `grafo_red.py` para conexiones y diagnóstico. |
| 2026-10-05 | `d10e57b` | Implementación del registro de eventos en `enrutamiento.py` para cálculos de ruta. |
| 2026-10-05 | `6498d88` | Actualización de la lógica de registro en `grafo_red.py`: validar antes de registrar, evitar contaminación por errores. |
| 2026-10-05 | `1c5e75c` | Actualización de la lógica de registro en `enrutamiento.py`: validar antes de registrar. |
| 2026-10-05 | `ffcb377` | Implementación del registro de eventos de registro e inicio de sesión en `tabla_hash.py`. |
| 2026-10-05 | `d712c5a` | Actualización del constructor de `Servidor` para que la tabla reciba el nombre del servidor (auditoría con contexto). |
| 2026-10-05 | `7cf499e` | Merge pull request #8: motor de auditoría implementado. |
| 2026-10-07 | `67fb847` | Actualización del sistema de lectura en `auditoria.py` con tres opciones: total, desde fecha, de una fecha específica. |
| 2026-10-07 | `e31456d` | Reformateo del menú en `main.py` a sistema modular con `menuAuditoria()` que adopta todas las implementaciones. |
| 2026-10-07 | `04fb76c` | Corrección de nombres de variables y funciones en `main.py` para usar camelCase consistente. |
| 2026-10-07 | `888f9a8` | Merge pull request #9: auditoría mejorada, menú integrado y registro en todas las operaciones. |

Estado actual: `auditoria.py` registra cada acción con fecha, hora y origen en
`network_audit_log.txt` usando `~` como separador. Permite consultar desde el
menú principal con tres opciones: lectura total del registro, lectura desde una
fecha en adelante, y lectura de un día específico. El módulo se activa durante
ejecución regular y puede desactivarse para pruebas unitarias. Todos los módulos
registran sus eventos: servidor (creación, eliminación, autenticación), grafo
(conexiones, diagnóstico), enrutamiento (cálculos de ruta).

### Validación y Mejoras Finales - Carlos Víquez

| Fecha | Evidencia Git | Avance documentado |
|---|---|---|
| 2026-10-08 | `43f7049` | Arreglos finales del código, validaciones y pruebas. |
| 2026-10-08 | `b6b317a` | Merge pull request #10: arreglos finales, validaciones y pruebas. |
| 2026-10-08 | `f84ccd8` | Actualización del README para documentar enrutamiento, auditoría y validaciones. |

### Historial de integraciones observable

| Fecha | Evidencia Git | Operación documentada |
|---|---|---|
| 2026-09-24 | `d2c110f` | Merge del pull request #1 desde `IsmaAlfaro/Alannah`. |
| 2026-09-25 | `280caba` | Merge del pull request #2 desde `IsmaAlfaro/Alannah`. |
| 2026-09-25 | `c778a84` | Merge del pull request #3 desde `IsmaAlfaro/Alannah`. |
| 2026-09-28 | `803e085` | Merge del pull request #4 desde `IsmaAlfaro/Alannah` (grafo e integración inicial). |
| 2026-10-03 | `10f6e2f` | Merge del pull request #5 desde `IsmaAlfaro/Carlos` (enrutamiento en desarrollo). |
| 2026-10-03 | `6cbf398` | Merge del pull request #6 desde `IsmaAlfaro/Carlos` (enrutamiento con tests). |
| 2026-10-03 | `588c5d6` | Merge del pull request #7 desde `IsmaAlfaro/Carlos` (integración en menú). |
| 2026-10-07 | `7cf499e` | Merge del pull request #8 desde `IsmaAlfaro/Andrés-Dev` (motor de auditoría). |
| 2026-10-07 | `888f9a8` | Merge del pull request #9 desde `IsmaAlfaro/Andrés-Dev` (auditoría y menús mejorados). |
| 2026-10-08 | `b6b317a` | Merge del pull request #10 desde `IsmaAlfaro/Carlos` (validaciones y pruebas finales). |

### Registro de commits analizados

| Fecha | Commit | Autor | Mensaje o avance agrupado |
|---|---|---|---|
| 2026-09-15 | `21ed4d4` | Ismael Alfaro Benavides | Initial commit. |
| 2026-09-24 | `4d47cb6`, `c585217`, `249ce92` | alannah-byte | Estructura inicial, hijos, búsqueda y visualización. |
| 2026-09-24 | `d2c110f` | alannah-byte | Merge pull request #1. |
| 2026-09-25 | `c29ab3c`, `53567b2`, `2c70199` | alannah-byte | Servidor, eliminación, creación y manejo por rutas. |
| 2026-09-25 | `c7c14de`, `2eefe20`, `c8a8fce` | alannah-byte | Búsqueda por ruta y mejora de creación. |
| 2026-09-25 | `7969ca7`, `423778a`, `1b59e7d`, `7e33983` | alannah-byte | Tabla hash, importación y programa principal. |
| 2026-09-25 | `280caba` | alannah-byte | Merge pull request #2. |
| 2026-09-25 | `c778a84` | Ismael Alfaro Benavides | Merge pull request #3. |
| 2026-09-25 | `b32f689` | IsmaAlfaro | Ignorar archivos de caché de Python. |
| 2026-09-28 | `2aa4b35`, `5d4caea`, `8f4e3ca` | alannah-byte | Grafo, prompts y actualización de main. |
| 2026-09-28 | `803e085` | alannah-byte | Merge pull request #4 (grafo). |
| 2026-10-02 | `f43be98` | IsmaAlfaro | Creación del grafo red y paquete tests. |
| 2026-10-02 | `cab1d01` | IsmaAlfaro | README limpio. |
| 2026-10-03 | `4290ba8` | IsmaAlfaro | Integración del menú de red. |
| 2026-10-03 | `2fd3211` | IsmaAlfaro | Actualización del README con menú de red. |
| 2026-10-03 | `7b2b2e9` | Carlos Viquez | Enrutamiento creado con tests. |
| 2026-10-03 | `6cbf398` | CarlosViquez31 | Merge pull request #6 (enrutamiento). |
| 2026-10-03 | `d2a7a6e` | Carlos Viquez | Cambios en main. |
| 2026-10-03 | `c98a289` | CarlosViquez31 | Merge branch 'main' into Carlos. |
| 2026-10-03 | `10f6e2f` | CarlosViquez31 | Merge pull request #5. |
| 2026-10-03 | `588c5d6` | CarlosViquez31 | Merge pull request #7 (cambios en main y readme). |
| 2026-10-03 | `6a92be2` | IsmaAlfaro | Completar commits recientes en la bitácora. |
| 2026-10-05 | `5c5ddc8` | seguraAriasAndres | Creación de auditoria.py. |
| 2026-10-05 | `68cd354` | seguraAriasAndres | Decisión: módulo de funciones vs clase. |
| 2026-10-05 | `49fd4f7` | seguraAriasAndres | Implementación del método registrador. |
| 2026-10-05 | `2b33a6f` | seguraAriasAndres | Implementación de la lógica de lectura. |
| 2026-10-05 | `f7a1e2b` | seguraAriasAndres | Ajuste del formato de salida. |
| 2026-10-05 | `8f4f1c6` | seguraAriasAndres | Motor de auditoría con interruptor manual. |
| 2026-10-05 | `9f8204d` | seguraAriasAndres | Registro en servidor.py. |
| 2026-10-05 | `395b044` | seguraAriasAndres | Registro en grafo_red.py. |
| 2026-10-05 | `d10e57b` | seguraAriasAndres | Registro en enrutamiento.py. |
| 2026-10-05 | `6498d88` | seguraAriasAndres | Actualización de lógica en grafo_red.py. |
| 2026-10-05 | `1c5e75c` | seguraAriasAndres | Actualización de lógica en enrutamiento.py. |
| 2026-10-05 | `ffcb377` | seguraAriasAndres | Registro en tabla_hash.py. |
| 2026-10-05 | `d712c5a` | seguraAriasAndres | Actualización del constructor de Servidor. |
| 2026-10-05 | `7cf499e` | IsmaAlfaro | Merge pull request #8 (auditoría). |
| 2026-10-06 | `f7a1e2b` | seguraAriasAndres | Ajuste de formato en auditoria.py. |
| 2026-10-07 | `67fb847` | seguraAriasAndres | Sistema de lectura mejorado (3 opciones). |
| 2026-10-07 | `e31456d` | seguraAriasAndres | Reformateo de menú a sistema modular. |
| 2026-10-07 | `04fb76c` | seguraAriasAndres | Corrección de nombres en camelCase. |
| 2026-10-07 | `888f9a8` | seguraAriasAndres | Merge pull request #9 (auditoría y menús). |
| 2026-10-08 | `43f7049` | Carlos Viquez | Arreglos finales, validaciones y pruebas. |
| 2026-10-08 | `b6b317a` | CarlosViquez31 | Merge pull request #10 (arreglos finales). |
| 2026-10-08 | `f84ccd8` | CarlosViquez31 | Actualización final del README. |

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

### Auditoría

La auditoría se implementa como un módulo que registra eventos secuencialmente
en un archivo con estructura separada por delimitadores.

| Operación | Complejidad | Explicación |
|---|---|---|
| Registrar evento | O(L + D) | Genera una cadena de longitud L y busca el final del archivo (seek). La escritura es O(1) amortizado. |
| Leer todos los registros | O(R) | Recorre todas las líneas del archivo, donde R es la cantidad de registros. |
| Filtrar por fecha | O(R) | Recorre todos los registros y compara la fecha de cada uno. |

El archivo de auditoría crece linealmente con el número de eventos. Cada evento
incluye origen, acción, fecha y hora.
