import requests
import csv

from environs import Env
from datetime import datetime
from pathlib import Path


class CheckConnection:
    def __init__(self):
        secret = Env()
        secret.read_env()
        self.token = secret.str("TOKEN_BOT")
        self.chat_id = secret.str("CHAT_ID")
        self.now = datetime.now()
        self.file_name = "historial_{}.csv".format(self.now.strftime("%d-%B-%Y"))

    def test_connection(self):
        url_to_check = "http://google.com/"
        date_time = "{}".format(self.now.strftime("%d %B %Y - %H:%M:%S"))

        try:
            response = requests.get(url_to_check)
            if response.status_code == 200:
                self.read_log()
        except requests.exceptions.ConnectionError as err:
            message_err = "{} - Error de comunicación al exterior|waiting\n".format(date_time)
            self.write_log(message_err)
            print(err)

    def send_message(self, message):
        send_text = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}".format(
            self.token,
            self.chat_id,
            message,
        )
        response = requests.post(send_text)
        return response

    def clean_file(self):
        file = open(self.file_name, "r+")
        file.truncate(0)
        file.close()

    def write_log(self, message):
        with open(self.file_name, "a", encoding="utf8") as file:
            file.write(message)
            file.close()

    def read_log(self):

        try:
            file_exists = Path("./{}".format(self.file_name))
            if file_exists.exists:
                updated_lines = []
                with open(self.file_name, "r", encoding="utf8") as file:
                    csv_reader = csv.reader(file, delimiter="|")
                    for row in csv_reader:
                        if row[1] == "waiting":
                            self.send_message(row[0])
                            updated_lines.append("{}|notified\n".format(row[0]))
                self.clean_file()

                for updated_item in updated_lines:
                    self.write_log(updated_item)
            else:
                open(self.file_name, "w").close()
        except ValueError as err:
            print(err)


if __name__ == "__main__":
    run = CheckConnection()
    run.test_connection()
