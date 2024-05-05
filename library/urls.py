from rest_framework.routers import SimpleRouter
from library.views import BookViewSet, BookReviewSet, CartAPI
from django.urls import path
router = SimpleRouter()
router.register(r"books", BookViewSet, basename="books")
router.register(r"book_reviews", BookReviewSet, basename="book_reviews")

urlpatterns = [
    *router.urls,
    path('cart', CartAPI.as_view(), name='cart'),
]
