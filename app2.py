from flask import Flask, request, Response
from settings import TOKEN
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.messages import TextMessage
import random
import datetime
from MyDataBase import MyDataBase

bot_configuration = BotConfiguration(
    name='LearnEnglishBot',
    avatar='http://viber.com/avatar.jpg',
    auth_token=TOKEN
)
viber = Api(bot_configuration)
app = Flask(__name__)

count = 0


@app.route("/")
def func():
    db = MyDataBase('database.db')
    users = db.get_all_users()
    for u in users:
        round = db.get_last_round(u[0]["id"])
        if datetime.datetime.now() - round[0]["time_round"] == datetime.timedelta(minutes=1):
            viber.send_messages("eXQrDJeQ+LhhwwwqSoAaiQ==", [TextMessage(text="Повтори слова")])
    global count
    count += 1
    return f"hello {count}"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80)
