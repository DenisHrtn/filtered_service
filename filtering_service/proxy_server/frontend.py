# frontend.py
import socket
import time

HOST = "127.0.0.1"  # IP-адрес прокси-сервера
PORT = 8080        # Порт прокси-сервера

def send_message(host, port, message):
    """Отправляет сообщение на прокси-сервер."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(message.encode('utf-8'))
        print(f"Сообщение отправлено на прокси: {message}")


if __name__ == "__main__":
    message = '{"Mask": true, "Delete": true, "Filter": false, "Fields_to_hide": ["Email", "Endpoint", "Номер телефона", "Страна", "Регион", "Срок действия карты", "Специальность"]}'
    send_message(HOST, PORT, message)
    time.sleep(10000)