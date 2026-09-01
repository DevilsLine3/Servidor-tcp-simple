import socket

HOST = "127.0.0.1"
PORT = 5050

with socket.create_connection((HOST, PORT)) as s:
    mensaje = input("Ingrese una cadena: ")
    s.sendall(mensaje.encode("utf-8"))
    data = s.recv(1024)
    print(f"Último carácter aparece: {data.decode('utf-8').strip()} veces")
