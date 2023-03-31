import os
import logging
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (
    SendMessageError,
    HTTPError,
    RequestError,
)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)


TOKENS = {
    'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
    'TELEGRAM_TOKEN': PRACTICUM_TOKEN,
    'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
}


def check_tokens():
    """Проверяет доступность токенов."""
    token_list = []
    for token in TOKENS:
        if globals()[token] is None:
            for i in token:
                token_list = [{i}]
                logging.critical(f'Токены "{token_list}" не найдены')
                sys.exit(1)


def send_message(bot, message):
    """Отправляет сообщения в чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as error:
        logging.error(SendMessageError)
        raise SendMessageError(
            f'При отправке сообщения "{message}" к {TELEGRAM_CHAT_ID} '
            f'произошла ошибка: "{error}"'
        )
    else:
        logger.debug(f'Сообщение "{message}" к {TELEGRAM_CHAT_ID} отправлено')


def get_api_answer(timestamp):
    """Делает запрос к эндпроинту, возвращает ответ api.
    и переводит его в формат json.
    """
    try:
        request_status = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )

        if request_status.status_code != HTTPStatus.OK:
            raise HTTPError(
                f'Эндпоинт "{ENDPOINT}" не доступен'
            )

    except requests.RequestException:
        raise RequestError('Сбой при запросе')

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
