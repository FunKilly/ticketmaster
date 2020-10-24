"""ticketmaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from events.views import EventManagementViewSet, EventViewSet
from tickets.views import UserTicketViewSet
from users.views import CreateUserView, ObtainAuthToken

router = DefaultRouter()
router.register(r"admin/events", EventManagementViewSet)
router.register(r"events", EventViewSet)
router.register(r"tickets", UserTicketViewSet)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("login/", ObtainAuthToken.as_view(), name="login"),
]

urlpatterns += router.urls
