# api_yamdb

# ИНСТРУКЦИЯ ПО УСТАНОВКЕ И ЗАПУСКУ

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/NikitaPolechshuk/api-yamdb
```

```
cd api-yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Загрузка CSV файлов:
```
python3 manage.py load_data --path=/custom/path/to/csv/files/
```
*путь по умолчанию:* **'static/data/'**

### [Полное описание API *.yaml](https://github.com/NikitaPolechshuk/api-yamdb/blob/main/api_yamdb/static/redoc.yaml)


