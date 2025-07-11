import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from reviews.models import (
    Category, Genre, Title, Review, Comment
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Load data from CSV files into database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default='static/data/',
            help='Base path to CSV files'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        base_path = options['path']
        self.load_categories(f'{base_path}category.csv')
        self.load_genres(f'{base_path}genre.csv')
        self.load_users(f'{base_path}users.csv')
        self.load_titles(f'{base_path}titles.csv')
        self.load_genre_title(f'{base_path}genre_title.csv')
        self.load_reviews(f'{base_path}review.csv')
        self.load_comments(f'{base_path}comments.csv')

    def load_categories(self, file_path):
        self.stdout.write(f'Loading categories from {file_path}...')
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Categories loaded'))

    def load_genres(self, file_path):
        self.stdout.write(f'Loading genres from {file_path}...')
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Genres loaded'))

    def load_users(self, file_path):
        self.stdout.write(f'Loading users from {file_path}...')
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                User.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'username': row['username'],
                        'email': row['email'],
                        'role': row['role'],
                        'bio': row['bio'] or '',
                        'first_name': row['first_name'] or '',
                        'last_name': row['last_name'] or ''
                    }
                )
        self.stdout.write(self.style.SUCCESS('Users loaded'))

    def load_titles(self, file_path):
        self.stdout.write(f'Loading titles from {file_path}...')
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                category = Category.objects.get(id=row['category']) if row['category'] else None
                Title.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'year': row['year'],
                        'category': category,
                        'description': row.get('description', '')
                    }
                )
        self.stdout.write(self.style.SUCCESS('Titles loaded'))

    def load_genre_title(self, file_path):
        self.stdout.write(f'Loading genre-title relations from {file_path}...')
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)
        self.stdout.write(self.style.SUCCESS('Genre-Title relations loaded'))
    
    def load_reviews(self, file_path):
        self.stdout.write(f'Loading reviews from {file_path}...')
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                author = User.objects.get(id=row['author'])
                Review.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'title': title,
                        'text': row['text'],
                        'author': author,
                        'score': row['score'],
                        'pub_date': row['pub_date']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Reviews loaded'))

    def load_comments(self, file_path):
        self.stdout.write(f'Loading comments from {file_path}...')
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                review = Review.objects.get(id=row['review_id'])
                author = User.objects.get(id=row['author'])
                Comment.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'review': review,
                        'text': row['text'],
                        'author': author,
                        'pub_date': row['pub_date']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Comments loaded'))
