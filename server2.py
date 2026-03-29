import socket
import time
import threading
from concurrent.futures import ThreadPoolExecutor


def handle_client(client_socket, address):
    print(f"[+] Клиент подключён: {address}")

    try:
        request = client_socket.recv(1024).decode()
        print(f"[{address}] Запрос:\n{request}")

        # Имитация долгой операции
        time.sleep(10)

        response_body = (
            f"Ответ от сервера\n"
            f"Поток: {threading.current_thread().name}\n"
            f"Клиент: {address}\n"
        )

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            f"Content-Length: {len(response_body.encode())}\r\n"
            "\r\n"
            f"{response_body}"
        )

        client_socket.sendall(response.encode())

    except Exception as e:
        print(f"[!] Ошибка: {e}")

    finally:
        client_socket.close()
        print(f"[-] Клиент {address} отключён")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(("0.0.0.0", 8080))
    server.listen(5)

    print("[*] Сервер запущен на http://localhost:8080")

    executor = ThreadPoolExecutor(max_workers=5)

    while True:
        client_socket, address = server.accept()

        print(f"[~] Новое соединение: {address}")

        executor.submit(handle_client, client_socket, address)


if __name__ == "__main__":
    start_server()