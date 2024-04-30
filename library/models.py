from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    GENRE_OPTIONS = (
        ('Action', 'Приключенческий боевик'),
        ('Adventure', 'Приключения'),
        ('Comedy', 'Комедия'),
        ('Crime', 'Криминал'),
        ('Drama', 'Драма'),
        ('Fantasy', 'Фэнтези'),
        ('Horror', 'Ужасы'),
        ('Mystery', 'Мистика'),
        ('Romance', 'Романтика'),
        ('Sci-Fi', 'Научная фантастика'),
        ('Thriller', 'Триллер'),
        ('War', 'Война'),
        ('Western', 'Вестерн'),
        ('Technical', "Техническая литература")
    )

    name = models.CharField(max_length=30, choices=GENRE_OPTIONS)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=80, verbose_name='book_title')
    author = models.ForeignKey(to=Author, max_length=80, verbose_name='book_author', on_delete=models.CASCADE)
    description = models.TextField()
    published = models.DateField()
    genres = models.ManyToManyField(Genre)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title}: {self.price}Rub"


class Cart(models.Model):
    ADDRESS_OPTIONS = (
        ('Вива-Ленд', "просп. Кирова, 147, Самара"),
        ("Космопорт", "ул. Дыбенко, 30, Самара")
    )
    user = models.OneToOneField(to=User, on_delete=models.PROTECT, related_name='cart_user')
    address = models.CharField(max_length=50, choices=ADDRESS_OPTIONS)
    paid = models.BooleanField(default=False, verbose_name='Статус оплаты')
    created = models.DateTimeField(auto_now_add=True, null=True)

    def total_price(self):
        return sum([cart_item.total() for cart_item in CartBook.objects.filter(cart=self)])

    def __str__(self):
        return f"{self.created}, {self.total_price()}Rub: {'Оплачен' if self.paid else 'Не оплачен'}"


class CartBook(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def total(self):
        return self.count * self.book.price

    def __str__(self):
        return f"{self.book.title}, " \
               f"{self.book.price}Rub * {self.count} = {self.total()}Rub"


class BookReview(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Stars rate 1-5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.book} {self.rating} {self.created_at}"
