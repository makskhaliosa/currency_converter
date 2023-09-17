from django.urls import path

from .views import RatesViewSet

name = 'api'

urlpatterns = [
    path('rates', RatesViewSet.as_view()),
]
