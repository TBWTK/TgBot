from sqlalchemy import Column, Integer, String, Boolean, Date, Time, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine('postgresql://postgres:postgres@db:5432/bot')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


# определяем класс модели для таблицы tasks
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    producer = Column(String(50))
    responsible = Column(String(50))
    date = Column(Date)
    time = Column(Time)
    description = Column(String)
    is_created = Column(Boolean)
    is_active = Column(Boolean)


session.close()
