from const import ADDRESS
from socket import socket, AF_INET, SOCK_STREAM
import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def receive_messages() -> None:
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                logging.info(f"Received: {message}")
            else:
                break
        except Exception as e:
            logging.error(f"Error receiving message: {e}")
            break

if __name__ == "__main__":
    client_socket: socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDRESS)

    receive_thread: threading.Thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    logging.info("Enter 'exit()' to disconnect.")
    while True:
        message: str = input('Message: ')
        if message.lower() == 'exit()':
            break
        client_socket.send(message.encode('utf-8'))

    client_socket.close()
    logging.info("Disconnected from server.")