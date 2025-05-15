from database import get_db
from database.models import *

def add_user_db(username, phone_number):
    # первый способ генерации сессий (устаревший)
    db = next(get_db())
    # второй способ генерации сессий
    with next(get_db()) as db:
        user = db.query(User).filter_by(username=username).first()
        if not user:
            user = db.query(User).filter_by(phone_number=phone_number).first()
            # объединение 9 и 11 строчки через 1 запрос
            # user = db.query(User).filter(User.username == username and User.phone_number == phone_number).first()
            if not user:
                user = User(username=username, phone_number=phone_number)
                db.add(user)
                db.commit()
                db.refresh(user)
        return user.id
# получение информации о юзере, либо о всех юзерах
def get_users_info_db(user_id=0):
    with next(get_db()) as db:
        exact_user = db.query(User).all() if user_id == 0 else db.query(User).filter_by(id=user_id).first()
        return exact_user if exact_user else "Юзер не найден"
# функция сохранения ответа + учёт рейтинга
def add_answer_db(user_id, question_id, user_answer=0):
    with next(get_db()) as db:
        exact_question = db.query(Questions).filter_by(id=question_id).first()
        new_answer = UserAnswer(user_id=user_id,
                                question_id=question_id,
                                user_answer=user_answer)
        db.add(new_answer)
        db.commit()
        if exact_question.correct_answer == user_answer:
            exact_rating = db.query(Rating).filter(Rating.user_id == user_id and Rating.level == exact_question.level).first()
            if exact_rating:
                exact_rating.correct_answers += 1
                db.commit()
            else:
                new_rating = Rating(user_id=user_id,
                                    correct_answers=1,
                                    level=exact_rating.level)
                db.add(new_rating)
                db.commit()
            return True
        return False







