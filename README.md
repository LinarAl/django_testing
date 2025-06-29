# Django testing  
## Структура репозитория:
```
Dev
 └── django_testing
     ├── ya_news
     │   ├── news
     │   │   ├── fixtures/
     │   │   ├── migrations/
     │   │   ├── pytest_tests/   <- Директория с тестами pytest для проекта ya_news
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanews/
     │   ├── manage.py
     │   └── pytest.ini
     ├── ya_note
     │   ├── notes
     │   │   ├── migrations/
     │   │   ├── tests/          <- Директория с тестами unittest для проекта ya_note
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanote/
     │   ├── manage.py
     │   └── pytest.ini
     ├── .gitignore
     ├── README.md
     ├── requirements.txt
     └── structure_test.py
```
## Как запустить проект:
1. Клонировать репозиторий и перейти в него в командной строке:

    ```
    git clone https://github.com/LinarAl/django_testing.git
    ```
    ```
    cd django_testing
    ```

2. Cоздать и активировать виртуальное окружение:

    - Если у вас Linux/macOS
    ```
    python3 -m venv env
    ```
    ```
    source env/bin/activate
    ```
    - Если у вас windows
    ```
    python -m venv env
    ```
    ```
    source env/scripts/activate
    ```
3. Обновить pip и установить зависимости из файла requirements.txt:
    ```
    python -m pip install --upgrade pip
    ```
    ```
    pip install -r requirements.txt
    ```
4. Выполнить миграции:
    ```
    cd ya_news
    ```
    ```
    python manage.py migrate
    ```
    ```
    cd ../ya_note
    ```
     ```
    python manage.py migrate
    ```
5. Запустить проект:
    - находясь в папке ya_note или ya_news:
    ```
    python manage.py runserver
    ```
