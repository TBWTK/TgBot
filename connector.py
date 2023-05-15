from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Task, Base


# создаем объект Engine для управления подключением к базе данных
engine = create_engine('postgresql://postgres:postgres@db:5432/bot')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


class ConnectorCreateTask:
    # Создание задачи: создание поля и добавление продюсера
    @staticmethod
    def create_task_add_producer(username):
        updt = session.query(Task).filter_by(is_created=True, producer=username).first()
        print(updt)
        if updt is None:
            task = Task(producer=username, is_created=True)
            session.add(task)
            session.commit()

# Создание задачи: Добавление ответственного
    @staticmethod
    def create_task_add_responsible(username, responsible):
        updt = session.query(Task).filter_by(is_created=True, producer=username).one()
        updt.responsible = responsible
        session.commit()

# Создание задачи: Добавление даты
    @staticmethod
    def create_task_add_date(username, date):
        updt = session.query(Task).filter_by(is_created=True, producer=username).one()
        updt.date = date
        session.commit()

# Шаг 4: Добавление времени
    @staticmethod
    def create_task_add_time(username, time):
        updt = session.query(Task).filter_by(is_created=True, producer=username).one()
        updt.time = time
        session.commit()

# Шаг 3: Добавление описания задачи
    @staticmethod
    def create_task_add_description(username, description):
        updt = session.query(Task).filter_by(is_created=True, producer=username).one()
        updt.description = description
        updt.is_active = True
        session.commit()

# Финал: Получение созданной задачи
    @staticmethod
    def get_created_task(username):
        updt = session.query(Task).filter_by(is_created=True, producer=username).one()
        updt.is_created = False
        session.commit()
        return updt


class ConnectorNotification:
    # Уведомления и логирование: Получение активных задач
    @staticmethod
    def get_task_active():
        return session.query(Task).filter_by(is_active=True, is_created=False).all()

    @staticmethod
    def check_responsible_in_task(id_task, username):
        updt = session.query(Task).filter_by(id=id_task, responsible=username).first()
        if updt is None:
            return False
        else:
            return True

    @staticmethod
    def update_active_status(id_task):
        updt_task = session.query(Task).filter_by(id=id_task).one()
        updt_task.is_active = False
        session.commit()

    @staticmethod
    def get_task(id_task):
        updt = session.query(Task).filter_by(id=id_task).one()
        return updt


session.close()
