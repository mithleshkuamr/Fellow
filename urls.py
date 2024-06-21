from django.urls import path
from . import views

urlpatterns = [
    path('comments/store/', views.store_comments_view, name='store_comments'),
    path('comments/', views.get_comments_view, name='get_comments'),
    path('comments/export/', views.export_comments_csv, name='export_comments_csv'),
]
