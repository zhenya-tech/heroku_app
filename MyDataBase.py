import sqlite3
import json
import os
import psycopg2

# DATABASE_URL = os.environ['DATABASE_URL']


class MyDataBase:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        with open('create_schema.sql', 'rt') as f:
            query = f.read()
            cursor.executescript(query)
        self.conn.commit()
        cursor.close()

    def close(self):
        self.conn.close()

    def add_words(self):
        with open('english_words.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for elem in data:
            query = """
                INSERT INTO words(word, translation, examples)
                VALUES (?, ?, ?)
            """
            try:
                self.conn.execute(query, (elem["word"], elem["translation"], " ".join(elem["examples"])))
                self.conn.commit()
            except:
                self.conn.rollback()

    def add_user(self, name, viber_id):
        query = """
                INSERT INTO users(name, viber_id)
                VALUES (?, ?)
                """
        try:
            self.conn.execute(query, (name, viber_id))
            self.conn.commit()
        except:
            self.conn.rollback()

    def add_learning(self, user_id, word_id, time):
        query = """
                INSERT INTO learning(user_id, word_id, time_last_answer)
                VALUES (?, ?, ?)
                """
        try:
            self.conn.execute(query, (user_id, word_id, time))
            self.conn.commit()
        except:
            self.conn.rollback()

    def add_round(self, user_id, time):
        query = """
                    INSERT INTO round (user_id, count_answers, correct_count, time_round)
                    VALUES (?, 0, 0, ?)
                """
        try:
            self.conn.execute(query, (user_id, time))
            self.conn.commit()
        except:
            self.conn.rollback()

    def get_last_round(self, user_id):
        query = """
                    SELECT * 
                    FROM round
                    WHERE user_id = ? and id = (
                                                  SELECT MAX(id)
                                                  FROM round
                                                  WHERE user_id = ?
                                                )
                    """
        ret_value = self.conn.execute(query, (user_id, user_id)).fetchall()
        # print(len(ret_value))
        # print(ret_value[0]["id"])
        return ret_value

    def change_right_answer(self, user_id, word_id):
        query = """
                UPDATE learning
                    SET right_answer = right_answer + 1
                    WHERE user_id = ? and word_id = ?
                """
        try:
            self.conn.execute(query, (user_id, word_id))
            self.conn.commit()
        except:
            self.conn.rollback()

    def change_count_answer(self, user_id, round_id):
        query = """
                   UPDATE round
                       SET count_answers = count_answers + 1
                       WHERE user_id = ? and id = ?
                   """
        try:
            self.conn.execute(query, (user_id, round_id))
            self.conn.commit()
        except:
            self.conn.rollback()

    def change_correct_count(self, user_id, round_id):
        query = """
                   UPDATE round
                       SET correct_count = correct_count + 1
                       WHERE user_id = ? and id = ?
                   """
        try:
            self.conn.execute(query, (user_id, round_id))
            self.conn.commit()
        except:
            self.conn.rollback()

    def change_time_last_answer(self, user_id, word_id, time):
        query = """
                   UPDATE learning
                       SET time_last_answer = ?
                       WHERE user_id = ? and word_id = ?
                   """
        try:
            self.conn.execute(query, (time, user_id, word_id))
            self.conn.commit()
        except:
            self.conn.rollback()

    def find_user(self, viber_id):
        query = """
                SELECT * 
                FROM users
                WHERE viber_id = ?
                """
        ret_value = self.conn.execute(query, (viber_id,)).fetchall()
        # print(len(ret_value))
        # print(ret_value)
        return ret_value

    def get_all_users(self):
        query = """
                SELECT * 
                FROM users
                """
        ret_value = self.conn.execute(query).fetchall()
        return ret_value

    def get_word(self, id):
        query = """
                SELECT * 
                FROM words
                WHERE id = ?
                """
        ret_value = self.conn.execute(query, (id,)).fetchall()
        # print(len(ret_value))
        # print(ret_value)
        return ret_value

    def find_learning(self, user_id, word_id):
        query = """
                SELECT * 
                FROM learning
                WHERE user_id = ? and word_id = ?
                """
        ret_value = self.conn.execute(query, (user_id, word_id)).fetchall()
        # print(len(ret_value))
        # print(ret_value)
        return ret_value

    def get_count_learn_words(self, user_id):
        query = """
                        SELECT COUNT(*) as count
                        FROM learning
                        WHERE user_id = ? and right_answer > 20
                        """
        ret_value = self.conn.execute(query, (user_id,)).fetchone()
        # print(len(ret_value))
        print(ret_value)
        return ret_value


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime

DATABASE_URI = "postgres+psycopg2://postgres:postgres@localhost:5432/my_database"

engine = create_engine(DATABASE_URI)

Base = declarative_base()

Session = sessionmaker(engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, default='John Doe')
    viber_id = Column(String, nullable=False, unique=True)
    last_time_visit = Column(DateTime,
                             nullalable=False,
                             default=datetime.datetime.utcnow())

    words = relationship("Learning", back_populates='user')

    def __repr__(self):
        return f'{self.id}: {self.name}[{self.viber_id}]'


class Learning(Base):
    __tablename__ = 'learning'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    word = Column(String, nullable=False)
    right_answer = Column(Integer, nullable=False, default=0)
    last_time_answer = Column(DateTime, nullalable=False, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates='words')

    def __pepr__(self):
        return f'{self.id}: {self.user_id}[{self.word} / {self.right_answer}]'
