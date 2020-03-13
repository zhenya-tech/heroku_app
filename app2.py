from settings import TOKEN
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import TextMessage
from app import Session, User
import datetime

bot_configuration = BotConfiguration(
    name='LearnEnglishBot',
    avatar='http://viber.com/avatar.jpg',
    auth_token=TOKEN
)
viber = Api(bot_configuration)

# стартовая клавиатура
REMIND_KEYBOARD = {
    "Type": "keyboard",
    "Buttons": [
        {
            "Columns": 6,
            "Rows": 1,
            "BgColor": "#e6f5ff",
            "BgMedia": "http://link.to.button.image",
            "BgMediaType": "picture",
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "Старт",
            "ReplyType": "message",
            "Text": "Старт"
        }, {
            "Columns": 6,
            "Rows": 1,
            "BgColor": "#e6f5ff",
            "BgMedia": "http://link.to.button.image",
            "BgMediaType": "picture",
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "Напомнить  через 30 минут",
            "ReplyType": "message",
            "Text": "Напомнить  через 30 минут"
        }, {
            "Columns": 6,
            "Rows": 1,
            "BgColor": "#e6f5ff",
            "BgMedia": "http://link.to.button.image",
            "BgMediaType": "picture",
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "Информация",
            "ReplyType": "message",
            "Text": "Информация"
        }
    ]
}

# словарь соответсвий пользователя и времени последнего напоминания
user_reminder = {}

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    session = Session()
    users = session.query(User)
    for u in users:
        if datetime.datetime.utcnow() >= u.time_reminder:
            bot_response = TextMessage(text='Время повторить слова',
                                       keyboard=REMIND_KEYBOARD, tracking_data='tracking_data')
            print(u.viber_id)
            viber.send_messages(u.viber_id, 
                            [bot_response])


sched.start()
