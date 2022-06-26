from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('results', views.ResultsPage.as_view(), name='results')
]