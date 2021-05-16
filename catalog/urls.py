from django.urls import path
from . import views

urlpatterns = [
    # Function path defines:
    #     1. URL pattern: empty string
    #     2. View function thatll be called if the URL pattern is detected
    #     3. Name: unique identifier for this URL mapping
    path('', views.index, name='index'),
]