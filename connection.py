from environs import Env
from datetime import datetime
import requests
import urllib


secret = Env()
secret.read_env()


class CheckConnection:
    def __init__(self) -> None:
        self.token = secret.str("TOKEN_BOT")
        self.chat_id = secret.str("CHAT_ID")

    def send_message(self, message):
        url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}".format(
            self.token,
            self.chat_id,
            message,
        )
        print(url)

    def test_connection(self):
        url_ping = "http://google.com/"
        now = datetime.now()
        date_time = "{}".format(now.strftime("%d %B %Y - %H:%M:%S"))
        print(date_time)

        try:
            urllib.request.urlopen(url_ping, timeout=1)
        except urllib.error.URLError as err:
            print("Sin conexión a internet {}".format(err))


if __name__ == "__main__":
    run = CheckConnection()
    run.test_connection()
