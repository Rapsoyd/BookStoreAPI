from django.contrib import admin
from library.models import Author, Genre, Book, Cart, CartBook


class BookInline(admin.StackedInline):
    model = CartBook
    extra = 5


class CartAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    list_display = ['created', 'total_price', 'paid']


admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Cart, CartAdmin)
