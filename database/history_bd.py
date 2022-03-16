import sqlite3
from loguru import logger
from datetime import datetime


@logger.catch
def create_history_bd(user_id: int) -> None:
    """ Фунцкия, которая создаёт БД с историей посика пользователя"""

    connect = sqlite3.connect(r'database/bot_database.bd')
    cursor = connect.cursor()
    try:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS history_{user_id}(command TEXT,"
                       "date_time DATETIME,"
                       "hotels TEXT")
        logger.info(f'Table history_{user_id} created.')
    except sqlite3.OperationalError:
        pass
    finally:
        connect.commit()


@logger.catch
def set_history_info(command: str, date_time: datetime, hotels: str, user_id: int) -> None:
    """
    Функция, которая записывает параметры в таблицу history
    :param command: команда пользователя
    :param date_time: дата и время команды
    :param hotels: найденные отели
    :param user_id: id пользователя
    """

    connect = sqlite3.connect(r'database/bot_database.bd')
    cursor = connect.cursor()
    cursor.execute(f"UPDATE history_{user_id}(command, date_time, hotels) VALUES(?, ?, ?)",
                   (command, date_time, hotels))
    connect.commit()
    logger.info(f'Table history_{user_id} updated.')


@logger.catch
def get_history_info(user_id: int) -> list or None:
    """Функция, которая возвращает данные пользователя"""

    connect = sqlite3.connect(r'database/bot_database.bd')
    cursor = connect.cursor()
    try:
        cursor.execute(f"SELECT * FROM history_{user_id} WHERE user_id {user_id}")
        value = cursor.fetchone()
        return value
    except sqlite3.OperationalError:
        pass


@logger.catch
def clear_history_bd(user_id: int) -> None:
    """Функция, которая удаляет данные о пользователе """

    connect = sqlite3.connect(r'database/bot_database.bd')
    cursor = connect.cursor()
    cursor.execute(f"DELETE FROM history_{user_id} WHERE user_id={user_id}")
    connect.commit()
