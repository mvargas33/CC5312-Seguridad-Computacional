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

En ambos casos se obtuvo el mismo valor de la FLAG la que corresponde a : `L7VfqfIY5XQU7fdLoiXenbKnuTMEEvze`

### Respuestas a preguntas explícitas

#### Explicación del Script de Python para realizar la inyección ciega de forma automática


Inicialmente se importan las bibliotecas necesarias para realizar la conexión a internet, mediante la biblioteca `requests`. Posteriomente en un diccionario se almacena el valor de la cookie encontrada en la P1, además de generar una lista con las alternativas alfanuméricas.

![CODE A](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P2/CODE%20A.png)

Luego se genera un código que obtiene un valor de verdad de acuerdo a si el tiempo de sleep es mayor o igual al tiempo fijado anteriormente en la variable `sleep_time` (3 segundos). Inicialmente se escribe una versión "tunneable" de la consulta mediante un f_string `query_d = f"RSA' WHERE nombre = 'platodeldia'; SELECT CASE when (SELECT 1 FROM configuraciones WHERE nombre ='FLAG' and valor like '{elem}') = 1 then pg_sleep({sleep_time}) else pg_sleep(0) end; --"`, de esta forma es posible automatizar el cambio de los parámetros `elem` y `sleep_time`.

En el valor de payload se obtiene el id del input del formulario, el que corresponde a `plato_del_dia`. Se obtiene el tiempo actual y se realiza la request POST, añadiendo las cookies y el valor de verify en false debido a la no verificación HTTTPS del sitio. Cuando termina la request se obtiene el tiempo de término para realizar un delta que permita discernir entre si correspondió a un acierto o no, lo que se obtiene de acuerdo a si delta es mayor o igual a `sleep_time`, retornado `True` y `False` si no es mayor.

![CODE B](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P2/CODE%20B.png)

Finalmente se realiza el ciclo while, el que al principio de cada iteración obtiene el largo actual de la FLAG, pues la condición de término es si no agrega más carácteres al valor de la FLAG. Dentro del ciclo se tiene un ciclo for que itera por los posibles carácteres alfanuméricos, los que se van testeando utilizando la función `send_and_delta_time_it(elem)`, y si retorna `True` se agrega a la clave si no continúa iterando.

Cuando los largos de las claves son iguales, entonces se detiene el algoritmo imprimiendo en pantalla el valor de la FLAG obtenida.

![CODE C](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P2/CODE%20C.png)


#### Explicar dos mitigaciones posibles para el o los problemas que permitieron extraer este valor (FLAG), con sus beneficios y limitaciones

- Una mitigación puede ser validar el input en cada formulario. Por ejemplo, se pueden usar expresiones regulares para definir que los platos sólo pueden ser alfanuméricos y espacios: Esto descarta caracteres como ';','*', '--', '(', ')' que son típicos de inyecciones SQL. Estas validaciones se deben hacer en el cliente, pero sobretodo en el servidor antes de guardar los valores en la base de datos. Esto limita bastante los valores que puede tomar el input, lo cual es un claro beneficio. Dentro de las limitaciones tenemos que no podemos poder nombres raros a los platos pero qué mas da.

- Otra mitigación son las consultas parametrizadas o precompiladas. En estas consultas el input no se concatena directamente con la consulta, si no que el input se reemplaza más tarde. Por ejemplo, tenemos la consulta precompilada `SELECT nombre FROM Usuarios WHERE nombre =? and clave =?"`. En este caso no podemos inyectar código del estilo `(SUBQUERY);--` en nombre. Simplemente se buscará en la tabla un usuario de nombre `(SUBQUERY);--` y que de seguro no se encontrará. Lo que pasa acá es que las acciones de la consulta son precompiladas antes de hacer el input, la secuencia de pasos ya está definida desde antes y por lo tanto no es modificable.


### Anexo

En esta sección se muestran los pasos utilizando imagenes para dar mayor claridad a cómo se realizó la experimentación en este apartado del Laboratorio:

Primer bug:

![First Bug](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P2/0%20Primer%20bug.png)

Campo del Form:

![Form field](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P2/1%20Campo%20Form.png)

Anulador de la sentencia SQL:

![Anular sentencia SQL](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P2/2%20Consejo2.png)

Valor de la Flag:

![Flag Value](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P2/3%20FLAG2.png)

SQLQuery para obtener la Flag directamente:

![Direct Query](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P2/4%20SQLQueryFail.png)

Sitio mostrando la Flag:

![Flag en el sitio](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P2/5%20SQLQueryFailProof.png)
