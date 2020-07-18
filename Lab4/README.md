# Lab 4

Instructions
* Install requirements `pip3 install requirements.txt`
* Install tcpdump
* Execute with `sudo` (some of this protocols require elevated privileges to send packages using restricted ports)

# P1 Memached

La estrategia a usar es simple: guardar un valor de tamaño máx en el servior, con una llave de tamaño mínimo (1 bytes). Luego hacer get del recurso y recibir una respuesta de largo mayor al get.

Si el largo más grande fuera 1000 bytes por ejemplo, el comando para setear se contruye así:

```python
key = b'k'
exptime = 0 // Forever
size = 1000
val = b'a'*size
command = 'set %s 0 %d %d\r\n%s\r\n' % (key, exptime, len(val), val)
```

Y el comando para preguntar:

```python
command = 'get %s\r\n' % (key)
```

De esta forma se obtiene una eficiencia de amplificaión cercana a 1000 / 7 = 142.8

## Mejorando el ataque

Sin embargo, queremos saber exactamente cuántos son los bytes máx que se pueden guardar en un par (key, value). Para esto ejecutamos `stats settings` y buscamos el parámetro `item_size_max`. Obtenemos el valor de 1Mb, lo cual es el default.

Entonces, ahora se intenta usar un size de 1024*1024, pero UDP nos manda un error de largo de mensaje:

(acá pantallazo)

Lo que pasa es que un datagrama de UDP puede tener un largo de hasta aprox. 65535 bytes (65507 al sacar headers). Por lo tanto estamos limitados a mandar comandos de hasta ese largo aprox.

Fuente: https://stackoverflow.com/questions/1098897/what-is-the-largest-safe-udp-packet-size-on-the-internet

Para conexiones TCP esto no sucede, ya que permite mandar mensajes de largo arbitrario entre dos servidores mediante la abstracción de sockets.

Se encontraron implementaciones (otras librerías) para guardar archivos de largo arbitrarios en memcached guardando chunks de 1.000.000 de bytes en llaves sucesivas, pudiendo reconstruir el paquete si se preguntaba por el ítem en el mismo orden. Además se usan hashes para integridad.

Fuente: https://github.com/Lunacie/pymemcache-large-file/blob/master/caching.py

Sin embargo esta implementación se basa en `pymemcached` que funciona mediante TCP, y es por esto que el script puede mandar comandos de largo arbitrario, lo cual en nuestro caso es imposible por las limitaciones de UDP.

Fuente: https://github.com/pinterest/pymemcache/blob/master/pymemcache/client/base.py

Por lo tanto se busca cuál es el mayor largo de comandos que acepta memcached mediante UDP: 1400 bytes en total

Fuente: https://github.com/memcached/memcached/blob/14521bd820869f70fbcf6e2b57c3eba0fbb60367/memcached.h#L68

Lo que permitiría guardar un ítem de largo cercano a 1400 bytes y obtener un eficiencia de 1400 / 7 = 200

## Tryhardeando aún más

Pero no nos quedaremos acá, porque memcached permite obtener varios ítemes a la vez usando comando `gets`. Por lo tanto, podemos obtener tantos ítemes como nos permita el largo de comando de 1400 bytes. El comando tiene el siguiente formato:

gets <key>*\r\n
- <key>* means one or more key strings separated by whitespace.

Fuente: Doc Oficial de Memcached https://github.com/memcached/memcached/blob/14521bd820869f70fbcf6e2b57c3eba0fbb60367/doc/protocol.txt#L284

Lo cual permitiría preguntar por (1400 - 5) / 2 = 697 ítemes, si las llaves son de un byte. Quedando algo como:

`gets a b c d e f g h i ...`

Sin embargo, sólo tenemos 255 valores distintos en un byte, por lo tanto luego debemos usar llaves de dos bytes. Al final quedan 255 llaves de un byte, lo cual usa 510 bytes del mensaje, dejando (1400 - 5 - 510) = 885 bytes, y por lo tanto alcanzan 295 llaves más (cada pregunta usa 2 bytes para la key, y un espacio de separación). En total son 550 ítems consultados.

`gets a b c d e f g h i ... aa ab ac ad ...`

Y si cada ítem pesa 1400 bytes, tenemos una consulta de tamaño 1400, y se nos retornan 1400*550 bytes. Dando una eficiencia de 1400*550/1400 = 550. 

Analicemos el caso en que sólo preguntamos por 255 llaves: La consulta usa 5 + 2*255 = 515 bytes, y la respuesta es de 1400*255 = 357.000 bytes. La eficiencia es 357.000/515 = 693.2.

Por lo tanto la consulta más eficiente sólo contiene llaves de largo 1 a ítemes de largo 1400, aunque la sobrecarga de red es mayor en el caso de usar un comando gets de 1400 bytes, porque se usa más banda ancha (más bytes en total transferidos desde el servidor).

Nos acotaremos entonces al caso de llaves de largo 1 byte.

Entonces, para probar el caso base guardamos dos valores en llaves a y b, con contenido de 1400 bytes. Luego hacemos la consulta `gets a b`, pero notamos que sólo recibimos el contenido de a:

(foto de gets a b)

Bajamos un poco las expectativas y guardamos en a y b contenido de unos pocos bytes:

(foto de hola chao)

Entonces nos damos cuenta que toda la respuesta del comando gets debe caber en un paquete UDP de 1400 bytes, por lo tanto, independiente de por cúantas llaves preguntemos sólo nos pueden responder hasta 1400 bytes en un sólo paquete UDP.

En conclusión, `gets` no tiene ningún efecto en el ataque, y lo más eficiente es hacer `get a`, y guardar en a un valor de 1400 bytes (máx tamaño que se puede enviar y recibir en un paquete UDP para la implementación de memecached)

## Otras ideas

Se podría buscar el ítem que tenga más bytes almacenado en memchached y preguntar por él, utilizando `stats slabs`, y luego `stats cachedump <slab class> <number os items to dump>` buscar la key de los items y luego preguntar por las keys.

Fuente: https://lzone.de/blog/How-to%20Dump%20Keys%20from%20Memcache

Pero como hemos concluirdo, la mayor respuesta que permite UDP es de 1400 bytes, por lo tanto aunque el ítem de mayor tamaño pese 1Mb (máx default), sólo se nos enviarán los primeros 1400 bytes de este ítem.

## Conclusiones de memcached

La mejor eficiencia obtenida es aproximadamente 1400/7 = 200, dado que se guarda el par (key, value), donde key es de 1 byte y value de 1400, y luego se hace `get key\r\n`.

# P1 DNS

1) La utilidad original del servicio DNS es resolver la IP de un name server, puesto que, para los humanos es más sencillo recordar conjuntos de palabras que conjuntos numéricos. Luego este servicio, dado un name server, por ejemplo : ucursos.cl, devuelve su ip asociada al navegador para poder, finalmente, acceder al sitio web.

2) Se adjunta en el script las modificaciones realizadas con lo que a la obtención de la salida estándar refiere.

3) Se propone para maximizar la eficiencia ocupar el total de RR's permitidas por el protocolo DNS, llenando el espacio designado del protocolo a estas respuestas, para así obtener una respuesta emitida por el servidor más grande de lo que se consulta. Para realizarlo se propone obtener un dominio que contenga varios subdominios para así enviar los RR's correspondientes a cada subdominio asociado al recorrido de la resolución enviada al servicio de DNS.

4) Para maximizarla se debería eliminar las limitaciones de cortar una respuesta en la respuesta recibida por el DNS, puesto que, en un datagrama UDP, los paquetes son de tamaño fijo.

# P1 NTP

1) NTP se basa en el uso de UDP para enviar y recibir mensajes, donde no se valida la IP del enviador, por lo tanto se puede hacer spoofing de la IP, usando la IP de la víctima

2) Luego existen dos comandos donde se envían pocos bytes de solicitud y se retornan muchos más de respuesta: `REQ_MON_GETLIST` y `REQ_MON_GETLIST_1`, por factores de 3660 y 5500 respectivamente (misma definición de eficiencia del enunciado). Otras fuentes indican factores entre 556-4670

3) Monlist entrega hasta 100 datagramas UDP de 440 bytes de payload cada uno. La respuesta contiene las estadísticas de los clientes NTP: IP's de últimos clientes contactados (que hacen requests), NTP version y número de requests por cliente que contactaron al servidor.

4) La forma de mejorar el ataque es maximizando la lista de clientes que se contactan con el servidor que presenta la vulnerabilidad (acepta monlist). Para ello:

    a) Se debe encontrar un servidor que corra NTP con una versión anterior a la 4.2.7p26 y que no haya deshabilitado el comando.

    b) Se necesita enmascarar las  600 - N IPs necesarias para llenar la lista de clientes contactados recientemente del servidor, donde N son las IPs ya existentes de clientes honestos que contactan al servidor.

    Como UDP no valida el source de la IP, se podría variar manualmente la IP de los paquetes UDP para hacer requests al servidor NTP, siguiendo el protocolo en forma honesta pero invisible: NTP debe intercambiar timestamps, entonces por ejemplo, intentamos mandar un paquete estándar de primer request con IP source distinta a la nuestra, luego el servidor responde a esa IP (no vemos la respuesta), pero asumiendo que todo va bien, podemos mandar las requests que vienen en forma default con la IP cambiada. Asumiremos que después de un punto el servidor guarda la información de este cliente fantasma y lo incluirá en la respuesta de `monlist`.

    c) Luego hacer `monlist` al servidor (que retornará una cantidad máx de clientes recientes) usando en los paquetes UDP la IP de la víctima.
    
5) En forma práctica, sólo mandamos el request `REQ_MON_GETLIST_1` al servicio que corría el servidor del lab, y nos retornó un mensaje tal que la eficiencia de amplificación fue de 4.05 aproximadamente.


Fuente (KB CERT): https://www.kb.cert.org/vuls/id/348126
Fuente (Christian Rossow): https://christian-rossow.de/publications/amplification-ndss2014.pdf

