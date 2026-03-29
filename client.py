import socket
import threading


def make_request(i):
    try:
        print(f"[→] Запрос {i} отправлен")

        # Создаём сокет
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Подключаемся к серверу
        client.connect(("localhost", 8080))

        # Формируем HTTP-запрос вручную
        request = (
            "GET / HTTP/1.1\r\n"
            "Host: localhost\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        client.sendall(request.encode())

        # Получаем ответ (читаем до конца)
        response = b""
        while True:
            data = client.recv(1024)
            if not data:
                break
            response += data

        client.close()

        print(f"[←] Ответ {i}:\n{response.decode()}\n")

    except Exception as e:
        print(f"[!] Ошибка в запросе {i}: {e}")


def main():
    threads = []

    # 10 параллельных клиентов
    for i in range(10):
        t = threading.Thread(target=make_request, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("[*] Все запросы завершены")


if __name__ == "__main__":
    main()