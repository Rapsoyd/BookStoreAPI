from rest_framework.routers import SimpleRouter
from library.views import UserViewSet, BookViewSet, BookReviewSet

router = SimpleRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"books", BookViewSet, basename="books")
router.register(r"book_reviews", BookReviewSet, basename="book_reviews")


urlpatterns = router.urls