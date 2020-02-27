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

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    # print('This job is run every three minutes.')
    viber.send_messages("eXQrDJeQ+LhhwwwqSoAaiQ==", [TextMessage(text="Повтори слова")])

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()
# app = Flask(__name__)
#
# count = 0
#
#
# @app.route("/")
# def func():
#     # db = MyDataBase('database.db')
#     # users = db.get_all_users()
#     # for u in users:
#     #     round = db.get_last_round(u[0]["id"])
#     if datetime.datetime.now() - datetime.datetime.utcnow() >= datetime.timedelta(minutes=1):
#         viber.send_messages("eXQrDJeQ+LhhwwwqSoAaiQ==", [TextMessage(text="Повтори слова")])
#     global count
#     count += 1
#     return f"hello {count}"
#
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=80)
