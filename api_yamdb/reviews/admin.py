from django.contrib import admin
from django.contrib.auth import get_user_model
from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'first_name',
        'last_name',
        'is_staff',
    )
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')
    list_editable = ('role',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20


class GenreInline(admin.TabularInline):
    model = Title.genre.through
    extra = 1
    verbose_name = 'Жанр'
    verbose_name_plural = 'Жанры'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category',
        'display_genres',
        'description_short',
    )
    list_filter = ('category', 'genre', 'year')
    search_fields = ('name', 'category__name', 'genre__name')
    inlines = (GenreInline,)
    exclude = ('genre',)
    list_per_page = 20

    def display_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])

    display_genres.short_description = 'Жанры'

    def description_short(self, obj):
        return (
            obj.description[:50] + '...'
            if len(obj.description) > 50
            else obj.description
        )

    description_short.short_description = 'Описание'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'score', 'text_short', 'pub_date')
    list_filter = ('score', 'pub_date')
    search_fields = ('text', 'author__username', 'title__name')
    raw_id_fields = ('title', 'author')
    list_per_page = 20

    def text_short(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text

    text_short.short_description = 'Текст отзыва'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text_short', 'pub_date')
    search_fields = ('text', 'author__username', 'review__text')
    raw_id_fields = ('review', 'author')
    list_per_page = 20

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_short.short_description = 'Текст комментария'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
