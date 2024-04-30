from rest_framework.viewsets import GenericViewSet, ModelViewSet
from library.models import Book, BookReview
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
    Response,
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin)
from library.serializers import (UserRegistrationSerializer,
                                 UserRetrieveSerializer,
                                 BookListSerializer,
                                 BookRetrieveSerializer,
                                 BookReviewSerializer)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

class UserViewSet(CreateModelMixin, GenericViewSet):

    @action(detail=False, methods=["get", "put", "patch", "delete"], url_path="me")
    def me(self, request):
        if request.method == "GET":
            instance = self.request.user
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        elif request.method in ["PUT", "PATCH"]:
            instance = request.user
            serializer = self.get_serializer(instance, data=request.data, partial=request.method == 'PATCH')
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            user = request.user
            user.delete()
            return Response({'message': 'Аккаунт был успешно удалён'}, status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        if self.action in ["retrieve", "me"]:
            return UserRetrieveSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class BookViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Book.objects.all().prefetch_related('genres').order_by('published',
                                                                      'genres')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['title', 'published', 'genres']
    search_filterset = ['title', 'published', 'genres']
    ordering_fields = ['published', 'price']

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        elif self.action == 'retrieve':
            return BookRetrieveSerializer


class BookReviewSet(UpdateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = BookReview.objects.all().prefetch_related("book", "user").order_by("-id")
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    serializer_class = BookReviewSerializer
    ordering_fields = ['created_at', 'rating']
    filterset_fields = ['book__id']

    @action(detail=True, methods=['post'])
    def add_comment_to_book(self, request, pk=None):
        user = request.user
        book = get_object_or_404(Book, pk=pk)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(book=book, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def user_reviews(self, request):
        instance = self.request.user
        book_id = self.request.query_params.get('book_id')  # Getting book id from URL params
        user_reviews = BookReview.objects.filter(user=instance, book__id=book_id)
        serializer = self.get_serializer(user_reviews, many=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не являетесь автором этого отзыва.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не являетесь автором этого отзыва.")
        instance.delete()
