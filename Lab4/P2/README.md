## DNS Spoofing

### ¿Cómo correr el código?

Para correr código es necesario tener instalada la biblioteca `scapy` con el comando `pip install scapy`, en una máquina virtual utilizando Linux (fue probado en Lubuntu).

Luego basta utilizar un visualizador de código como Visual Studio Code con la versión 3.8 de Python para correr el código con el botón play, o desde un terminal `python dns_spoofing.py`.

Notar que es necesario:

Estar conectado/a a la VPN del CEC : `sudo openvpn --config CEC-fcfm.ovpn`

Levantar un servidor HTTP en el puerto 5312 : `while true; do printf 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n{"ok": true}' | netcat -l -w 1 5312; done`

### ¿Cómo se llegó a la solución propuesta?

Para la solución propuesta inicialmente se examinó la respuesta obtenida por el DNS Resolver para un caso en el que entregue la IP correcta, vale decir, resuelva correctamente. Con esta información considerada, posteriormente se modificó el paquete recibido con la información `IP destino`, `ID de consulta DNS`, `IP asociada al dominio consultado` y además la información del identificador de la consulta DNS la que se iteraba entre un valor entre 1 y 1024.

Posteriormente, dado que se quiere recibir la información que envía el cliente, en este caso un TOTP, se levantó un servidor HTTP que imprimía en pantalla la flag que el cliente enviaba, creyéndo que lo hacía al sitio que esperaba, hacia nuestro servidor.

La FLAG obtenida entre las `13:51:58.670729` y las `13:52:03.040490` del día 22 de Julio del año 2020 corresponde a :  `139949`.

En el apartado de los anexos se muestra la obtención de la flag mediante un Screenshot.

### Respuestas a preguntas explícitas

#### TODO Explicar la factibilidad de un ataque de tipo DNS Spoofing si cada uno de estos problemas de implementación no existiera (manteniendo los otros problemas de implementación):

##### Si el puerto de origen de la consulta DNS variase constantemente.
##### Si el ID de request pudiese tomar cualquier valor.
##### Si el cliente no esperara paquetes de cualquier IP de origen.

### Explicación del Script de Python para realizar el DNS Spoofing:

Inicialmente se importan las bibliotecas necesarias para generar paquetes, mediante la biblioteca `scapy`. Posteriomente se reutiliza la consulta DNS de la clase auxiliar, cambiando los campos del usuario que recibe la respuesta por nuestra dirección otorgada por la VPN.

![CODE A](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P2/CODE%20A.png)

Ref : CODE A

Con la información de la estructura del paquete, es posible generar un paquete para la IP que consulta con una IP maliciosa (la nuestra), para que el cliente o víctima se conecte a nuestro servidor.

![CODE B](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P2/CODE%20A.png)

Ref : CODE B

Dado que, existen 1024 números distintos de ID's para la consulta DNS, se prueba por cada uno de ellos, enviando 1024 paquetes con 1024 valores distintos

![CODE C](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P2/CODE%20A.png)

Ref : CODE C

### Anexo

En esta sección se muestran los pasos utilizando imagenes para dar mayor claridad a cómo se realizó la experimentación en este apartado del Laboratorio:

El Plan:

![El Plan]()

Ref : 0 Import Scapy VM Fail

No se realiza la importación de la biblioteca `scapy` en la máquina virtual:

![Import Scapy VM Fail](http://anakena.dcc.uchile.cl/anakena.jpg)

Ref : 0 Import Scapy VM Fail

Correción del Problema de la importación:

![Import Scapy Correction](http://anakena.dcc.uchile.cl/anakena.jpg)

Ref : 1 Import Scapy Correction

Conexión con la VPN:

![VPN Connection](http://anakena.dcc.uchile.cl/anakena.jpg)

Servidor Corriendo:

![Server Running](http://anakena.dcc.uchile.cl/anakena.jpg)

Ref : Server Running

Envío de Paquetes visualizados en Wireshark:

![Wireshark](http://anakena.dcc.uchile.cl/anakena.jpg)

Ref : Wireshark

Valor de la Flag:

![Flag Value](http://anakena.dcc.uchile.cl/anakena.jpg)

Ref : We have the flag
