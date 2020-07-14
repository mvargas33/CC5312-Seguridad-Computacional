# Lab 4

Instructions
* Install requirements `pip3 install requirements.txt`
* Install tcpdump
* Execute with `sudo` (some of this protocols require elevated privileges to send packages using restricted ports)

# Memached

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

Pero no nos quedaremos acá, porque memcached permite obtener varios ítemes a la vez usando comando `gets`. Por lo tanto, podemos obtener tantos ítemes como nos permita el largo de comando de 1400 bytes. El comando tiene el siguiente formato:

gets <key>*\r\n
- <key>* means one or more key strings separated by whitespace.

Fuente: Doc Oficial de Memcached https://github.com/memcached/memcached/blob/14521bd820869f70fbcf6e2b57c3eba0fbb60367/doc/protocol.txt#L284

Lo cual permitiría preguntar por (1400 - 5) / 2 = 697 ítemes, si las llaves son de un byte. Quedando algo como:

`gets a b c d e f g h i ...`

Sin embargo, sólo tenemos 255 valores distintos en un byte, por lo tanto luego debemos usar llaves de dos bytes. Al final quedan 255 llaves de un byte, lo cual usa 510 bytes del mensaje, dejando (1400 - 5 - 510) = 885 bytes, y por lo tanto alcanzan 295 llaves más (cada pregunta usa 2 bytes para la key, y un espacio de separación). En total son 550 ítems consultados.

Y si cada ítem pesa 1400 bytes, tenemos una consulta de tamaño 1400, y se nos retornan 1400*550 bytes. Dando una eficiencia de 1400*550/1400 = 550. 

Analicemos el caso en que sólo preguntamos por 255 llaves: La consulta usa 5 + 2*255 = 515 bytes, y la respuesta es de 1400*255 = 357.000 bytes. La eficiencia es 357.000/515 = 693.2.

Por lo tanto la consulta más eficiente sólo contiene llaves de largo 1 a ítemes de largo 1400, aunque la sobrecarga de red es mayor en el caso de usar un comando gets de 1400 bytes, porque se usa más banda ancha (más bytes en total transferidos desde el servidor).

Nos acotaremos entonces al caso de llaves de largo 1 byte.






