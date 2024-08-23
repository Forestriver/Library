from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book


class BookTests(APITestCase):

    def setUp(self):
        # Create sample books for testing
        self.book1 = Book.objects.create(
            author='Author One',
            title='Book One',
            date_of_publishing='2020-01-01',
            language='English'
        )
        self.book2 = Book.objects.create(
            author='Author Two',
            title='Book Two',
            date_of_publishing='2021-02-02',
            language='Spanish'
        )
        self.book3 = Book.objects.create(
            author='Author Three',
            title='Book Three',
            date_of_publishing='2022-03-03',
            language='French'
        )

    def test_create_book(self):
        url = reverse('book-create')
        data = {
            'author': 'New Author',
            'title': 'New Book',
            'date_of_publishing': '2023-04-04',
            'language': 'German'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.get(
            pk=response.data['id']).title, 'New Book')

    def test_get_book_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure all books are returned
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['count'], 3)

    def test_get_book_detail(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Book One')

    def test_update_book(self):
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'author': 'Updated Author',
            'title': 'Updated Book',
            'date_of_publishing': '2024-05-05',
            'language': 'Italian'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book')

    def test_delete_book(self):
        url = reverse('book-delete', kwargs={'pk': self.book2.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_pagination(self):
        url = reverse('book-list') + '?page=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming fewer than or exactly 10 books
        self.assertEqual(len(response.data['results']), 3)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
