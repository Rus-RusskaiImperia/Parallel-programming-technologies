import socket
import threading
import time


def handle_client(client_socket, address):
    print(f"[+] Подключился клиент: {address}")

    try:
        # Получаем HTTP-запрос
        request = client_socket.recv(1024).decode()
        print(f"[{address}] Запрос:\n{request}")

        # Имитация долгой обработки (например, БД)
        time.sleep(10)

        # Тело ответа
        response_body = (
            f"Ответ от сервера\n"
            f"Поток: {threading.current_thread().name}\n"
            f"Клиент: {address}\n"
        )

        # HTTP-ответ
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

    # Чтобы можно было быстро перезапускать сервер
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(("0.0.0.0", 8080))
    server.listen(5)

    print("[*] Сервер запущен на http://localhost:8080")

    while True:
        client_socket, address = server.accept()

        # Создаём поток на каждого клиента
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, address)
        )

        client_thread.start()


if __name__ == "__main__":
    start_server()