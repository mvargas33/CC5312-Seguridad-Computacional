## DNS Spoofing

### ¿Cómo correr el código?

Para correr código es necesario tener instalada la biblioteca `scapy` con el comando `pip install scapy`, en una máquina virtual utilizando Linux (fue probado en Lubuntu).

Luego basta utilizar un visualizador de código como Visual Studio Code con la versión 3.8 de Python para correr el código con el botón play, o desde un terminal `sudo python3 dns_spoofing.py`.

Notar que es necesario:

Estar conectado/a a la VPN del CEC : `sudo openvpn --config CEC-fcfm.ovpn`

Cambiar `malicious_ip` por la IP que entrega la VPN del CEC

Levantar un servidor HTTP en el puerto 5312 : `while true; do printf 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n{"ok": true}' | netcat -l -w 1 5312; done`

### ¿Cómo se llegó a la solución propuesta?

Para la solución propuesta inicialmente se examinó la respuesta obtenida por el DNS Resolver para un caso en el que entregue la IP correcta, vale decir, resuelva correctamente. Con esta información considerada, posteriormente se modificó el paquete recibido con la información `IP destino`, `ID de consulta DNS`, `IP asociada al dominio consultado` y además la información del identificador de la consulta DNS la que se iteraba entre un valor entre 1 y 1024.

Posteriormente, dado que se quiere recibir la información que envía el cliente, en este caso un TOTP, se levantó un servidor HTTP que imprimía en pantalla la flag que el cliente enviaba, creyéndo que lo hacía al sitio que esperaba, hacia nuestro servidor.

La FLAG obtenida entre las `13:51:58.670729` y las `13:52:03.040490` del día 22 de Julio del año 2020 corresponde a :  `139949`.

Observación: La máquina virtual decía `13:51:58.670729`, cuando en el reloj de Windows eran las `12:51:58`

En el apartado de los anexos se muestra la obtención de la flag mediante un Screenshot.

### Respuestas a preguntas explícitas

#### Explicar la factibilidad de un ataque de tipo DNS Spoofing si cada uno de estos problemas de implementación no existiera (manteniendo los otros problemas de implementación):

##### Si el puerto de origen de la consulta DNS variase constantemente.
Si el puerto del usuario cambia constantemente, este puede variar entre los valores 1 y 65536, y por cada uno de estos valores, habría que probar todos los ID de request DNS que son 1024 (por enunciado). Entonces el espacio de posibilidades aumenta en 65535x, lo cual hace más infactible el ataque, pero no tan imposible aún:

- Por el ataque de cumpleaños, si el usuario cambia el puerto en forma equibrobale, entonces después de 1.2*sqrt(65536) cambios, es altamente probable, que repita un puerto, esto es después de 307.2 intentos. Y si cambia el puerto cada 10 ms, luego de 3 segundos se repite el puerto con alta probabilidad. Por lo tanto se podría atacar a un puerto fijo realizando el ataque constantemente, esperándo que el usuario repita el puerto en algún momento y se finalice el ataque.

  La probabilidad de éxito (en función del tiempo) depende directamente de la frecuencia en que el usuario cambia el puerto

  Fuente: https://es.wikipedia.org/wiki/Ataque_de_cumplea%C3%B1os

- El ataque puede hacerse de todas formas con máquinas en paralelo, donde cada una apunte a los 65536 puertos distintos, o bien, que cada una abarque un rango depuertos. Luego realizar el ataque variando el ID de TX. Esto puede hacerse contratando una botnet por ejemplo ($10 USD por hora).


##### Si el ID de request pudiese tomar cualquier valor.
El ID tiene 16 bits en el paquete, por que puede tomar 65536 valores dintintos, si el puerto a atacar es fijo, entonces la probabilidad de éxito por intento disminuye, pero el ataque sigue siendo factible, porque si bien, antes se probaban 1024 valores, y en aprox. 10 seg se obtenía la flag, ahora ese tiempo será mayor, pero se obtendrá la flag eventualmente.

Lo único que cambia es el espacio de valores a probar que ahora es mayor.


##### Si el cliente no esperara paquetes de cualquier IP de origen.
El protocolo IPv4 aguanta 2^32 valores distintos, IPv6 2^128. Por lo tanto, sin saber qué rango de IPs acepta el usuario (y asumiendo que ningún router bloqueará los paquetes con IPs extrañas) es muy infacible completar el ataque sólo provando valores IP distintos, y para cada uno 1024 valores distintos.

Además, en la realidad, si tenemos el rango de IPs que acepta el usuario, deberíamos de alguna forma tener acceso a alguna máquina destro de ese rango, para que la IP de origen no se vea como maliciosa por los routers/firewalls y no se bloqueen los paquetes. Y esto ya es infactible, ya que asociar IP a georeferenciasción parece ser un problema disfuso (por lo dicho en clases) como para saber siquiera dónde atacar para conseguir acceso a una máquina con esos valores IP.

##### Comparación de espacios de búsqueda

Se puede ver del siguiente gráfico que el espacio de C (restricción de IP) es exponencialmente mayor al del caso A (Puerto cambiante), y este mayor al caso B(Valores posibles de TX ID). Además la curva que ajusta el gráfico es exponencial, por lo que la probabilidad de hacer cada ataque disminuye exponencialmente también, y se hacen menos factibles.

![GRAFICO](http://anakena.dcc.uchile.cl/~patorres/Laboratorio4Seguridad/EspacioDeBusqueda.png)
Ref : EspacioDeBusqueda

La infactibilidad puede medirse en tiempo usando el ataque de cumpleaños para cualquier espacio de búsqueda, y con eso darse cuenta de la factibilidad de cada cada caso.

### Explicación del Script de Python para realizar el DNS Spoofing:

Inicialmente se importan las bibliotecas necesarias para generar paquetes, mediante la biblioteca `scapy`.

![CODE A](http://anakena.dcc.uchile.cl/~patorres/Laboratorio4Seguridad/CodeABibliotecas.jpg)

Ref : CODEABibliotecas

Además, se agregan como valores constantes al inicio del script nuestra IP y la IP de la víctima.

![CODE B](http://anakena.dcc.uchile.cl/~patorres/Laboratorio4Seguridad/CodeBTunneables.jpg)

Ref : CodeBTunneables

Posteriomente se reutiliza la consulta DNS de la clase auxiliar, cambiando los campos del usuario que recibe la respuesta por nuestra dirección otorgada por la VPN.

![CODE C](http://anakena.dcc.uchile.cl/~patorres/Laboratorio4Seguridad/CodeCAnsDNS.jpg)

Ref : CodeCAnsDNS

Con la información de la estructura del paquete, es posible generar un paquete para la IP que consulta con una IP maliciosa (la nuestra), para que el cliente o víctima se conecte a nuestro servidor.

![CODE D](http://anakena.dcc.uchile.cl/~patorres/Laboratorio4Seguridad/CodeDpktgen.jpg)

Ref : CODE D

Dado que, existen 1024 números distintos de ID's para la consulta DNS, se prueba por cada uno de ellos, enviando 1024 paquetes con 1024 valores distintos

![CODE E](http://anakena.dcc.uchile.cl/~patorres/Laboratorio4Seguridad/CodeEEnviar.jpg)

Ref : CODE E

### Anexo

En esta sección se muestran los pasos utilizando imagenes para dar mayor claridad a cómo se realizó la experimentación en este apartado del Laboratorio:

El Plan consiste en ganarle al DNS, hacer que el sitio web entre a nuestro servidor y robárle el TOTP:

![El Plan](http://anakena.dcc.uchile.cl/~patorres/Laboratorio4Seguridad/LAB4_PLAN_B.png)

Ref : LAB4_PLAN_B.png

No se realiza la importación de la biblioteca `scapy` en la máquina virtual:

![Import Scapy VM Fail](http://anakena.dcc.uchile.cl/~patorres/Laboratorio4Seguridad/0%20NotImporting.jpg)

Ref : 0 NotImporting.jpg

Correción del Problema de la importación:

![Import Scapy Correction](http://anakena.dcc.uchile.cl/~patorres/Laboratorio4Seguridad/1%20Correction.jpg)

Ref : 1 Correction.jpg

Conexión con la VPN:

![VPN Connection](http://anakena.dcc.uchile.cl/~patorres/Laboratorio4Seguridad/2%20VPN.jpg)

Ref : 2 VPN.jpg

Servidor Corriendo:

![Server Running](http://anakena.dcc.uchile.cl/~patorres/Laboratorio4Seguridad/3%20Server%20Running.jpg)

Ref : 3 Server Running.jpg

Envío de Paquetes visualizados en Wireshark:

![Wireshark](http://anakena.dcc.uchile.cl/~patorres/Laboratorio4Seguridad/4%20Wireshark.png)

Ref : 4 Wireshark.jp

Valor de la Flag:

![Flag Value](http://anakena.dcc.uchile.cl/~patorres/Laboratorio4Seguridad/5%20We%20have%20the%20flag.jpg)

Ref : 5 We have the flag.jpg
