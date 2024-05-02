from rest_framework import serializers
from django.contrib.auth.models import User
from library.models import BookReview, Book
from django.db.models import Avg


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User(
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user

class BookListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "published",
            "genres",
            "price",
            "avg_rating",
            "total_reviews",
            "short_description",
        )

    def get_avg_rating(self, obj):
        return BookReview.objects.filter(book=obj).aggregate(avg_rating=Avg('rating'))['avg_rating']

    def get_total_reviews(self, obj):
        return BookReview.objects.filter(book=obj).count()

    def get_short_description(self, obj):
        if len(obj.description) > 270:
            return obj.body[:270] + '...'
        return obj.body


class BookReviewSerializer(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = BookReview
        fields = ('id', 'book', 'user', 'comment', 'rating', 'created_at', 'can_edit')
        read_only_fields = ('id', 'book', 'user', 'created_at', 'can_edit')

    def get_can_edit(self, obj):
        return obj.user == self.context['request'].user


class BookRetrieveSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    author = serializers.CharField(source='author.name')

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "description",
            "published",
            "genres",
            "price",
            "avg_rating",
            "total_reviews",
        )

    def get_avg_rating(self, obj):
        return BookReview.objects.filter(book=obj).aggregate(avg_rating=Avg('rating'))['avg_rating']

    def get_total_reviews(self, obj):
        return BookReview.objects.filter(book=obj).count()


