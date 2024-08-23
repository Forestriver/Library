from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book


class BookTests(APITestCase):

    def setUp(self):
        # Create sample books with unique ISBNs
        self.book1 = Book.objects.create(
            title='Book One',
            author='Author One',
            published_date='2020-01-01',
            isbn='978-3-16-148410-0',
            pages=200,
            cover='http://example.com/cover1.jpg',
            language='English'
        )
        self.book2 = Book.objects.create(
            title='Book Two',
            author='Author Two',
            published_date='2021-02-02',
            isbn='978-3-16-148410-1',
            pages=300,
            cover='http://example.com/cover2.jpg',
            language='Spanish'
        )

    def test_create_book(self):
        url = reverse('book-create')
        data = {
            'title': 'Book Three',
            'author': 'Author Three',
            'published_date': '2022-03-03',
            'isbn': '978-3-16-148410-2',
            'pages': 400,
            'cover': 'http://example.com/cover3.jpg',
            'language': 'French'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(
            pk=response.data['id']).title, 'Book Three')

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming 2 books in setup

    def test_filter_books_by_author(self):
        url = reverse('book-list') + '?author=Author One'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    def test_filter_books_by_year(self):
        url = reverse('book-list') + '?year_of_publishing=2021'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book Two')

    def test_filter_books_by_language(self):
        url = reverse('book-list') + '?language=Spanish'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book Two')

    def test_get_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Book One')

    def test_update_book(self):
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Updated Book One',
            'author': 'Updated Author One',
            'published_date': '2020-12-31',
            'isbn': '978-3-16-148410-0',  # Unique ISBN must remain the same
            'pages': 250,
            'cover': 'http://example.com/updated_cover.jpg',
            'language': 'English'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book One')

    def test_delete_book(self):
        url = reverse('book-delete', kwargs={'pk': self.book2.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)  # Only 1 book should remain

    def test_get_nonexistent_book(self):
        url = reverse('book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_book(self):
        url = reverse('book-update', kwargs={'pk': 9999})
        data = {
            'title': 'Nonexistent Book',
            'author': 'Nonexistent Author',
            'published_date': '2024-01-01',
            'isbn': '978-3-16-148410-3',
            'pages': 500,
            'cover': 'http://example.com/nonexistent_cover.jpg',
            'language': 'German'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_book(self):
        url = reverse('book-delete', kwargs={'pk': 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
