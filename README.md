# homework_bot
# Описание
Бот-ассистент - Telegram-бота, который обращается к API сервиса Практикум.Домашка и узнаваёт статус вашей домашней работы.

## Стек технологий
- Python
- Telegram API
- Yandex.Praktikum API
- python-telegram-bot
- flake8==3.9.2
- flake8-docstrings==1.6.0
- pytest==6.2.5
- python-dotenv==0.19.0
- python-telegram-bot==13.7
- requests==2.26.0

## Что должен делать бот:
- Раз в 10 минут опрашивать API сервиса Практикум.Домашка и проверять статус отправленной на ревью домашней работы
- При обновлении статуса анализировать ответ API и отправлять вам соответствующее уведомление в Telegram
- Логировать свою работу и сообщать вам о важных проблемах сообщением в Telegram
- Каждое сообщение в журнале логов должно состоять как минимум из даты и времени события, уровня важности события, описания события.

## Функции:
- Функция main(): в ней описана основная логика работы программы. Все остальные функции запускаются из неё. Последовательность действий следующая: сделать запрос к API, проверить ответ. Если есть обновления — получить статус работы из обновления и отправить сообщение в Telegram. Подождать некоторое время и сделать новый запрос.
- Функция check_tokens() проверяет доступность переменных окружения, которые необходимы для работы программы. Если отсутствует хотя бы одна переменная окружения — функция должна вернуть False, иначе — True.
- Функция get_api_answer() делает запрос к единственному эндпоинту API-сервиса. В качестве параметра функция получает временную метку. В случае успешного запроса возвращает ответ API, преобразовав его из формата JSON к типам данных Python.
- Функция check_response() проверяет ответ API на корректность. В качестве параметра функция получает ответ API, приведенный к типам данных Python. Если ответ API соответствует ожиданиям, то функция возвращает список домашних работ (он может быть и пустым), доступный в ответе API по ключу 'homeworks'.
Функция parse_status() извлекает из информации о конкретной домашней работе статус этой работы. В качестве параметра функция получает только один элемент из списка домашних работ. В случае успеха, функция возвращает подготовленную для отправки в Telegram строку, содержащую один из вердиктов словаря HOMEWORK_STATUSES.
- Функция send_message() отправляет сообщение в Telegram чат, определяемый переменной окружения TELEGRAM_CHAT_ID. Принимает на вход два параметра: экземпляр класса Bot и строку с текстом сообщения.

# Запуск проекта

- Клонируйте репозиторий с проектом на свой компьютер
```bash
git clone git@github.com:Xenia387/homework_bot.git
```

```
cd homework_bot
```

- Установите и активируйте виртуальное окружение

```
python3 -m venv env
```

```
source venv/bin/activate
```

  или

```
python -m venv venv
```

```
source venv/Scripts/activate
```

- Установите зависимости из файла requirements.txt
  
```
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

Автор проекта: Анисимова Ксения
- email: anis.xenia@yandex.ru
- telegram: @Ksenia_An_mova
