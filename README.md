# MongoDB aggregator
***
Телеграмм бот, получающий данные и MongoDB на основании запроса
## Функционал:
1. Агрегация информации по запросу

## Установка и использование:
- В файле config.py содержатся переменные для подключения к MongoDB:
**DB_NAME**
**COLLECTION_NAME**
**MONGODB**
- Создайте файл .env, содержащий следующие переменные:
> файл создается в корневой папке проекта
  - в файле указать токен телеграмм бота:\
  **TELEGRAM_TOKEN**=ТОКЕН
- Установить виртуальное окружение и активировать его (при необходимости):
> Установка и активация в корневой папке проекта
```sh
python3 -m venv venv
source venv/bin/activate # for macOS
source venv/Scripts/activate # for Windows
```
- Установить зависимости:
```sh
pip install -r requirements.txt
```
- Запустить проект:
```sh
python3 main.py
```
