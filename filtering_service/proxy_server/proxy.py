import socket
import json
import multiprocessing
from functools import partial
import re
import time
import requests


number_of_cores = 12
ENDPOINT = "http://127.0.0.1:8000/api/admin-panel/upload-user-data/"


class Proxy:
    def __init__(self, frontend_host, frontend_port, backend_host, backend_port):
        self.frontend_host = frontend_host
        self.frontend_port = frontend_port
        self.backend_host = backend_host
        self.backend_port = backend_port

    def start(self):
        """Запускает прокси-сервер."""
        frontend_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        frontend_server.bind((self.frontend_host, self.frontend_port))
        frontend_server.listen()
        print(f"Прокси запущен на {self.frontend_host}:{self.frontend_port}")

        while True:
            client_socket, client_address = frontend_server.accept()
            print(f"Новое подключение от {client_address}")
            self.handle_connection(client_socket)

    def handle_connection(self, client_socket):
        """Обработка подключения клиента."""
        try:
            # Получение сообщения от frontend
            message = client_socket.recv(1024).decode('utf-8')
            print(f"Получено сообщение от frontend: {message}")
            client_socket.close()
            # Обработка сообщения
            processed_message = self.process_message(message)
            print(f"Обработанное сообщение: {processed_message}")

            self.send_to_back(processed_message, ENDPOINT)

        except Exception as e:
            print(f"Ошибка при обработке соединения: {e}")
        finally:
            client_socket.close()

    def process_message(self, message):
        message = message.strip("[").strip("]")
        fields_to_hide = message.split(", ")
        lines = self.read_file()
        
        dictionaries = self.create_dictionaries(lines)
        for i in dictionaries:
            for j in fields_to_hide:
                if j in i:
                    i[j] = "***"        
        # тут будет обработка поля message
        
        for i in dictionaries:
            i["Message"] = self.change_message(i["Message"], fields_to_hide)
        
        result = self.create_json(dictionaries)
        #result = list(json.dumps(i, ensure_ascii=False) for i in dictionaries)
        return "[\n" + ",\n".join(result) + "\n]"

    def send_to_back(self, message, endpoint):
        """
        Отправляет обработанное сообщение на бек
        """
        try:
            time.sleep(1)

            url = "http://127.0.0.1:8000/api/admin-panel/upload-user-data/"
            headers = {
                'Content-Type': 'application/json',
                'X-Proxy-Auth': 'V%U<UwFo[#V/,l<$9plp]KE[6@=tU^pDdP|<2<G<C;V/{=Til9~!L|Gs2i*4'
            }

            response = requests.post(url, data=message.encode('utf-8'), headers=headers)

            if response.status_code == 201:
                print(f"Запрос успешно отправлен на {url}")
            else:
                print(f"Ошибка при отправке запроса: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Ошибка при отправке запроса на бекенд: {e}")

    def read_file(self):
        with open('/Users/denisharitonciksergeevic/filtering_service/filtering_service/proxy_server/data 2.log', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = list(i.strip("\n") for i in lines)
            return lines

    def change_message(self, message, fields_to_hide):
        for i in fields_to_hide:
            if i in ("Фамилия","Имя","Отчество","Пол","Дата рождения"):
                message = self.replace_FIO(message)
            if i in ("Адрес прописки","Страна","Регион","Город","Улица","Номер дома"):
                message = self.replace_Adress(message)
            if i in ("Серия и номер паспорта", "Код подразделения","Кем выдан"):
                message = self.replace_Pasport(message)
            if i in ("Логин","Пароль"):
                message = self.replace_LoginPassword(message)
            if i in ("номер счета","Имя владельца карты","Номер кредитной карты","Срок действия карты"):
                message = self.replace_Card(message)
            if i in ("Специальность","Направление","Учебное заведение","Серия/Номер диплома","Регистрационный номер"):
                message = self.replace_University(message)
                
        return message
    
    def add_key(self, new_message):
        return "" + new_message
    
    def create_dictionaries(self, lines):
        return parallel_load_json(lines)
    
    def create_json(self, dictionaries):
        with multiprocessing.Pool(processes=4) as pool:
            # Создаем частичную функцию для json.dumps
            dump_with_options = partial(json.dumps, ensure_ascii=False) 
            result = pool.map(dump_with_options, dictionaries)
        return result
    
    def replace_data(self, text, pattern):
        def repl(match):
            return match.group(1) + '*' * (len(match.group(0)) - len(match.group(1)) - 1) + '\n'

        result = re.sub(pattern, repl, text)
        return result

    def replace_FIO(self, text):
        pattern = r'((Фамилия|Имя|Отчество|Пол|Дата рождения)\s*(?:\:|\=|\s{2})\s*).*?\n'
        return self.replace_data(text, pattern)

    def replace_Adress(self,text):
        pattern = r'((Адрес прописки|Страна|Регион|Город|Улица|Номер дома)\s*(?:\:|\=|\s{2})\s*).*?\n'
        return self.replace_data(text, pattern)

    def replace_Pasport(self,text):
        pattern = r'((Серия и номер паспорта|Код подразделения|Кем выдан)\s*(?:\:|\=|\s{2})\s*).*?\n'
        return self.replace_data(text, pattern)

    def replace_LoginPassword(self,text):
        pattern = r'((Логин|Пароль)\s*(?:\:|\=|\s{2})\s*).*?\n'
        return self.replace_data(text, pattern)

    def replace_Card(self,text):
        pattern = r'((номер счета|Имя владельца карты|Номер кредитной карты|Срок действия карты)\s*(?:\:|\=|\s{2})\s*).*?\n'
        return self.replace_data(text, pattern)

    def replace_University(self,text):
        pattern = r'((Специальность|Направление|Учебное заведение|Серия/Номер диплома|Регистрационный номер)\s*(?:\:|\=|\s{2})\s*).*?\n'
        return self.replace_data(text, pattern)
    
    #Proxy.change_message() missing 1 required positional argument: 'fields_to_hide'


def parallel_load_json(lines):
    with multiprocessing.Pool(processes=number_of_cores) as pool:
        dictionaries = pool.map(load_json, lines)
        return dictionaries


def load_json(line):
    return json.loads(line)


def create_parallel_json(dictionaries):
    with multiprocessing.Pool(processes=number_of_cores) as pool:
        result = pool.map(load_json, dictionaries)
        return dictionaries


def create_json(dictionary):
    return json.dumps(dictionary, ensure_ascii=False)

    
if __name__ == '__main__':
    proxy = Proxy("127.0.0.1", 8080, "127.0.0.1", 8000) 
    proxy.start()
