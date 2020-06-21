## Blind SQL Injection

### ¿Cómo correr el código?

Para correr código es necesario tener instalada la biblioteca `requests` con el comando `pip install requests`.

Luego basta utilizar un visualizador de código como Visual Studio Code con la versión 3.8 de Python para correr el código con el botón play, o desde un terminal `python blindsqlinjection.py`.

### ¿Cómo se llegó a la solución propuesta?

Para la solución propuesta incialmente se examinó que efectivamente se estaba presente ante una vulnerabilidad que permitiese realizar una inyección SQL, probando con entradas sencillas como `hola';` la que mostraba la consulta que realiza el sitio.

Luego se procedió a anular esta instrucción SQL mediante el siguiente string, dado que, entre perder todas las filas de la tabla y cambiar un valor, se prefirió la segunda opción : `RSA' WHERE nombre = 'platodeldia'; --`.

Finalmente completó la consulta con el ejemplo visto en la clase auxiliar 5, la que permite realizar búsqueda mediante timer's que se gatillan cuando la expresión propuesta contiene los caracteres de la fila a buscar, en este caso la fila con el atributo o columna nombre igual a `FLAG`.

Consulta obtenida : `RSA' WHERE nombre = 'platodeldia'; SELECT CASE when (SELECT 1 FROM configuraciones WHERE nombre ='FLAG' and valor like 'L%') = 1 then pg_sleep(10) else pg_sleep(0) end; --`

Con esta consulta fue posible automatizar el proceso de consultas utilizando el lenguaje de programación Python en su versión 3.8 en conjunto con la biblioteca requests mediante el siguiente algoritmo:

Precondiciones : Valor de la cookie

Generar una función que realice una request al servidor mediante POST

Generar un algoritmo que consulte hasta que largo(clave_hasta_ahora) == largo(clave_despues_de_probar_combinaciones)

Imprimir valor de la FLAG

Para más detalles del código ver parte siguiente de explicación de script y comentarios en el código realizado `blindsqlinjection.py`.

De forma alternativa se generó una consulta que permite mostrar el valor de la flag de forma inmediata : `hola' WHERE nombre= 'plato_del_dia'; UPDATE configuraciones SET valor = (SELECT valor FROM configuraciones WHERE nombre='FLAG')  WHERE nombre= 'plato_del_dia'; --`.

### Respuestas a preguntas explícitas

#### Explicación del Script de Python para realizar la inyección ciega de forma automática

#### Explicar dos mitigaciones posibles para el o los problemas que permitieron extraer este valor (FLAG), con sus beneficios y limitaciones

TODO
