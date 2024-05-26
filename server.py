from const import SERVER, ADDRESS
from socket import socket, AF_INET, SOCK_STREAM
import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(client_socket: socket, client_address: tuple[str, int]) -> None:
    logging.info(f"New connection from {client_address}.")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                logging.info(f"Message from {client_address}: {message}")
                broadcast_message(f"Message from {client_address}: {message}", client_socket)
            else:
                break
        except Exception as e:
            logging.error(f"Error handling message from {client_address}: {e}")
            break

    logging.info(f"Disconnected from {client_address}.")
    client_socket.close()

def broadcast_message(message: str, exclude_socket: socket) -> None:
    for client in clients:
        if client != exclude_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                logging.error(f"Error broadcasting message: {e}")
                client.close()
                clients.remove(client)

def start_server(server: socket, clients: list[socket]) -> None:
    server.listen()
    logging.info(f"Server is listening on {SERVER}")

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        logging.info(f"Active connections: {threading.active_count() - 1}")

if __name__ == "__main__":
    server: socket = socket(AF_INET, SOCK_STREAM)
    server.bind(ADDRESS)

    clients: list[socket] = []

    logging.info("Starting server...")
    start_server(server, clients)