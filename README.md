# api_yamdb
Проект YaMDb собирает отзывы пользователей на различные произведения (книги, фильмы, музыку).
API позволяет управлять контентом, отзывами и пользователями.

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
python3 -m venv venv   # Для Linux/Mac
python -m venv venv   # Для Windows
```

```
source venv/bin/activate   # Для Linux/Mac
venv\Scripts\activate.bat   # Для Windows
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate   # Для Linux/Mac
python manage.py migrate   # Для Windows
```

Запустить проект:

```
python3 manage.py runserver   # Для Linux/Mac
python manage.py runserver   # Для Windows   
```

Загрузка тестовых данных (опционально) из CSV файлов:
```
python3 manage.py load_data --path=/custom/path/to/csv/files/   # Для Linux/Mac
python manage.py load_data --path=/custom/path/to/csv/files/   # Для Windows
```
*Путь к csv файлам по умолчанию:* `static/data/`

## 📡 Доступные эндпоинты API

### 🔐 Аутентификация и пользователи
- `POST /api/v1/auth/signup/` - Регистрация нового пользователя  
  *Права доступа: Доступно без токена*
- `POST /api/v1/auth/token/` - Получение JWT-токена  
  *Права доступа: Доступно без токена*
- `GET /api/v1/users/me/` - Получение данных своей учетной записи  
  *Права доступа: Любой авторизованный пользователь*

### 📚 Категории (Categories)
- `GET /api/v1/categories/` - Получение списка всех категорий  
  *Права доступа: Доступно без токена*
- `POST /api/v1/categories/` - Добавление новой категории  
  *Права доступа: Администратор*
- `DELETE /api/v1/categories/{slug}/` - Удаление категории  
  *Права доступа: Администратор*

### 🎭 Жанры (Genres)
- `GET /api/v1/genres/` - Получение списка всех жанров  
  *Права доступа: Доступно без токена*
- `POST /api/v1/genres/` - Добавление жанра  
  *Права доступа: Администратор*
- `DELETE /api/v1/genres/{slug}/` - Удаление жанра  
  *Права доступа: Администратор*

### 🎬 Произведения (Titles)
- `GET /api/v1/titles/` - Получение списка всех произведений  
  *Права доступа: Доступно без токена*
- `POST /api/v1/titles/` - Добавление произведения  
  *Права доступа: Администратор*
- `GET /api/v1/titles/{title_id}/` - Получение информации о произведении  
  *Права доступа: Доступно без токена*
- `PATCH /api/v1/titles/{title_id}/` - Частичное обновление информации  
  *Права доступа: Администратор*
- `DELETE /api/v1/titles/{title_id}/` - Удаление произведения  
  *Права доступа: Администратор*

### ✍️ Отзывы (Reviews)
- `GET /api/v1/titles/{title_id}/reviews/` - Получение списка отзывов  
  *Права доступа: Доступно без токена*
- `POST /api/v1/titles/{title_id}/reviews/` - Добавление отзыва  
  *Права доступа: Аутентифицированные пользователи*
- `GET /api/v1/titles/{title_id}/reviews/{review_id}/` - Получение отзыва по ID  
  *Права доступа: Доступно без токена*
- `PATCH /api/v1/titles/{title_id}/reviews/{review_id}/` - Обновление отзыва  
  *Права доступа: Автор отзыва/Модератор/Администратор*
- `DELETE /api/v1/titles/{title_id}/reviews/{review_id}/` - Удаление отзыва  
  *Права доступа: Автор отзыва/Модератор/Администратор*

### 💬 Комментарии (Comments)
- `GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/` - Получение комментариев  
  *Права доступа: Доступно без токена*
- `POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/` - Добавление комментария  
  *Права доступа: Аутентифицированные пользователи*
- `GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` - Получение комментария  
  *Права доступа: Доступно без токена*
- `PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` - Обновление комментария  
  *Права доступа: Автор комментария/Модератор/Администратор*
- `DELETE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` - Удаление комментария  
  *Права доступа: Автор комментария/Модератор/Администратор*

### 👥 Пользователи (Users)
- `GET /api/v1/users/` - Получение списка всех пользователей  
  *Права доступа: Администратор*
- `POST /api/v1/users/` - Добавление нового пользователя  
  *Права доступа: Администратор*
- `GET /api/v1/users/{username}/` - Получение пользователя по username  
  *Права доступа: Администратор*
- `PATCH /api/v1/users/{username}/` - Изменение данных пользователя  
  *Права доступа: Администратор*
- `DELETE /api/v1/users/{username}/` - Удаление пользователя  
  *Права доступа: Администратор*

# Документация API
Полная документация API доступна по адресу `/redoc/` после запуска проекта.


