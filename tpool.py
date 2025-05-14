from socket import *
import socket
import logging
import json
from concurrent.futures import ThreadPoolExecutor
from file_protocol import FileProtocol

fp = FileProtocol()

# Fungsi pengganti class thread, sesuai dengan pola ThreadPoolExecutor
def ProcessTheClient(connection, address):
    try:
        data_received = ""
        while True:
            data = connection.recv(1024)
            if data:
                d = data.decode()
                data_received += d
                if data_received[-1:] == '\n':
                    hasil = fp.proses_string(data_received.strip())
                    hasil = hasil + "\r\n\r\n"
                    connection.sendall(hasil.encode())
                    break
            else:
                break
    except Exception as e:
        logging.warning(f"Error processing client {address}: {str(e)}")
    finally:
        connection.close()

def main():
    server_address = ('0.0.0.0', 46666)
    max_workers = 50  # Jumlah thread dalam pool

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(server_address)
        server_socket.listen(5)
        logging.warning(f"Server listening on {server_address}")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            while True:
                connection, client_address = server_socket.accept()
                logging.warning(f"Accepted connection from {client_address}")
                executor.submit(ProcessTheClient, connection, client_address)

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()

