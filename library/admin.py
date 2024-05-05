from django.contrib import admin
from library.models import Author, Genre, Book, BookReview


@admin.register(BookReview)
class AdminBookReview(admin.ModelAdmin):
    list_display = ['id', 'book', 'user', 'rating', 'get_comment', 'created_at']

    def get_comment(self, obj):
        max_length = 63
        if len(obj.comment) > max_length:
            return obj.comment[:63] + '...'
        return obj.comment

    get_comment.short_description = 'comment'


admin.site.register(Author)
admin.site.register(Genre)


@admin.register(Book)
class AdminBook(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'get_short_description', 'published', 'price']

    def get_short_description(self, obj):
        max_length = 86
        if len(obj.description) > max_length:
            return obj.description[:86] + '...'
        return obj.description

    get_short_description.short_description = 'description'

