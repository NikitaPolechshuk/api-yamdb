# Models constans
SLUG_REGEX = '^[-a-zA-Z0-9_]+$'
SLUG_ERROR = 'Slug может содержать только буквы, цифры, дефисы и подчеркивания'

CATEGORY_NAME_MAX_LENGTH = 256
CATEGORY_SLUG_MAX_LENGTH = 50

GENRE_NAME_MAX_LENGTH = 256
GENRE_SLUG_MAX_LENGTH = 50

TITLE_NAME_MAX_LENGTH = 256

REVIEW_SCORE_MIN = 1
REVIEW_SCORE_MAX = 10

# Serializer constants
USER_USERNAME_OCCUPIED_ERROR = 'Пользователь с таким username уже существует'
USER_EMAIL_OCCUPIED_ERROR = 'Пользователь с таким email уже существует'
USER_USERNAME_ME_ERROR = "Имя пользователя 'me' недопустимо."
USER_NOT_FOUND_ERROR = 'Пользователь не найден'
USER_WRONG_CONFIRMATION_CODE_ERROR = 'Неверный код подтверждения'

CATEGORY_EMPTY_NAME_ERROR = 'Название категории не может быть пустым'
CATEGORY_EMPTY_SLUG_ERROR = 'Slug категории не может быть пустым'

TITLE_PATCH_VALIDATION_ERROR = 'Не указаны данные для обновления'
TITLE_EMPTY_NAME_ERROR = 'Название произведения не может быть пустым'
TITLE_GENRE_REQUIRED_ERROR = ('Произведение должно принадлежать '
                              'хотя бы к одному жанру')
TITLE_YEAR_CANNOT_BE_EMPTY_ERROR = 'Год выпуска обязателен'
TITLE_YEAR_CANNOT_BE_GT_CURRENT_ERROR = ('Год выпуска не может быть '
                                         'больше текущего')

REVIEW_SCORE_VALIDATION_ERROR = 'Оценка должна быть от 1 до 10'
REVIEW_ALREADY_EXISTS_ERROR = 'Вы уже оставили отзыв на это произведение'
