from sqlalchemy import (Column, String, Integer,
                        DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
# модель юзеров
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    reg_date = Column(DateTime, default=lambda: datetime.now())
# вопросы
class Questions(Base):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True, autoincrement=True)
    main_text = Column(String)
    v1 = Column(String)
    v2 = Column(String)
    v3 = Column(String, nullable=True)
    v4 = Column(String, nullable=True)
    correct_answer = Column(Integer)
    level = Column(String, default="Beginner")

# ответы юзеров
class UserAnswer(Base):
    __tablename__ = "useranswer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    question_id = Column(Integer, ForeignKey("question.id"))
    user_answer = Column(Integer)
    # создание связей
    user_fk = relationship(User, lazy="subquery")
    question_fk = relationship("Questions", lazy="subquery")
# таблица рейтинга
class Rating(Base):
    __tablename__ = "rating"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    correct_answers = Column(Integer, default=0)
    level = Column(String)
    user_fk = relationship(User, lazy="subquery")


