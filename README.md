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
- Dijkstra manual, reconstrucción de la ruta y simulación del envío mostrando saltos y latencia total.
- Auditoría automática de archivos, conexiones, cálculo de rutas, registro de usuarios y accesos exitosos o fallidos.
- Consulta del historial completo, desde una fecha o para una fecha específica.
- Menú de administración de red integrado en `main.py`, con selección mediante `match/case` y manejo de errores.
- Pruebas de conexiones, eliminación y diagnóstico de red con `assert`.

El menú principal permite acceder a los servidores, administrar la red o consultar auditoría.
`main()` crea una única instancia de `GrafoRed` con los mismos objetos `Servidor`
utilizados para autenticación y archivos, y la pasa a `menuRed(red)`.
Los usuarios, archivos y conexiones se mantienen en memoria durante la ejecución;
la red no se vuelve a crear al abrir el submenú. La auditoría se activa después de
crear los servidores iniciales; sus registros se conservan en `network_audit_log.txt`.

### Pendientes

- Corregir la eliminación por ruta: seleccionar al hijo directo de la carpeta padre antes de borrar su subárbol. Actualmente la búsqueda puede eliminar un descendiente de otra ruta con el mismo nombre.
- Proteger el formato de auditoría frente a separadores dentro de los datos y registros incompletos o con fechas inválidas.
- Manejar fallos de escritura de auditoría desde archivos, autenticación y red.
- Exigir latencias finitas y positivas; actualmente se aceptan `nan` e `inf`.
- Validar nombres de archivos y carpetas, credenciales vacías y entradas del selector de servidores.
- Optimizar la escritura del log para evitar leer todo el historial en cada evento.
- Revisar la distribución y el crecimiento de la tabla hash para limitar las colisiones.
- Ampliar pruebas de árboles, autenticación, auditoría y casos límite.
- Completar las bitácoras de IA con los aportes de cada integrante.
- Organizar los menús por módulos después de estabilizar las funciones.
- Incorporar y documentar las ampliaciones semanales que publique el docente.

## Estructuras y técnicas implementadas

- **Árbol general:** cada `NodoArchivo` contiene nombre, tipo y lista de hijos. La raíz de cada servidor es `/` y los archivos se mantienen como hojas mediante la operación de agregar hijos.
- **Recursividad:** búsqueda por nombre, visualización y vaciado de subárboles desde los descendientes.
- **Tabla hash manual:** arreglo de listas, función propia basada en la suma de `ord()` y módulo por el tamaño de la tabla. Las colisiones se resuelven mediante encadenamiento.
- **Grafo ponderado no dirigido:** listas paralelas de servidores y adyacencias; cada conexión almacena `(indice_vecino, latencia)` en ambos extremos.
- **BFS:** cola implementada con una lista y un índice de lectura, más una lista de visitados para evitar repeticiones.
- **Excepciones:** las operaciones inválidas de la red lanzan `ValueError`; `menuRed` las captura. El manejo de errores de escritura de auditoría sigue pendiente.
- **Selección con `match/case`:** el menú de red ofrece agregar conexiones, eliminarlas, diagnosticar, simular envíos y volver al menú principal.
- **Dijkstra:** búsqueda lineal del mínimo no visitado, relajación de aristas y reconstrucción mediante predecesores.
- **Auditoría:** append a un archivo UTF-8, fecha y hora mediante `datetime`, lectura y filtros por fecha.

## Ejecución y pruebas

Requiere Python 3.10 o superior por el uso de `match/case` en el menú de red.
Los módulos actuales no necesitan paquetes externos.
Ejecutar desde la raíz del repositorio:

```bash
python main.py
```

Ejecutar las pruebas de red:

```bash
python -m tests.prueba_red
```

Ejecutar las pruebas de enrutamiento:

```bash
python practica_grafo.py
```

Las pruebas actuales son scripts con `assert`, no una suite de `unittest`.
La prueba de red se ejecuta como módulo para resolver imports desde la raíz.
Deben ejecutarse sin la opción `-O`, que desactiva las aserciones. En procesos
nuevos, la auditoría está desactivada por defecto para estas pruebas; `main()`
la activa para el uso interactivo.

En el entorno de desarrollo de Ismael, si el comando `python` no está disponible
en PowerShell, se utiliza la ruta del intérprete instalado:

```powershell
& "C:\msys64\ucrt64\bin\python.exe" main.py
& "C:\msys64\ucrt64\bin\python.exe" -m tests.prueba_red
& "C:\msys64\ucrt64\bin\python.exe" practica_grafo.py
```

El último mensaje esperado de las pruebas es:

```text
Pruebas de diagnóstico completadas correctamente.
Pruebas de enrutamiento completadas correctamente.
```

### Cobertura actual de las pruebas de red

| Área | Casos comprobados por el script |
|---|---|
| Conexiones | Almacenamiento en ambos sentidos, duplicados directos e inversos, servidor inexistente, conexión consigo mismo y latencias negativas o cero. |
| Eliminación | Borrado en ambos sentidos, conservación de servidores y otras conexiones, enlace inexistente y servidor inexistente. |
| Diagnóstico | Servidor aislado, reconexión de toda la red, componentes separados sin nodos aislados, ciclos sin visitas repetidas y origen inexistente. |

Ismael reportó la ejecución satisfactoria de las pruebas durante el desarrollo
guiado. En la revisión del 7 de octubre de 2026, la IA ejecutó ambos scripts con
`-B` sobre la versión `888f9a8`: ambos pasaron. `practica_grafo.py` verifica rutas
directas e indirectas, menor costo, rutas inversas, destinos desconectados, origen
igual al destino, servidores inexistentes, red vacía, predecesores, latencias
decimales y conservación de las adyacencias.

Las pruebas adicionales de revisión se ejecutaron en memoria, usando objetos
simulados para la lectura del log y los errores de E/S. Confirmaron los fallos
descritos en el plan de correcciones. No se agregaron como archivos de pruebas
ni se escribió en el log del proyecto. Falta convertir esos casos en pruebas
de regresión y verificar la integración completa con auditoría activada.

### Validación manual del menú de red

Ismael ejecutó `main.py` y compartió capturas de las siguientes comprobaciones:

| Acción desde el menú | Resultado observado |
|---|---|
| Conectar Servidor 1 con Servidor 2, con latencia 10 ms. | Mensaje de conexión agregada con latencia `10.0`. |
| Conectar Servidor 2 con Servidor 3, con latencia 15 ms. | Mensaje de conexión agregada con latencia `15.0`. |
| Diagnosticar desde Servidor 1 con ambos enlaces. | Recorrido `Servidor 1 -> Servidor 2 -> Servidor 3`, red conectada y ningún servidor aislado o no alcanzable. |
| Diagnosticar después de eliminar el enlace entre Servidor 2 y Servidor 3. | Recorrido `Servidor 1 -> Servidor 2`, red desconectada y Servidor 3 identificado como aislado y no alcanzable. |

El orden mostrado es el recorrido de visita BFS, no una ruta de envío de paquetes.
La comprobación manual de salir del submenú y volver a entrar conservando las
conexiones fue propuesta, pero todavía no se ha reportado su resultado.

## Estructura de módulos

```text
main.py              Menús principal, autenticación, archivos, red y auditoría.
servidor.py          Árbol y tabla de usuarios locales de cada servidor.
nodo_archivo.py      Nodos, búsqueda, visualización y eliminación recursiva.
tabla_hash.py        Función hash, encadenamiento, registro y autenticación.
grafo_red.py         Servidores, conexiones ponderadas y diagnóstico BFS.
enrutamiento.py      Dijkstra, reconstrucción y simulación de envío.
auditoria.py         Escritura del log, lectura y filtros por fecha.
grafo.py             Representación alternativa mediante diccionarios, no usada por main.
practica_grafo.py    Pruebas de enrutamiento con assert.
tests/
    __init__.py      Identifica el paquete de pruebas.
    prueba_red.py    Pruebas de conexiones, eliminación y diagnóstico.
.gitignore           Exclusión de cachés de Python.
README.md            Documentación y bitácora de desarrollo e IA.
network_audit_log.txt Archivo generado al registrar eventos con auditoría activa.
```

La copia local contiene una carpeta `menus/` vacía, reservada para la organización
de los menús. Por ahora las funciones de menú siguen en `main.py`; Git no registra
carpetas vacías.

## Bitácora de desarrollo

Esta bitácora se actualizó el 7 de octubre de 2026 a partir del código y del
historial local hasta `888f9a8`, junto con la conversación de desarrollo de Ismael.
Las responsabilidades confirmadas son: Alannah desarrolló la base de archivos,
servidores, autenticación y menús iniciales; Ismael trabajó la red, su diagnóstico
y la conexión del menú de red con el menú principal.
Carlos Víquez desarrolló enrutamiento. Los commits de `seguraAriasAndres`
documentan el trabajo de Andrés en auditoría y su integración con los módulos.

### Módulos de Archivos, Servidores y Autenticación - Alannah

| Fecha | Evidencia Git | Avance documentado |
|---|---|---|
| 2026-09-23 | `4d47cb6`, `c585217`, `249ce92` | Estructura inicial, incorporación de hijos, búsqueda y visualización del árbol. |
| 2026-09-24 | `c29ab3c`, `53567b2`, `2c70199` | Eliminación de nodos, clase `Servidor` y operaciones básicas de creación. |
| 2026-09-24 | `c7c14de`, `2eefe20`, `c8a8fce` | Búsqueda por ruta, manejo de nodos mediante rutas y mejora de la creación. |
| 2026-09-24 | `7969ca7`, `423778a`, `1b59e7d`, `7e33983` | Registro de prompts, tabla hash, importación en servidor y programa principal. |
| 2026-09-28 | `2aa4b35`, `5d4caea`, `8f4e3ca` | Grafo alternativo, registro de prompts y actualización del programa principal según los mensajes de commit. |

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
| 2026-10-02 | `cab1d01` | Organización del README con funcionalidades, bitácora, prompts y complejidades. |
| 2026-10-03 | `4290ba8` | Integración de `menu_red` con `match/case` en `main.py` y acceso desde el menú principal. |
| 2026-10-03 | `2fd3211` | Actualización del README con la integración del menú de red y las comprobaciones manuales. |
| 2026-10-03 | `6a92be2` | Incorporación de commits recientes a la bitácora del README. |

Estado actual: `GrafoRed` registra servidores y almacena conexiones bidireccionales
con latencias positivas. Permite agregar y eliminar enlaces y diagnosticar la red
mediante BFS. Devuelve los nombres visitados, los no alcanzables, los aislados y
un booleano que indica si toda la red es alcanzable desde el origen.

La integración inicial en `main.py` agregó `menu_red(red)` con `match/case` y la
opción «Administrar red» en el menú principal. El submenú solicita nombres,
convierte la latencia con `float()`, captura `ValueError` y presenta el resultado
del diagnóstico. Este avance está registrado en el commit `4290ba8` y se
complementa con las capturas de las pruebas manuales compartidas por Ismael.
En la versión integrada actual, la función se llama `menuRed` e incluye el envío
de paquetes incorporado por Carlos; Andrés añadió pausas y limpieza de consola.

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
| Integración con main | `lo que vamos a hacer es hacer todo y depues sepepararlo a carpetas, podrias mostrarme no cambiando codigo internamente que haria yo para conectarlo a la funcionalidad del main` (espaciado normalizado) | Se incorporó manualmente el menú en `main.py`, creando la red una sola vez con los servidores existentes. La separación en carpetas se dejó para después. |
| Menú con match/case | `podrias hacer el menu de red con switch, quiero ver como se implementa en python` | Se adaptó el menú a `match/case`; se explicó que los casos no necesitan `break` y que el de la opción 0 termina el `while`. |
| Prueba del menú | `y para provarlo` | Las capturas posteriores muestran creación de dos conexiones, diagnóstico de red conectada y diagnóstico con Servidor 3 aislado tras eliminar un enlace. |
| Cachés de Python | `Me podrias decir como ignorar los cahes` | Se agregó `.gitignore` y se verificó con `git status --ignored` que `__pycache__` quedara ignorado. |
| Documentación | `quiero que cambies el readme nuevo usando siempre este tipo obviamente con los datos nuevos` | Se solicitó adaptar el formato del proyecto anterior al código, prompts e historial verificables del proyecto actual. |
| Revisión integral | `ahora si observa todo el proyecto y dime que errores hay, o optimzaciones o cambios para hacer` | La IA revisó los módulos, ejecutó las pruebas existentes y reprodujo errores en memoria. Ismael solicitó correcciones guiadas; todavía no se documentan como resueltas. |
| Plan de mejoras | `okey actualiza el readme con todo lo nuevo y despues me vas guiando para ir poco a poco con todo lo que hay que arreglar, optimizar o mejorar` | Se actualizó la documentación y se ordenaron las correcciones para aplicación manual, empezando por la eliminación por ruta. |

</details>

### Módulo Enrutamiento - Carlos Víquez

| Fecha | Evidencia Git | Avance documentado |
|---|---|---|
| 2026-10-03 | `7b2b2e9` | Implementación de enrutamiento y pruebas. |
| 2026-10-03 | `d2a7a6e` | Integración del envío de paquetes en el menú de red. |

Estado actual: `enrutamiento.py` calcula la ruta de menor latencia con Dijkstra
implementado manualmente sobre las listas `servidores` y `adyacencias` de
`GrafoRed`, sin modificar ese módulo. Funciones: `buscar_minimo_no_visitado`,
`dijkstra`, `reconstruir_ruta`, `calcular_ruta` y `simular_envio_paquete`.
Maneja origen o destino inexistentes (`ValueError`), origen igual al destino
y destino sin ruta. El menú de red tiene la opción 4 para simular el envío.

Pruebas: `python practica_grafo.py` (ruta directa, varios saltos,
elección de menor latencia, sin ruta, origen = destino, servidor inexistente,
red vacía y latencias decimales).

Complejidad: Dijkstra con búsqueda lineal del mínimo es O(V²) en tiempo y O(V)
en memoria auxiliar.

Validación manual:
| Acción desde el menú | Resultado observado |
|---|---|
| Conectar Servidor 1 con Servidor 2 (10 ms), Servidor 2 con Servidor 3 (15 ms) y Servidor 1 con Servidor 3 (30 ms). | Mensajes de conexión agregada. |
| Simular envío de Servidor 1 a Servidor 3. | Eligió el desvío, no la conexión directa de 30 ms: `Servidor 1 -> Servidor 2 -> Servidor 3`, con latencia total de `25.0 ms`. |
| Diagnosticar la red desde Servidor 1 tras eliminar enlaces. | Recorrido `Servidor 1 -> Servidor 2`, red no conectada y Servidor 3 aislado y no alcanzable. El diagnóstico BFS siguió funcionando con normalidad. |

Pendiente documental: Carlos debe aportar sus prompts utilizados y explicar sus
adaptaciones. Las comprobaciones de esta sección proceden del README previo y
del script existente, sin reconstruir conversaciones que no fueron compartidas.

### Módulo Auditoría y Menús - Andrés

| Fecha | Evidencia Git | Avance documentado |
|---|---|---|
| 2026-10-04 | `5c5ddc8`, `68cd354`, `49fd4f7`, `8f4f1c6`, `2b33a6f` | Creación y ajustes del módulo de auditoría. |
| 2026-10-04 | `d10e57b`, `1c5e75c`, `395b044`, `6498d88`, `c2b9979`, `9f8204d` | Integración de eventos en enrutamiento, grafo y servidor. |
| 2026-10-05 | `f7a1e2b` | Actualización de auditoría. |
| 2026-10-06 | `ffcb377`, `d712c5a` | Auditoría de registro y autenticación con identificación del servidor. |
| 2026-10-06 | `67fb847`, `e31456d`, `04fb76c` | Actualización de auditoría y menús; la versión integrada incluye filtros por fecha y activación del registro. |

Estado actual: `auditoria.py` agrega fecha, hora, origen y acción al archivo
`network_audit_log.txt`. `menuAuditoria()` permite consultar todo el historial,
desde una fecha o una fecha específica. `main()` activa la auditoría después
de inicializar los servidores. `TablaHash` registra altas y accesos exitosos o
fallidos; servidor, grafo y enrutamiento registran sus operaciones integradas.

Pendientes: robustecer el formato del registro, manejar errores de escritura en
los menús operativos y optimizar el append. Andrés debe completar sus prompts,
adaptaciones y validaciones reportadas. La separación de menús en carpetas sigue
planificada para una etapa posterior.

### Historial de integraciones observable

| Fecha | Evidencia Git | Operación documentada |
|---|---|---|
| 2026-09-23 | `d2c110f` | Merge del pull request #1 desde `IsmaAlfaro/Alannah`. |
| 2026-09-24 | `280caba` | Merge del pull request #2 desde `IsmaAlfaro/Alannah`. |
| 2026-09-24 | `c778a84` | Merge del pull request #3 desde `IsmaAlfaro/Alannah`. |
| 2026-09-28 | `803e085` | Merge del pull request #4 desde `IsmaAlfaro/Alannah`. |
| 2026-10-03 | `c98a289` | Integración de `main` en la rama Carlos. |
| 2026-10-03 | `10f6e2f`, `6cbf398`, `588c5d6` | Merges de los pull requests #5, #6 y #7 desde `IsmaAlfaro/Carlos`. |
| 2026-10-06 | `7cf499e`, `888f9a8` | Merges de los pull requests #8 y #9 desde `IsmaAlfaro/Andrés-Dev`. |

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
| 2026-09-28 | `2aa4b35`, `5d4caea`, `8f4e3ca`, `803e085` | alannah-byte | Grafo alternativo, prompts, main e integración por PR #4. |
| 2026-10-02 | `f43be98` | IsmaAlfaro | creacion del grafo red, la carpeta de pruebas (Test). |
| 2026-10-02 | `cab1d01` | IsmaAlfaro | readme limpio |
| 2026-10-03 | `4290ba8` | IsmaAlfaro | integracion de menu red a el menu en main |
| 2026-10-03 | `2fd3211` | IsmaAlfaro | Actualizar README con integracion del menu de red |
| 2026-10-03 | `6a92be2` | IsmaAlfaro | Completar commits recientes en la bitacora del README |
| 2026-10-03 | `c98a289`, `10f6e2f`, `7b2b2e9`, `6cbf398`, `d2a7a6e`, `588c5d6` | Carlos Viquez / CarlosViquez31 | Sincronización, enrutamiento, pruebas, menú e integraciones #5–#7. |
| 2026-10-04 | `5c5ddc8`, `68cd354`, `49fd4f7`, `d10e57b`, `395b044`, `c2b9979`, `8f4f1c6`, `9f8204d`, `6498d88`, `1c5e75c`, `2b33a6f` | seguraAriasAndres | Creación y ajustes de auditoría e integración con módulos. |
| 2026-10-05 | `f7a1e2b` | seguraAriasAndres | Update auditoria.py |
| 2026-10-06 | `7cf499e` | Ismael Alfaro Benavides | Merge pull request #8. |
| 2026-10-06 | `ffcb377`, `d712c5a`, `67fb847`, `e31456d`, `04fb76c`, `888f9a8` | seguraAriasAndres | Autenticación, servidor, auditoría, menús y merge del PR #9. |

## Plan de correcciones y mejoras

Estado de referencia: revisión del 7 de octubre de 2026 sobre `888f9a8`.
Los puntos siguientes están pendientes; su documentación no significa que hayan
sido corregidos. Cada cambio se aplicará manualmente y se verificará antes de
continuar con el siguiente.

| Orden | Área y cambio | Evidencia / comprobación prevista |
|---|---|---|
| 1 | Seleccionar el hijo directo al eliminar por ruta y conservar el vaciado recursivo. | Confirmado: eliminar `/Documentos/nota.txt` borra `/Documentos/Tareas/nota.txt` aunque la primera ruta no exista. Probar también nombres iguales en distintos niveles y cascada. |
| 2 | Proteger el formato del log y validar cada registro antes de interpretarlo. | Confirmado con lectura simulada: `~` dentro de una acción puede provocar `ValueError`; una línea incompleta produce `IndexError`. |
| 3 | Capturar errores de escritura de auditoría en autenticación, archivos y red. | Un `OSError` simulado escapa del menú de autenticación. Verificar que se informe al usuario y se mantenga un estado coherente. |
| 4 | Validar latencias finitas y positivas dentro de `GrafoRed`. | Confirmado: con `nan` o `inf`, BFS declara conectividad pero Dijkstra no encuentra ruta. |
| 5 | Validar nombres, credenciales y selección numérica. | Confirmado: se crean nodos con nombres vacíos, `/` y `a/b` que no se recuperan por su ruta; se autentican credenciales vacías; `²` provoca `ValueError` en el selector. |
| 6 | Añadir pruebas de regresión e integración para los casos anteriores y los filtros de auditoría. | Las pruebas existentes de red y enrutamiento pasan, pero no cubren esos errores. |
| 7 | Evitar leer todo el log para escribir un evento y controlar el crecimiento de la tabla hash. | `registrar_evento` lee el archivo completo; la tabla tiene 10 buckets y no redimensiona. |
| 8 | Unificar estilo, aclarar el grafo alternativo, reutilizar validación de fechas y separar menús. | Dos clases `GrafoRed` con interfaces distintas; mezcla de convenciones y validación de fechas duplicada. |

Otros ajustes de mantenimiento: hacer portable `limpiarConsola()` (actualmente
usa `cls`), reemplazar búsquedas dinámicas innecesarias de funciones de auditoría
por llamadas directas y mantener el README alineado con las correcciones.

La implementación lineal de Dijkstra es adecuada para la escala actual. Cambiarla
por una cola de prioridad es una optimización opcional para redes mayores.

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

### Dijkstra y auditoría

| Operación | Complejidad actual | Explicación |
|---|---|---|
| Dijkstra | O(V² + E), equivalente a O(V²) en este grafo simple | Busca linealmente el mínimo en cada iteración y recorre las adyacencias. Memoria auxiliar O(V). |
| Reconstruir ruta | O(V) en el peor caso | Sigue predecesores e invierte la lista. |
| Agregar evento al log | O(B) en tiempo y memoria | Actualmente lee todo el archivo, de B caracteres, antes de agregar la línea. |
| Leer y filtrar auditoría | O(B) para leer, más el procesamiento de registros | Carga el contenido y construye listas de registros y resultados filtrados. |

Los costos de escritura de auditoría se suman a los de las operaciones que la
invocan. En particular, la autenticación con auditoría activa no tiene un costo
total constante mientras cada evento lea el historial completo.
