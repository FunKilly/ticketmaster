from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView

from .exceptions import InvalidCredentialsException
from .serializers import AuthTokenSerializer, UserSerializer


class CreateUserView(CreateAPIView):
    queryset = get_user_model()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    # Login
    serializer_class = AuthTokenSerializer
    permission_classes = (permissions.AllowAny,)
    serializer_action_classes = {
        "create": AuthTokenSerializer,
    }

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = self.get_user_if_valid(serializer.validated_data)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})

    @staticmethod
    def get_user_if_valid(data):
        username = data["username"]
        password = data["password"]

        user = authenticate(username=username, password=password)

        if not user:
            raise InvalidCredentialsException
        else:
            return user
