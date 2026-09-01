import socket
import threading
import queue
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5050
MAX_WORKERS = 50          # tamaño del pool de threads
PERSIST_FILE = 'resultados.txt'
QUEUE_MAXSIZE = 2000       # tamaño máximo de la cola de espera

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(threadName)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Cola de mensajes en espera para persistencia
persist_queue = queue.Queue(maxsize=QUEUE_MAXSIZE)


def count_last_char(text: str) -> int:
    """Cuenta cuántas veces aparece el último carácter en la cadena."""
    last_char = text[-1]
    return text.count(last_char)


def persist_worker():
    """
    Hilo único dedicado que consume la cola y escribe en el archivo.
    Al ser el único consumidor, se evitan condiciones de carrera en el
    archivo sin necesidad de locks explícitos sobre el I/O.
    """
    with open(PERSIST_FILE, 'a', encoding='utf-8') as f:
        while True:
            item = persist_queue.get()
            if item is None:  # señal de apagado
                persist_queue.task_done()
                break
            word, count, ts = item
            f.write(f"{ts}\t{word}\t{count}\n")
            f.flush()
            persist_queue.task_done()


def handle_client(conn: socket.socket, addr):
    """Maneja una conexión de cliente (ejecutado por un hilo del pool)."""
    try:
        conn.settimeout(10)
        data = conn.recv(4096)
        if not data:
            return

        text = data.decode('utf-8', errors='replace').strip()

        if not text:
            response = "ERROR: el mensaje no puede estar vacío\n"
            conn.sendall(response.encode('utf-8'))
            logger.warning(f"Mensaje vacio de {addr}")
            return

        count = count_last_char(text)
        response = f"{count}\n"
        conn.sendall(response.encode('utf-8'))

        # Encolar para persistencia (no bloquea la respuesta al cliente)
        ts = datetime.now().isoformat()
        try:
            persist_queue.put_nowait((text, count, ts))
        except queue.Full:
            logger.error("Cola de persistencia llena, se descarta el registro")

        logger.info(
            f"{addr} -> {text!r} : ultimo caracter '{text[-1]}' aparece {count} veces"
        )

    except socket.timeout:
        logger.warning(f"Timeout con {addr}")
    except Exception as e:
        logger.exception(f"Error manejando a {addr}: {e}")
    finally:
        conn.close()


def main():
    # Arrancar el hilo escritor (consumidor de la cola)
    writer_thread = threading.Thread(
        target=persist_worker, name="PersistWriter", daemon=True
    )
    writer_thread.start()

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(256)
    logger.info(f"Servidor escuchando en {HOST}:{PORT}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS, thread_name_prefix="Worker") as pool:
        try:
            while True:
                conn, addr = server_sock.accept()
                pool.submit(handle_client, conn, addr)
        except KeyboardInterrupt:
            logger.info("Apagando servidor...")
        finally:
            persist_queue.put(None)   # señal de apagado para el escritor
            writer_thread.join(timeout=5)
            server_sock.close()


if __name__ == '__main__':
    main()