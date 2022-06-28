# Бот помощник с распознаванием речи для VK и Telegram

## Цели проекта

* Сделать бота в Telegram и Вконтакте
* Обучить их нейросетью.
* Создать скрит для загрузки интентов в DialogFlow

> Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

## Пример работы программы
Пример результата для Telegram:

![Пример результата для Telegram](https://dvmn.org/filer/canonical/1569214094/323/)

Пример результата для ВКонтакте:

![Пример результата для ВКонтакте](https://dvmn.org/filer/canonical/1569214089/322/)

## Конфигурации

* Python version: 3.10
* Libraries: requirements.txt

## Запуск

- Скачайте код
- Через консоль в директории с кодом установите виртуальное окружение командой:

```bash
python3 -m venv env
```

- Активируйте виртуальное окружение командой:
```bash
source env/bin/activate
```

- Установите библиотеки командой:
```bash
pip install -r requirements.txt
```
- Создайте [Google-проект](https://cloud.google.com/dialogflow/es/docs/quick/setup), создать [агента в DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/build-agent).

- Запишите переменные окружения в файле `.env` в формате КЛЮЧ=ЗНАЧЕНИЕ

`GOOGLE_APPLICATION_CREDENTIALS` Название файла с JSON-ключом. Как его получить указано в этом [руководстве](https://cloud.google.com/docs/authentication/getting-started). Должен лежать в корне проекта.

`PROJECT_ID` ID Google проекта.

`TELEGRAM_API_TOKEN` Токен Телеграмма. Получить можно у [BotFather](https://telegram.me/BotFather).

`VK_API_TOKEN` API токен группы Вконтакте. Получить можно в настройках группы во вкладке "Работа с API".

- Для Телеграмма запустите скрипт командой:
```bash
python3 tg_helper_bot.py
```
- Для Вконтакте запустите скрипт командой:
```bash
python3 vk_helper_bot.py
```

- Для создания интентов запустите скрипт командой (проверьте расположение интентов в `intents/questions.json`:
```bash
python3 fill_intent.py
```