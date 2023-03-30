class SendMessageError(Exception):
    """Ошибка при отправке сообщения в чат."""


class HTTPError(Exception):
    """Проверка статуса запроса."""


class RequestError(Exception):
    """Ошибка запроса."""
