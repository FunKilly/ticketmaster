from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, permissions
from common_utils.mixins import GetSerializerClassMixin

from .models import UserTicket
from .serializers import UserTicketListSerializer, UserTicketDetailSerializer, UserTicketCreateSerializer


class UserTicketViewSet(
    GetSerializerClassMixin,
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserTicketDetailSerializer
    queryset = UserTicket.objects.all()
    serializer_action_classes = {
        "list": UserTicketListSerializer,
        "detail": UserTicketDetailSerializer,
        "create": UserTicketCreateSerializer,
    }


