# homework_bot
# Описание
Бот-ассистент - Telegram-бота, который обращается к API сервиса Практикум.Домашка и узнаваёт статус вашей домашней работы.

## Стек технологий
- Python3
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

# Запуск проекта

- Клонируйте репозиторий с проектом на свой компьютер
```bash
git clone git@github.com:Xenia387/homework_bot.git
```

- Установите и активируйте виртуальное окружение

```
python3 -m venv env
```

```
source env/bin/activate
```

  или

```
python -m venv env
```

```
source venv/Scripts/activate
```

- Установите зависимости из файла requirements.txt

```bash
pip install -r requirements.txt
```

Автор проекта: Анисимова Ксения
- email: anis.xenia@yandex.ru
- telegram: @Ksenia_An_mova
