from django.urls import path
from .views import home, adding_target

urlpatterns = [
    path('', home),
    path('add_target', adding_target)
]
