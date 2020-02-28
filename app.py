from flask import Flask, request, Response
from settings import TOKEN
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.messages import TextMessage
import random
import datetime
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

bot_configuration = BotConfiguration(
    name='LearnEnglishBot',
    avatar='http://viber.com/avatar.jpg',
    auth_token=TOKEN
)
viber = Api(bot_configuration)
app = Flask(__name__)

user_word = {}  # словарь соответсвий между пользователем и текущим словом
# DATABASE_URI = "postgres+psycopg2://postgres:postgres@localhost:5432/my_database"
# DATABASE_URL = 'sqlite:///example.db'
engine = create_engine(
    "postgres://irgxsiuwihwbuu:0644f4fbe12aa7051efefb7e04f0d8ce485ed600c0ddc57c4c31b20819f07178@ec2-54-75-231-215.eu-west-1.compute.amazonaws.com:5432/dfd2em5rqfdsv7")

Base = declarative_base()

Session = sessionmaker(engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, default='John Doe')
    viber_id = Column(String, nullable=False, unique=True)
    last_time_visit = Column(DateTime)

    words = relationship("Learning", back_populates='user')

    def __repr__(self):
        return f'{self.id}: {self.name}[{self.viber_id}]'


class Learning(Base):
    __tablename__ = 'learning'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    word = Column(String, nullable=False)
    right_answer = Column(Integer, nullable=False, default=0)
    last_time_answer = Column(DateTime)

    user = relationship("User", back_populates='words')

    def __pepr__(self):
        return f'{self.id}: {self.user_id}[{self.word} / {self.right_answer}]'


def CreateStartInfo(round):
    """
    создание информационного сообщения для пользователя
    :param user: пользователь, для которого создается сообщение
    :return: информационное сообщение
    """
    # db = MyDataBase('database.db')
    # получение необходимых данных из БД
    session = Session()
    user_id = session.query(User.id).filter(User.viber_id == round.viber_id)
    count_words = session.query(Learning).filter(Learning.user_id == user_id).filter(Learning.right_answer > 0).count()
    date_last_round = session.query(User.last_time_visit).filter(User.viber_id == round.viber_id).first()
    HELLO_MESSAGE = "Бот предназначен для заучивания иностранных слов.\n" \
                    "Для начала нажмите или напишите  'Старт'" \
                    f"\n Вы уже выучили {count_words} из 50" \
                    f"\n Последняя дата опроса: {date_last_round}"

    return HELLO_MESSAGE


# стартовая клавиатура
START_KEYBOARD = {
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
            "ActionBody": "Информация",
            "ReplyType": "message",
            "Text": "Информация"
        }
    ]
}


def CreateKeyboard(round):
    """
    создание клавиатуры для отправки перевода слова
    :param user: пользователь, для которого создается клавиатура
    :return: клавиатура
    """
    # получение необходимых данных из БД
    session = Session()
    translation = []
    translation.append(round.word["translation"])
    while len(translation) != 4:
        n = random.choice(data)["translation"]
        if n not in translation:
            translation.append(n)
    random.shuffle(translation)
    # создание клавиатуры
    KEYBOARD = {
        "Type": "keyboard",
        "Buttons": [
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#e6f5ff",
                "BgMedia": "http://link.to.button.image",
                "BgMediaType": "picture",
                "BgLoop": True,
                "ActionType": "reply",
                "ActionBody": f"{translation[0]}",
                "ReplyType": "message",
                "Text": f"{translation[0]}"
            },
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#e6f5ff",
                "BgMedia": "http://link.to.button.image",
                "BgMediaType": "picture",
                "BgLoop": True,
                "ActionType": "reply",
                "ActionBody": f"{translation[1]}",
                "ReplyType": "message",
                "Text": f"{translation[1]}"
            },
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#e6f5ff",
                "BgMedia": "http://link.to.button.image",
                "BgMediaType": "picture",
                "BgLoop": True,
                "ActionType": "reply",
                "ActionBody": f"{translation[2]}",
                "ReplyType": "message",
                "Text": f"{translation[2]}"
            },
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#e6f5ff",
                "BgMedia": "http://link.to.button.image",
                "BgMediaType": "picture",
                "BgLoop": True,
                "ActionType": "reply",
                "ActionBody": f"{translation[3]}",
                "ReplyType": "message",
                "Text": f"{translation[3]}"
            },
            {
                "Columns": 6,
                "Rows": 1,
                "BgColor": "#e6f5ff",
                "BgMedia": "http://link.to.button.image",
                "BgMediaType": "picture",
                "BgLoop": True,
                "ActionType": "reply",
                "ActionBody": "Пример использования",
                "ReplyType": "message",
                "Text": "Пример использования"
            }
        ]
    }
    return KEYBOARD


with open('english_words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


def choose_word(round):
    """
    выбор предлагаемого слова пользователю
    :param user: пользователь, для которого выбирается слово
    :return: выбранное слово
    """
    session = Session()
    round.word = data[random.choice(range(50))]
    user_id = session.query(User.id).filter(User.viber_id == round.viber_id)
    query = session.query(Learning).filter(Learning.user_id == user_id).filter(Learning.word == round.word["word"])
    learning = query.all()
    if len(learning) == 0:
        session.add(Learning(user_id=user_id, word=round.word["word"]))
        session.commit()
    else:
        right_answer = session.query(Learning.right_answer).filter(Learning.user_id == user_id).filter(
            Learning.word == round.word["word"]).first()
        if right_answer >= 20:
            choose_word(round)


# получение текущего слова пользователя по его id
def get_round(user_id):
    return user_round[user_id]


def send_message(round, correct):
    """
    отправка вопроса пользователю и
    :param user: пользователь, которому отправляется вопрос
    :param correct: правильность введенного перевода слова
    """
    session = Session()
    # отправка сообщения о правильности введенного перевода слова
    if correct is not None:
        viber.send_messages(round.viber_id, TextMessage(text=correct))
    # отправка вопроса о переводе слова
    if round.count_answers < 10:
        choose_word(round)
        bot_response = TextMessage(text=f"{round.count_answers + 1}. Как переводится слово {round.word['word']}",
                                   keyboard=CreateKeyboard(round), tracking_data='tracking_data')
        viber.send_messages(round.viber_id, [bot_response])
    # отправка о результате раунда
    else:
        bot_response = TextMessage(text=f"{round.correct_count} верных из {round.count_answers} заданных",
                                   keyboard=START_KEYBOARD,
                                   tracking_data='tracking_data')
        viber.send_messages(round.viber_id, [bot_response])


def get_answer(text, round):
    """
    получение ответа от пользователя
    :param text: полученное сообщение
    :param user: пользователь, от которого получили сообщение
    """
    session = Session()
    correct = 'Неверно'
    if text == round.word["translation"]:
        round.correct_count += 1
        user_id = session.query(User.id).filter(User.viber_id == round.viber_id)
        learning = session.query(Learning).filter(Learning.user_id == user_id).filter(
            Learning.word == round.word["word"]).first()
        learning.right_answer += 1
        session.commit()
        correct = 'Верно'
    round.count_answers += 1
    # отправка следующего сообщения пользователю
    send_message(round, correct)


def send_example(round):
    """
    отправка примера использования
    :param user: пользователь, которому нужно отправить пример
    """
    session = Session()
    # отправка примера использования пользователю
    number = random.choice(range(len(round.word["examples"])))
    bot_response = TextMessage(text=f'{round.word["examples"][number]}',
                               keyboard=CreateKeyboard(round), tracking_data='tracking_data')
    viber.send_messages(round.viber_id, [bot_response])


@app.route("/")
def hello():
    Base.metadata.create_all(engine)
    global count
    count += 1
    return f"hello {count}"


i = 0


class Round:
    def __init__(self, viber_id):
        self.viber_id = viber_id
        self.word = {}
        self.count_answers = 0
        self.correct_count = 0


user_round = {}


@app.route("/incoming", methods=['POST'])
def incoming():
    # Base.metadata.create_all(engine)
    session = Session()
    viber_request = viber.parse_request(request.get_data())
    # отправка приветственного сообщения и стартовой клавиатуры
    if isinstance(viber_request, ViberConversationStartedRequest):
        viber_user = viber_request.user.id
        if len(session.query(User).filter(User.viber_id == viber_user).all()) == 0:
            add_user = User(name=viber_request.user.name, viber_id=viber_user,
                            last_time_visit=datetime.datetime.utcnow())
            session.add(add_user)
            session.commit()
        new_round = Round(viber_user)
        user_round[viber_user] = new_round
        viber.send_messages(viber_user, [
            TextMessage(text=CreateStartInfo(session.query(User).filter(User.viber_id == viber_user).first()),
                        keyboard=START_KEYBOARD,
                        tracking_data='tracking_data')])
    if isinstance(viber_request, ViberMessageRequest):
        user = session.query(User).filter(User.viber_id == viber_request.sender.id).first()
        round = get_round(user.viber_id)
        message = viber_request.message
        if isinstance(message, TextMessage):
            # получаем сообщение от пользователя
            text = message.text
            if text == 'Старт':
                user.last_time_visit = datetime.datetime.utcnow()
                session.commit()
                round.correct_count = 0
                round.count_answers = 0
                send_message(round, None)
            elif text == "Информация":
                viber.send_messages(user.viber_id, [
                    TextMessage(
                        text=CreateStartInfo(session.query(User).filter(User.viber_id == user.viber_id).first()),
                        keyboard=START_KEYBOARD,
                        tracking_data='tracking_data')])
            elif text == 'Пример использования':
                send_example(round)
            else:
                get_answer(text, round)
    return Response(status=200)


if __name__ == "__main__":
    # Base.metadata.create_all(engine)
    app.run(host="127.0.0.1", port=80)
    # session = Session()
    # users = session.query(User)
    # format = "%Y-%m-%d %H:%M:%S.%f"
    # for u in users:
    #     print(u)
    # utc = tz.UTC
    # d = datetime.datetime.now()
    # print(d)
    # current_tz = tz.gettz()
    # print(d.astimezone((current_tz)))
    # db = MyDataBase('database.db')
    # users = db.get_all_users()
    # format = "%Y-%m-%d %H:%M:%S.%f"
    # for u in users:
    #     round = db.get_last_round(u["id"])
    #     print(u)
    #     user_reminder[u] = datetime.datetime(2020, 2, 27, 10, 53)
    #     d = datetime.datetime.strptime(round[0]["time_round"], format)
    #     if (datetime.datetime.now() - d >= datetime.timedelta(minutes=10)):
    #         if ((u not in user_reminder) or (
    #                 datetime.datetime.now() - user_reminder[u] >= datetime.timedelta(minutes=5))):
    #             user_reminder[u] = datetime.datetime.now()
    #             print("jkdv")

    #     # # db.add_words()
    # word = db.get_word((random.choice(range(50))))
    # print(word[0]["word"])
    #
    # # db.add_round(1, datetime.datetime.now())
    # # db.add_round(1, datetime.datetime.now())
    # # db.change_count_answer(1, 5)
    # # r = db.get_last_round(db.find_users('eXQrDJeQ+LhhwwwqSoAaiQ==')[0]["id"])
    # user = db.find_user('eXQrDJeQ+LhhwwwqSoAaiQ==')
    # print(db.get_count_learn_words(user[0]["id"])["count"])
    # # user_word[user[0]["id"]] = word[0]["id"]
    # # print(user_word)
    # # print(get_current_word(user[0]["id"]))
    # round = db.get_last_round(user[0]["id"])
    # date_last_round = round[0]["time_round"]
    # print(date_last_round)
    # print(date_last_round.split(" ")[0])
    # db.close()

    # d = {1:2, 2:5}
    # d[2] = 10
    # d[3] = 11
    # print(d)

    # format = ('%d.%m.%Y')
    # s = datetime.datetime.now().strftime(format)
    # print(s)
    # print(datetime.datetime.now().month)
    # users = db.get_all_users()
    # format = "%Y-%m-%d %H:%M:%S.%f"
    # for u in users:
    #     round = db.get_last_round(u["id"])
    #     # print(round)
    #     # print(round[0]["time_round"])
    #     # print(type(round[0]["time_round"]))
    #     d = datetime.datetime.strptime(round[0]["time_round"], format)
    #     # print(type(d))
    #     if datetime.datetime.now() - d > datetime.timedelta(hours=1):
    #         print("kjf")
