from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.list_books, name='book-list'),
    path('books/create/', views.create_book, name='book-create'),
    path('books/<int:pk>/', views.get_book, name='book-detail'),
    path('books/<int:pk>/update/', views.update_book, name='book-update'),
    path('books/<int:pk>/delete/', views.delete_book, name='book-delete'),
]
