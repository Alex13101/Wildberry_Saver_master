## Запуск проекта:

1. Склонировать репозиторий
```git clone https://github.com/McKrei/Wildberry-Saver.git```

2. Создать виртуальное окружение
```python -m venv venv```

3. Активировать виртуальное окружение
```venv\Scripts\activate```

4. Установить зависимости
```pip install -r requirements.txt```

5. создать файл .env и добавить в него переменные окружения
```
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=SECRET_KEY
```

5. Запустить проект
```flask run```
