from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# формат и название нашей базы данных
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
# вариант postgres
# SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin@localhost/quiz61"
#                            ^ формат     ^ юзер   ^пароль ^хост  ^ название бд
# создаем движок
engine = create_engine(SQLALCHEMY_DATABASE_URI)
# создаем генератор сессий
SessionLocal = sessionmaker(bind=engine)
# создаем класс для наследования в моделях
Base = declarative_base()

# создаем функцию-генератор сессий
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


