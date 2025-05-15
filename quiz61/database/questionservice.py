from database import get_db
from database.models import *

# дз добавление вопросов
def add_question_db(main_question, v1, v2, correct_answer, level, v3=None, v4=None):
    # Создаем сессию
    with next(get_db()) as db:
        # Создаем объект вопроса
        new_question = Question(main_question=main_question, v1=v1, v2=v2,
                                correct_answer=correct_answer, level=level, v3=v3, v4=v4)
        # Добавляем вопрос
        db.add(new_question)
        # Фиксируем изменения
        db.commit()
        return True
    ...
# дз вывод 20 вопросов данной сложности
def get_20_questions_db(level):
    # Создаем сессию
    with next(get_db()) as db:
        questions = db.query(Question).filter_by(level=level).all()
        questions2 = list(set(questions))
        return questions2[:20]

# получение таблицы лидеров
def get_top5_db(level):
    with next(get_db()) as db:
        top5 = db.query(Rating).filter_by(level=level).order_by(Rating.correct_answers.desc()).all()
        #[[id, user_id, correct_answer, level],[id, user_id, correct_answer, level],[id, user_id, correct_answer, level]....]
        filter_info = [[rating.user_id, rating.correct_answers] for rating in top5]
        #[[user_id, correct_answer],[user_id, correct_answer],,[user_id, correct_answer],,[user_id, correct_answer],]
        return filter_info[:5]



