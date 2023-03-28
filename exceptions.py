class SendMessageError(Exception):
    """Ошибка при отправке сообщения в чат."""

    pass


class HTTPError(Exception):
    """Проверка статуса запроса."""

    pass


class RequestError(Exception):
    """Ошибка запроса."""

    pass
