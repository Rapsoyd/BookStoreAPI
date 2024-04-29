from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, Response
from library.serializers import UserRegistrationSerializer, UserRetrieveSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):

    @action(detail=False, methods=["get", "post"], url_path="me")
    def me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer)

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        if self.action == "me":
            return UserRetrieveSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()