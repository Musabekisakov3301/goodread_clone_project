from django.test import TestCase
from django.urls import reverse

from books.models import Book,CustomUser

class BookTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))
        self.assertContains(response, 'No books found.')

    def test_books_list(self):
        book1 = Book.objects.create(title='book1', description='description1', isbn='11111')
        book2 = Book.objects.create(title='book2', description='description2', isbn='22222')
        book3 = Book.objects.create(title='book3', description='description3', isbn='33333')

        response = self.client.get(reverse('books:list') + "?page_size=2")
        
        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + "?page=2?page_size=2")

        self.assertContains(response, book3.title)
    
    def test_books_detail(self):
        book = Book.objects.create(title='book1', description='description1', isbn='11111')

        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
    
    def test_search_books(self):
        book1 = Book.objects.create(title='api', description='description1', isbn='11111')
        book2 = Book.objects.create(title='django', description='description2', isbn='22222')
        book3 = Book.objects.create(title='fastapi', description='description3', isbn='33333')

        response = self.client.get(reverse("books:list") + "?q=api")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)
        
        response = self.client.get(reverse("books:list") + "?q=django")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)
        
        response = self.client.get(reverse("books:list") + "?q=fastapi")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)

class BookReviewTest(TestCase):

    def test_add_review(self):
        book = Book.objects.create(title='book1', description='description1', isbn='11111')
                                    
        user = CustomUser.objects.create(
            username='user1', first_name='user_first_name', last_name='user_last_name', email='musabekisakov5@gmail.com'
        )
        user.set_password('123456789')
        user.save()

        self.client.login(username='user1', password='123456789')
        
        response = self.client.post(reverse('books:reviews', kwargs={'id:book.id'}), data={
            'stars_given': 3,
            'comment': 'Book'
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'Book')
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)