from rest_framework.viewsets import GenericViewSet
from library.models import Book, BookReview
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
    Response,
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin)
from library.serializers import (
    BookListSerializer,
    BookRetrieveSerializer,
    BookReviewSerializer,
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from library.services import Cart


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

    @action(detail=True, methods=['get'])
    def user_reviews(self, request, pk=None):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset().filter(user=user))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(data=request.data)
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


class CartAPI(APIView):
    """
    Single API to handle cart operations
    """

    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {"data": list(cart.__iter__()),
             "cart_total_price": cart.get_total_price()},
            status=status.HTTP_200_OK
        )

    def post(self, request, **kwargs):
        cart = Cart(request)

        if "remove" in request.data:
            product = request.data["product"]
            cart.remove(product)

        elif "clear" in request.data:
            cart.clear()

        else:
            product = request.data
            cart.add(
                product=product["product"],
                quantity=product["quantity"],
                overide_quantity=product["overide_quantity"] if "overide_quantity" in product else False
            )

        return Response(
            {"message": "cart updated"},
            status=status.HTTP_202_ACCEPTED)
