## Inyección XSS

### ¿Cómo correr el código?

Para correr el código `js_script` es necesario copiarlo y pegarlo en la sección de comentarios del sitio [Buffet Overflow](https://lsrw3krbznioprtvgdg8rx4s.lab3.cc5312.xor.cl/), la que se puede acceder utilizando la VPN del CEC, la que se puede configurar siguiendo [este sitio](https://www.cec.uchile.cl/vpn/).

Generar un servidor HTTP mediante el siguiente comando en Ubuntu o WSL (para Windows 10) `while true; do
    printf 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n{"ok": true}' | netcat -l -w 1 5312;
done`, obtenido desde el sitio de la [clase auxiliar 5](https://users.dcc.uchile.cl/~eriveros/cc5312/auxiliares/auxiliar-5/).

Para saber en qué dirección ip se ubica el servidor se puede utilizar el comando `ifconfig`

Puede revisar la sección anexo ubicada después de la sección de respuestas a preguntas explícitas para más detalles.

### ¿Cómo se llegó a la solución propuesta?

Dado que se quería "robar" una sesión, nuestro objetivo era obtener las cookies de administrador, por lo que inicialmente se probó con ingresar un comando `console.log(document.cookie);`, sin embargo nos percatamos de que esto mostraría las cookies en el navegador del BOT. Debido a este motivo se razonó que era necesario generar una entidad que obtuviese la información de las cookies del BOT, esta entidad corresponde a un servidor HTTP, el que escucha las solicitudes que se le envían.

Luego se probó en la región de comentarios un comando de Javascript para verificar si era vulnerable para XSS, el comando fue el siguiente `<script>while(true){alert(1);}</script>`, el que mostraba popups con el mensaje "1".

Utilizando la estructura del código en Javascript de la clase auxiliar 5 (XSS), se generó un código que enviaba mediante el método POST las cookies al servidor HTTP generado anteriormente, para de esta forma obtener la cookie.

Con la cookie obtenida se "bypasseo" la sesión de administrador permitiéndonos ingresar un nuevo plato de comida para el día de hoy.

Para más detalles ver la sección anexo.

### Respuestas a preguntas explícitas

#### Explicar dos mitigaciones que hubiesen hecho que el ataque no resultara con sus beneficios y limitaciones (las mitigaciones pueden ser al mismo problema o problemas distintos)

TODO

### Anexo

En esta sección se muestran los pasos utilizando imagenes para dar mayor claridad a cómo se realizó la experimentación en este apartado del Laboratorio:

Objetivo:

![The Plan](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P1/0%20How%20to%20hack%20it.png)

Sitio no hackeado:

![Sitio no hackeado](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P1/1%20Site%20not%20yet%20Hacked.png)

Montando un servidor HTTP mediante WSL:

![Mount and Test HTTP Server](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P1/2%20VPN%20IP.png)

Código JS visualizado desde VS:

![VS JS](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P1/4%20Code%20in%20VS.png)

Añadir un comentario en el sitio:

![Add Comment](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P1/5%20AddComment.png)

Código malicioso añadido con éxito

![Malicious JS](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P1/6%20MaliciousJSCode.png)

¡Tenemos la cookie!

![I have the cookie](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P1/7%20Mounted%20Server%20and%20Cookie.png)

Estado antes de usar la cookie:

![Before use the cookie](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P1/8%20Before%20Inject%20Cookie.png)

Cookie anterior:

![Before use the cookie see the cookie](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P1/9%20Before%20Inject%20Cookie.png)

Cookie añadida:

![Cookie added](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P1/10%20Cookie%20Injected.png)

Tenemos privilegios de admin:

![Im an admin](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P1/11%20Configure%20Hacked.png)

El sitio ha sido hackeado de forma exitosa:

![Site hacked](http://anakena.dcc.uchile.cl/~patorres/Laboratorio3Seguridad/P1/12%20Site%20Has%20Been%20Hacked.png)
