import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5050
TXT_PATH = "registro_conexiones.txt"

def count_last_char(text: str) -> int:
    """Cuenta cuántas veces aparece el último carácter en la cadena."""
    last_char = text[-1]
    return text.count(last_char)

def guardar_en_txt(addr, cadena, longitud):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"{timestamp},{addr[0]},{addr[1]},{cadena},{longitud}\n"
    with open(TXT_PATH, "a", encoding="utf-8") as f:
        f.write(linea)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")
    try:
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conexión establecida desde {addr}")
                data = conn.recv(1024)
                if not data:
                    continue
                cadena = data.decode("utf-8").strip()
                if not cadena:
                    conn.sendall("ERROR: el mensaje no puede estar vacío\n".encode("utf-8"))
                    continue
                longitud = count_last_char(cadena)
                conn.sendall(str(longitud).encode("utf-8"))
                guardar_en_txt(addr, cadena, longitud)
                print(f"Recibido: '{cadena}' -> Último carácter '{cadena[-1]}' aparece {longitud} veces")
    except KeyboardInterrupt:
        print("\nServidor detenido")
