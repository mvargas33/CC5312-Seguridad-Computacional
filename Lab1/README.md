## Laboratorio 1

Respuesta detalla y análisis en Reporte PDF. Para ejecutar el código seguir las siguientes instrucciones.

### P1

- Posicionarse en la carpeta correspondiente a la P1.
- Ejecutar `main.py` para obtener los archivos encriptados.
- Ejecutar `findprimes.py` para obtener el texto plano.
- Comprar `deciphered.txt` con `deciphered-MANUAL.txt`, donde el primero es el texto plano original, y el segundo el descifrado con el ataque.

### P2

- Posicionarse en la carpeta correspondiente a la P2
- Ejecutar `main.py` para realizar ataque. El programa imprimirá que byte de qué bloque del cipher text se está atacando en cada momento. Al final hace print de los bloques desencriptados como bytearrays de python. Más info en el PDF adjunto.
- NOTA: A veces el servidor responde lento, o la conexión queda en un estado incosistente y la terminal queda pegada. Si se reinicia el programa funciona sin problemas, causas ¿? No lo sabemos.
- NOTA2: Tuvimos que crear dos sockets adicionales sólo para calcular el largo de los bloques, lo cual hace el código menos legible. Sin embargo, si se reutilizaban estos sockets para el ataque, el servidor quedaba desfasado en mensajes. Por eso preferimos usar sockets aparte.
