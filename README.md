# Taller TCP en Python

Este proyecto implementa una pequeña aplicación cliente-servidor utilizando sockets TCP en Python. El objetivo es enviar una cadena desde un cliente al servidor, contar cuántas veces aparece el último carácter dentro de esa cadena y devolver el resultado.

## Descripción del proyecto

El repositorio contiene dos versiones del servidor:

- `servidor_tcp_mono.py`: servidor simple, secuencial.
- `servidor_tcp_multi.py`: servidor multihilo con cola para persistencia.
- `cliente_tcp.py`: cliente que envía un texto al servidor y muestra la respuesta.

Además, el proyecto guarda registros de conexiones y resultados en archivos de texto:

- `registro_conexiones.txt`
- `resultados.txt`

## ¿Qué hace la aplicación?

1. El cliente ingresa una cadena.
2. Se envia la cadena al servidor mediante TCP.
3. El servidor analiza la cadena.
4. Calcula cuántas veces aparece el último carácter dentro del texto.
5. Devuelve ese número al cliente.
6. Guarda información del evento en un archivo de registro.

Ejemplo:

- Entrada: `hola mundo`
- Último carácter: `o`
- El último carácter aparece 2 veces

## Requisitos

- Python 3.x
- Sistema operativo con soporte para sockets TCP

## Ejecutar el servidor simple

```bash
python servidor_tcp_mono.py
```

El servidor quedará escuchando en:

- Host: `0.0.0.0`
- Puerto: `5050`

## Ejecutar el servidor multihilo

```bash
python servidor_tcp_multi.py
```

Este servidor usa un pool de hilos para atender varias conexiones concurrentes y una cola para escribir los resultados en un archivo sin bloquear la respuesta del cliente.

## Ejecutar el cliente

En otra terminal o ventana:

```bash
python cliente_tcp.py
```

Se pedirá ingresar una cadena, por ejemplo:

```text
Ingrese una cadena: hola mundo
```

La salida mostrará algo como:

```text
Último carácter aparece: 2 veces
```

## Archivos generados

### `registro_conexiones.txt`

Guarda registros del servidor simple con información como:

- fecha y hora
- IP del cliente
- puerto
- cadena recibida
- longitud calculada

### `resultados.txt`

Guarda información del servidor multihilo, con la fecha, la cadena y la cantidad de repeticiones del último carácter.

## Notas importantes

- El puerto por defecto es `5050`.
- El cliente usa `127.0.0.1` para conectarse localmente.
- Si se ejecuta el servidor en una red local o en un entorno remoto, puede cambiar la dirección `HOST` según el caso.
- En el servidor multihilo, también se registra actividad con `logging` para observar conexiones, errores y eventos importantes.

## Autor

Proyecto desarrollado para el taller de programación con sockets TCP y concurrencia en Python.
