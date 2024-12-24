## Передумови

- Docker має бути встановлений на вашій машині.
- Для роботи потрібен Docker Compose. Якщо він не встановлений, дотримуйтесь інструкцій по встановленню [тут](https://docs.docker.com/compose/install/).

## Кроки для запуску проекту

### 1. Клонуйте репозиторій

Якщо ви ще не клонували репозиторій, зробіть це за допомогою Git:

```bash
git clone https://github.com/Tarasgr7/part_of_ex-main.git
cd vpn_servise
```
## 2. Створення та активація віртуального середовища (необов'язково)

Використання віртуального середовища Python є рекомендованою практикою для ізоляції залежностей вашого проєкту. Це запобігає конфліктам між різними проєктами та забезпечує відтворюваність середовища. (Не обов'язково для Docker, оскільки Docker сам по собі забезпечує ізоляцію).

### Створення віртуального середовища

Для створення віртуального середовища використовуйте наступну команду в терміналі:

```bash
python -m venv .venv
source .venv/bin/activate  # Для Linux/macOS
.venv\Scripts\activate     # Для Windows
```
## 3. Запуск Docker контейнера

Для запуску Docker контейнера з використанням `docker compose` вам знадобиться файл `docker-compose.yml`, який описує конфігурацію вашого застосунку, включаючи залежності, мережі та томи.

### Команда запуску

У кореневій папці проекту, де знаходиться файл `docker-compose.yml`, виконайте наступну команду в терміналі:

```bash
docker compose up --build
```

## 4. Виконання міграцій (для бази даних)

Для налаштування бази даних та створення необхідних таблиць у вашому Docker-контейнері, особливо якщо ви використовуєте Django або інший фреймворк з підтримкою міграцій, використовується команда `docker compose exec`.

### Команда виконання міграцій

Для запуску міграцій всередині контейнера виконайте наступну команду в терміналі, знаходячись у кореневій папці проекту з файлом `docker-compose.yml`:

```bash
docker compose exec web python manage.py migrate
```

## 5. Створення суперкористувача (необов'язково)

Створення суперкористувача (адміністратора) необхідне для отримання повного доступу до функціоналу вашого веб-застосунку, особливо якщо ви використовуєте Django або інші фреймворки, що передбачають таку роль.

### Команда створення суперкористувача

Для створення суперкористувача всередині Docker-контейнера виконайте наступну команду в терміналі, перебуваючи в кореневій папці проекту з файлом `docker-compose.yml`:

```bash
docker compose exec web python manage.py createsuperuser
```

## 6. Перевірка запуску

Після успішного запуску Docker-контейнера за допомогою `docker compose up` необхідно перевірити, чи веб-застосунок працює коректно.

### Перевірка веб-сторінки

1.  **Відкрийте браузер:** Запустіть ваш веб-браузер (Chrome, Firefox, Safari, Edge тощо).

2.  **Введіть адресу:** В адресний рядок браузера введіть наступну адресу:

    ```
    http://0.0.0.0:8080
    ```

    *   `0.0.0.1`: Це локальна IP-адреса (localhost), яка вказує на ваш комп'ютер.
    *   `8080`: Це порт, на якому працює ваш веб-застосунок. Цей порт має відповідати порту, який ви експонували в `docker-compose.yml` (наприклад, `ports: - "8080:8000"` означає, що порт 8000 всередині контейнера відображається на порт 8080 на вашому комп'ютері). Якщо ви використовуєте інший порт, введіть відповідний номер порту.

3.  **Перевірте відображення:** Якщо все налаштовано правильно, ви побачите головну сторінку  веб-застосунку.

### Перевірка адміністративної панелі (Django)

Якщо ви використовуєте Django або інший фреймворк з вбудованою адміністративною панеллю, ви можете перевірити її доступність наступним чином:

1.  **Введіть адресу адміністративної панелі:** В адресний рядок браузера введіть адресу адміністративної панелі. Для Django зазвичай це:

    ```
    http://0.0.0.0:8080/admin
    ```

    Знову ж таки, переконайтесь, що порт відповідає вашим налаштуванням.

2.  **Введіть дані суперкористувача:** На сторінці входу в адміністративну панель введіть ім'я користувача та пароль суперкористувача, якого ви створили на попередньому кроці (за допомогою `docker compose exec web python manage.py createsuperuser`).

3.  **Перевірте доступ:** Після успішної авторизації ви повинні побачити інтерфейс адміністративної панелі.

## 7. Зупинка Docker контейнерів

Після завершення роботи з вашим веб-застосунком або для звільнення ресурсів системи необхідно зупинити Docker контейнери. Для цього використовується команда `docker compose down`.

### Команда зупинки

Для зупинки та видалення контейнерів, запущених за допомогою `docker compose up`, виконайте наступну команду в терміналі, перебуваючи в кореневій папці проекту з файлом `docker-compose.yml`:

```bash
docker compose down
```

