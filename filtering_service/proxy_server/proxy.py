import socket
import json
import multiprocessing
from functools import partial
import re
import time
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # Импортируем Flask-CORS

number_of_cores = 12
ENDPOINT = "http://127.0.0.1:8000/api/admin-panel/upload-user-data/"
STATUS = False
app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов и методов


class Proxy:
    def __init__(self, backend_endpoint):
        self.backend_endpoint = backend_endpoint

    def process_message(self, message):
        message = json.loads(message)
        fields_to_hide_filter = message["filter"]
        fields_to_hide_delete = message["delete"]
        fields_to_hide_mask = message["mask"]

        if "Логин" in fields_to_hide_filter:
            fields_to_hide_filter.append("Login")

        elif "Логин" in fields_to_hide_delete:
            fields_to_hide_delete.append("Login")

        elif "Логин" in fields_to_hide_mask:
            fields_to_hide_mask.append("Login")

        lines = self.read_file()
        dictionaries = self.create_dictionaries(lines)
        if len(fields_to_hide_filter) > 0:
            dictionaries = self.filter_message(dictionaries, fields_to_hide_filter)
        if len(fields_to_hide_delete) > 0:
            dictionaries = self.delete_message(dictionaries, fields_to_hide_delete)
        if len(fields_to_hide_mask) > 0:
            dictionaries = self.mask_message(dictionaries, fields_to_hide_mask)

        result = self.create_json(dictionaries)

        result = list("[\n" + ",\n".join(i) + "\n]" for i in result)
        return result

    def send_to_back(self, messages, user, endpoint):
        """
        Отправляет обработанное сообщение на бек
        """
        STATUS = False
        counter = 1
        try:
            url = "http://127.0.0.1:8000/api/admin-panel/upload-user-data/"
            for message in messages:

                headers = {
                    "X-UserEmail": user,
                    "X-Num-Of-Packet": f"{counter}",
                    "Content-Type": "application/json",
                    "X-Proxy-Auth": "V%U<UwFo[#V/,l<$9plp]KE[6@=tU^pDdP|<2<G<C;V/{=Til9~!L|Gs2i*4",
                }
                counter += 1
                response = requests.post(
                    url, data=message.encode("utf-8"), headers=headers
                )
                if response.status_code == 201:
                    print(f"Запрос успешно отправлен на {url}")
                else:
                    print(
                        f"Ошибка при отправке запроса: {response.status_code}, {response.text}"
                    )
                if STATUS == True:
                    break

        except Exception as e:
            print(f"Ошибка при отправке запроса на бекенд: {e}")

    def read_file(self):
        with open("data_3.log", "r", encoding="utf-8") as file:
            lines = file.readlines()
            lines = list(i.strip("\n") for i in lines)
            return lines

    def add_key(self, new_message):
        return "" + new_message

    def create_dictionaries(self, lines):
        return parallel_load_json(lines)

    def create_json(self, dictionaries):
        with multiprocessing.Pool(processes=number_of_cores) as pool:
            # Создаем частичную функцию для json.dumps
            new_dictionaries = list()
            lst = list()
            counter = 0
            for i in dictionaries:
                lst.append(i)
                counter += 1
                if counter % 5000 == 0:
                    new_dictionaries.append(lst.copy())
                    lst.clear()
            if len(lst) > 0:
                new_dictionaries.append(lst)
            dump_with_options = partial(json.dumps, ensure_ascii=False)
            result = list()
            for i in new_dictionaries:
                result.append(list(pool.map(dump_with_options, i)))
        return result

    def filter_message(self, dictionaries, fields_to_hide):
        list_to_del = list()
        index = 0
        for i in dictionaries:
            for j in fields_to_hide:
                if j in i:
                    list_to_del.append(index)
                    break
            index += 1

        list_to_del = list_to_del[::-1]
        for i in list_to_del:
            dictionaries.pop(i)

        list_to_del.clear()
        index = 0

        for i in dictionaries:
            if self.replace_data_filter(i["Message"], fields_to_hide) == True:
                list_to_del.append(index)
            index += 1
        list_to_del = list_to_del[::-1]
        for i in list_to_del:
            dictionaries.pop(i)
        return dictionaries

    def delete_message(self, dictionaries, fields_to_hide):
        for i in dictionaries:
            for j in fields_to_hide:
                if j in i:
                    del i[j]
        for i in dictionaries:
            i["Message"] = self.replace_data_delete(i["Message"], fields_to_hide)
        return dictionaries

    def mask_message(self, dictionaries, fields_to_hide):
        for i in dictionaries:
            for j in fields_to_hide:
                if j in i:
                    i[j] = "*"
        for i in dictionaries:
            i["Message"] = self.replace_data_mask(i["Message"], fields_to_hide)
        return dictionaries

    def replace_data_mask(self, text, personal_data_list):
        result = "|".join(personal_data_list)
        pattern = rf"(({result})\s*(?:\:|\=|\s{{2}})\s*).*?\n"

        def repl(match):
            return (
                match.group(1)
                + "*" * (len(match.group(0)) - len(match.group(1)) - 1)
                + "\n"
            )

        result = re.sub(pattern, repl, text)
        return result

    def replace_data_filter(self, text, personal_data_list):
        result = "|".join(personal_data_list)
        pattern = rf"(({result})\s*(?:\:|\=|\s{{2}})\s*).*?\n"

        match = re.search(pattern, text)
        return match is not None

    def replace_data_delete(self, text, personal_data_list):
        result = "|".join(personal_data_list)
        pattern = rf"(({result})\s*(?:\:|\=|\s{{2}})\s*).*?\n"

        def repl(match):
            return match.group(1) + "\n"

        result = re.sub(pattern, repl, text)
        return result


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


proxy = Proxy(ENDPOINT)


@app.route("/upload", methods=["POST"])
def upload():
    try:
        email = ""
        # Предполагается, что данные приходят в виде JSON или простой строки
        if request.is_json:
            data = request.get_json()
            email = request.headers.get("X-UserEmail")
            message = json.dumps(data, ensure_ascii=False)
        else:
            message = request.get_data(as_text=True)

        print(f"Получено сообщение от frontend: {message}")
        print(email)
        STATUS = True
        # Обработка сообщения
        processed_message = proxy.process_message(message)
        print(processed_message)
        # print(f"Обработанное сообщение: {processed_message}")

        # Отправка на бэкенд
        response = proxy.send_to_back(processed_message, email, ENDPOINT)
        STATUS = False
        if response is None:
            return (
                jsonify(
                    {"status": "error", "message": "Ошибка при отправке на бэкенд"}
                ),
                500,
            )

        # Прокси-сервер будет передавать ответ бэкенда клиенту
        try:
            backend_response = response.json()
        except ValueError:
            backend_response = response.text

        return (
            jsonify(
                {
                    "status": "success" if response.status_code == 201 else "error",
                    "backend_status": response.status_code,
                    "backend_response": backend_response,
                }
            ),
            response.status_code,
        )

    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    # Запуск Flask-сервера
    app.run(host="127.0.0.1", port=8080)
