from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from users.models import CustomUser
from books.models import Book,BookReview

class BookReviewTestCase(APITestCase):
    def setUp(self):
        # DRY - Don't Repeat yourself
        self.user = CustomUser.objects.create(username='musabek', first_name='musabek')
        self.user.set_password('0424')
        self.user.save()
        self.client.login(username='musabek', password='0424')
    
    def test_book_review_detail(self):
       book = Book.objects.create(title='Book1', description='Description1', isbn='1345236')
       book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Rest API Book')
       
       response = self.client.get(reverse('api:review-detail', kwargs={'id': book_review.id}))

       self.assertEqual(response.status_code, 200)
       self.assertEqual(response.data['id'], book_review.id)
       self.assertEqual(response.data['stars_given'], 5)
       self.assertEqual(response.data['comment'], 'Rest API Book')
       self.assertEqual(response.data['book']['description'], 'Description1')
       self.assertEqual(response.data['book']['isbn'], '1345236')
       self.assertEqual(response.data['user']['id'], self.user.id)
       self.assertEqual(response.data['user']['first_name'], 'musabek')
       self.assertEqual(response.data['user']['username'], 'musabek')
    
    def test_delete_review(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1345236')
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Rest API Book')
        
        response = self.client.delete(reverse('api:review-detail', kwargs={'id': book_review.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=book_review.id).exists())
    
    def test_patch_review(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1345236')
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Rest API Book')
        
        response = self.client.delete(reverse('api:review-detail', kwargs={'id': book_review.id}), data={'stars_given': 4})
        book_review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.stars_given, 4)
    
    def test_put_review(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1345236')
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Rest API Book')
        
        response = self.client.delete(
            reverse('api:review-detail', kwargs={'id': book_review.id}), 
            data={'stars_given': 4, 'comment': 'New Comment', 'user_id': self.user.id, 'book': book.id}
        )
        book_review.refresh_from_db()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.stars_given, 4)
        self.assertEqual(book_review.comment, 'New Comment')
    
    def test_create_review(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1345236')
        data = {
            'stars_given': 5,
            'comment': 'New Comment',
            'user_id': self.user.id,
            'book_id': book.id
        }
        
        response = self.client.post(reverse('api:review-list'), data=data)
        book_review = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(book_review.stars_given, 5)
        self.assertEqual(book_review.comment, 'New Comment')

    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username='user2', first_name='User2')
        book = Book.objects.create(title='Book1', description='Description1', isbn='1345236')
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Rest API Book')
        book_review_two = BookReview.objects.create(book=book, user=user_two, stars_given=4, comment='Django Rest Framework')
        
        response = self.client.get(reverse('api:review-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(response.data['results'][0]['id'], book_review_two.id)
        self.assertEqual(response.data['results'][0]['stars_given'], book_review_two.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], book_review_two.comment)
        self.assertEqual(response.data['results'][1]['id'], book_review.id)
        self.assertEqual(response.data['results'][1]['stars_given'], book_review.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], book_review.comment)