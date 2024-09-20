from django.urls import path
from . import views


urlpatterns = [
    path('table/', views.showTable,name='table'),
    path('logs/', views.showLogs,name='logs'),
    path('match/',views.showMatches,name='match'),
    path('search/',views.showSearch,name='search'),
]