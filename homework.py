import os
import sys
import time
import logging
from http import HTTPStatus
import requests

import telegram

from dotenv import load_dotenv

from exceptions import (
    SendMessageError,
    HTTPError,
)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# secret_token = os.getenv(TOKEN)

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


chat_id = TELEGRAM_CHAT_ID


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

{
    "homework": [
        {
            "id": 123,
            "status": "approved",
            "homework_name": "username__hw_oop.zip",
            "reviewer_comment": "Всё нравится",
            "date_updated": "2020-02-11T14:40:57Z",
            "lesson_name": "Итоговый проект"
        },
        {
            "id": 124,
            "status": "rejected",
            "homework_name": "username__hw_python_oop.zip",
            "reviewer_comment": "Имеются некоторые замечания",
            "date_updated": "2020-02-13T16:42:47Z",
            "lesson_name": "Итоговый проект"
        },
        {
            "id": 125,
            "status": "reviewed",
            "homework_name": "username__hw_python_oop.zip",
            "reviewer_comment": "Работа проверяется",
            "date_updated": "2020-02-13T16:42:47Z",
            "lesson_name": "Итоговый проект"
        }
    ],
    "current_date": 1581604970
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
handler .setFormatter(formatter)


def check_tokens():
    """Проверяет доступность переменных окружения."""
    if not all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]):
        logging.critical('Токены не были найдены')
        sys.exit()


def send_message(bot, message):
    """Отправляет сообщения в чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug(f'{message}')

    except Exception as error:
        logging.error(SendMessageError)
        raise Exception(
            f'При отправке сообщения "{message}" произошла ошибка: "{error}"'
        )


def get_api_answer(timestamp):
    """Делает запрос к эндпроинту, возвращает ответ api.
    и переводит его в формат json.
    """
    timestamp = int(time.time())

    try:
        request_status = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'form_data': timestamp}
        )

        if request_status.status_code != HTTPStatus.OK:
            raise HTTPError('Эндпоинт не доступен')

    except requests.RequestEcxeption:
        logger.error('Сбой при запросе')

    return request_status.json()


def check_response(response):
    """Проверяет полученные данных на корректность."""
    if (
        not isinstance(response, dict)
        or not isinstance(response.get('homeworks'), list)
    ):
        logger.error(TypeError)
        raise TypeError('Тип данных не соответствует ожидаемому')

    if 'homeworks' not in response:
        logger.error(KeyError)
        raise KeyError('Отсутствует ключ "homeworks"')

    return response.get('homeworks')


def parse_status(homework):
    """Извлекает информацию о статусе работы."""
    homework_status = homework.get('status')
    homework_name = homework.get('homework_name')

    if 'homework_name' not in homework:
        logger.error(TypeError)
        raise TypeError('Отсутствует ключ "homework_name"')

    if homework_status not in HOMEWORK_VERDICTS:
        logger.error(KeyError)
        raise KeyError('Неожиданный статус')

    verdict = HOMEWORK_VERDICTS.get(homework_status)
    return (f'Изменился статус проверки работы "{homework_name}". {verdict}')


# тесты-то пройдены но кажется тут всё ужасно недоработано
def main():
    """Основная логика работы бота."""
    check_tokens()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    send_message(
        bot,
        'Бот начал работу. Каждые 10 минут будет приходить оповещение '
        'о текущем статусе проверки работы'
    )

    while True:
        try:
            timestamp = (0)
            timestamp = int(time.time())
            last_message = ''

            response = get_api_answer(timestamp)
            response_check = check_response(response)

            if not response_check:
                new_message = 'Работа не найдена'
            else:
                new_message = parse_status(response_check[0])

            if last_message != new_message:
                send_message(bot, new_message)

        except Exception as error:
            message = f'Сбой в работе программы. "{error}"'
            send_message(bot, message)

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
