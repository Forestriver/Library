from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        author = self.request.query_params.get('author', None)
        year = self.request.query_params.get('year', None)
        language = self.request.query_params.get('language', None)

        if author:
            queryset = queryset.filter(author__icontains=author)
        if year:
            queryset = queryset.filter(date_of_publishing__year=year)
        if language:
            queryset = queryset.filter(language__icontains=language)

        return queryset


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
