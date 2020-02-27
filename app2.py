from settings import TOKEN
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import TextMessage
import datetime
from MyDataBase import MyDataBase
from app import START_KEYBOARD

bot_configuration = BotConfiguration(
    name='LearnEnglishBot',
    avatar='http://viber.com/avatar.jpg',
    auth_token=TOKEN
)
viber = Api(bot_configuration)

# словарь соответсвий пользователя и времени посоеднего напоминания
user_reminder = {}

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    # print('This job is run every three minutes.')
    db = MyDataBase('database.db')
    users = db.get_all_users()
    for u in users:
        round = db.get_last_round(u["id"])
        d = datetime.datetime.strptime(round[0]["time_round"], format)
        if (datetime.datetime.now() - d > datetime.timedelta(hours=1)) and \
                ((u not in user_reminder) or (user_reminder[u] > datetime.timedelta(minutes=10))):
            user_reminder[u] = datetime.datetime.now()
            viber.send_messages(u["id"], [TextMessage(text="Время повторить слова", keyboard=START_KEYBOARD,
                        tracking_data='tracking_data')])

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()

