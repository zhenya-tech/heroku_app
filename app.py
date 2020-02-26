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

user_word = {}  # словарь соответсвий между пользователем и текущим словом


def CreateStartInfo(user):
    """
    создание информационного сообщения для пользователя
    :param user: пользователь, для которого создается сообщение
    :return: информационное сообщение
    """
    db = MyDataBase('database.db')
    # получение необходимых данных из БД
    count_words = db.get_count_learn_words(user[0]["id"])["count"]
    round = db.get_last_round(user[0]["id"])
    HELLO_MESSAGE = "Бот предназначен для заучивания иностранных слов.\n" \
                    "Для начала нажмите или напишите  'Старт'" \
                    f"\n Вы уже выучили {count_words} из 50"
    if len(round) != 0:
        date_last_round = round[0]["time_round"]
        HELLO_MESSAGE += f"\n Последняя дата опроса: {date_last_round.split(' ')[0]}"
    db.close()
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


def CreateKeyboard(user):
    """
    создание клавиатуры для отправки перевода слова
    :param user: пользователь, для которого создается клавиатура
    :return: клавиатура
    """
    db = MyDataBase('database.db')
    # получение необходимых данных из БД
    word_id = get_current_word(user[0]["id"])
    word = db.get_word(word_id)
    # создание списка переводов слов
    translation = []
    translation.append(word[0]["translation"])
    while len(translation) != 4:
        n = db.get_word((random.choice(range(50))))
        if n[0]["translation"] not in translation:
            translation.append(n[0]["translation"])
    random.shuffle(translation)
    print(translation)
    print(word[0]["word"])
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


def choose_word(user):
    """
    выбор предлагаемого слова пользователю
    :param user: пользователь, для которого выбирается слово
    :return: выбранное слово
    """
    db = MyDataBase('database.db')
    word = db.get_word((random.choice(range(50))))
    learning = db.find_learning(user[0]["id"], word[0]["id"])
    if len(learning) == 0:
        db.add_learning(user[0]["id"], word[0]["id"], datetime.datetime.now())
    else:
        right_answer = learning[0]["right_answer"]
        if right_answer >= 20:
            choose_word(user)
    db.close()
    return word


# получение текущего слова пользователя по его id
def get_current_word(user_id):
    return user_word[user_id]


def send_message(user, correct):
    """
    отправка вопроса пользователю и
    :param user: пользователь, которому отправляется вопрос
    :param correct: правильность введенного перевода слова
    """
    db = MyDataBase('database.db')
    # получение необходимых данных из БД
    round = db.get_last_round(user[0]["id"])
    count = round[0]["count_answers"]
    # отправка сообщения о правильности введенного перевода слова
    if correct is not None:
        viber.send_messages(user[0]["viber_id"], TextMessage(text=correct))
    # отправка вопроса о переводе слова
    if count < 10:
        word = choose_word(user)
        user_word[user[0]["id"]] = word[0]["id"]
        print(user_word)
        bot_response = TextMessage(text=f"{count + 1}. Как переводится слово {word[0]['word']}",
                                   keyboard=CreateKeyboard(user), tracking_data='tracking_data')
        viber.send_messages(user[0]["viber_id"], [bot_response])
    # отправка о результате раунда
    else:
        bot_response = TextMessage(text=f"{round[0]['correct_count']} верных из {count} заданных",
                                   keyboard=START_KEYBOARD,
                                   tracking_data='tracking_data')
        viber.send_messages(user[0]["viber_id"], [bot_response])
    db.close()


def get_answer(text, user):
    """
    получение ответа от пользователя
    :param text: полученное сообщение
    :param user: пользователь, от которого получили сообщение
    """
    db = MyDataBase('database.db')
    # получение необходимых данных из БД
    word_id = get_current_word(user[0]["id"])
    word = db.get_word(word_id)
    round = db.get_last_round(user[0]["id"])
    correct = 'Неверно'
    if text == word[0]["translation"]:
        db.change_correct_count(user[0]["id"], round[0]["id"])
        db.change_right_answer(user[0]["id"], word[0]["id"])
        db.change_time_last_answer(user[0]["id"], word[0]["id"], datetime.datetime.now())
        correct = 'Верно'
    db.change_count_answer(user[0]["id"], round[0]["id"])
    # отправка следующего сообщения пользователю
    db.close()
    send_message(user, correct)


def send_example(user):
    """
    отправка примера использования
    :param user: пользователь, которому нужно отправить пример
    """
    db = MyDataBase('database.db')
    # получение необходимых данных из БД
    word_id = get_current_word(user[0]["id"])
    word = db.get_word(word_id)
    examples = word[0]["examples"].split(". ")
    # отправка примера использования пользователю
    number = random.choice(range(len(examples)))
    bot_response = TextMessage(text=f'{examples[number]}',
                               keyboard=CreateKeyboard(user), tracking_data='tracking_data')
    viber.send_messages(user[0]["viber_id"], [bot_response])
    db.close()


@app.route("/")
def hello():
    global count
    count += 1
    return f"hello {count}"


@app.route("/incoming", methods=['POST'])
def incoming():
    db = MyDataBase('database.db')
    viber_request = viber.parse_request(request.get_data())
    # отправка приветственного сообщения и стартовой клавиатуры
    if isinstance(viber_request, ViberConversationStartedRequest):
        viber_user = viber_request.user.id
        if len(db.find_user(viber_user)) == 0:
            db.add_user(viber_request.user.name, viber_user)
        viber.send_messages(viber_user, [
            TextMessage(text=CreateStartInfo(db.find_user(viber_user)), keyboard=START_KEYBOARD,
                        tracking_data='tracking_data')])
    if isinstance(viber_request, ViberMessageRequest):
        user = db.find_user(viber_request.sender.id)
        message = viber_request.message
        if isinstance(message, TextMessage):
            # получаем сообщение от пользователя
            text = message.text
            if text == 'Старт':
                db.add_round(user[0]["id"], datetime.datetime.now())
                send_message(user, None)
            elif text == "Информация":
                viber.send_messages(user[0]["viber_id"], [
                    TextMessage(text=CreateStartInfo(db.find_user(user[0]["viber_id"])), keyboard=START_KEYBOARD,
                                tracking_data='tracking_data')])
            elif text == 'Пример использования':
                send_example(user)
            else:
                get_answer(text, user)
    db.close()
    return Response(status=200)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80)
    # db = MyDataBase('database.db')
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
