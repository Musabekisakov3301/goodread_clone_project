from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser

class HomePageTest(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='Book1',description='Description1',isbn='123123')
        user = CustomUser.objects.create(
            username='user1', first_name='user_first_name', last_name='user_last_name', email='musabekisakov5@gmail.com'
        )
        user.set_password('123456789')
        user.save()
        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment='New Book')
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment='Book')
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment='Test')

        response = self.client.get(reverse('home_page') + '?page_size=2')

        self.assertContains(response, review2.comment)
        self.assertContains(response, review3.comment)
        self.assertNotContains(response, review1.comment)