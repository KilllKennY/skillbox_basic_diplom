import sqlite3
from loguru import logger


@logger.catch
def create_user_bd(user_id: int) -> None:
    """ Функция, которая создаёт БД с информацией о пользователе"""

    connect = sqlite3.connect(r'database/bot_database.bd')
    cursor = connect.cursor()
    try:
        cursor.execute(r"CREATE TABLE IF NOT EXISTS user_info(user_id INTEGER UNIQUE,"
                       "command TEXT,"
                       "city_id INTEGER,"
                       "price_min INTEGER"
                       "price_max INTEGER,"
                       "distance_min INTEGER,"
                       "distance_max INTEGER,"
                       "check_in TEXT, "
                       "check_out TEXT,"
                       "hotels_amount INTEGER,"
                       "photos_amount INTEGER)")
        cursor.execute(f"INSERT INTO user_info(user_id) VALUES({user_id})")
        logger.info('Table "user_info" created.')
    except sqlite3.IntegrityError:
        pass
    finally:
        connect.commit()


@logger.catch
def set_user_info(column: str, value: int or str, user_id: int) -> None:
    """
    Функция, которая записывает данные в таблицу user_info
    :param column: столбец таблицы
    :param value: записываемое значение
    :param user_id: id пользователя
    """

    connect = sqlite3.connect(r'database/bot_database.bd')
    cursor = connect.cursor()
    cursor.execute(f"UPDATE user_info SET {column} = ? WHERE user_id = ?", (value, user_id))
    connect.commit()
    logger.info(f'Column {column} in table user_info updated for user {user_id}')


@logger.catch
def get_user_info(column: str, user_id: int) -> str or int:
    """ Функция возвращает данные пользователя из user_info"""

    connect = sqlite3.connect(r'database/bot_database.bd')
    cursor = connect.cursor()
    cursor.execute(f"SELECT {column} FROM user_info WHERE user_id {user_id}")
    value = cursor.fetchone()
    return value
