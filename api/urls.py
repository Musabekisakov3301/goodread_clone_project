from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import BookReviewViewSet  #BookReviewDetailAPIView, BookReviewListAPIView

app_name = 'api'

router = DefaultRouter()
router.register('reviews', BookReviewViewSet, basename='review')
urlpatterns = router.urls


'''urlpatterns = [
    path('reviews/', BookReviewListAPIView.as_view(), name='review-list'),
    path('reviews/<int:id>/', BookReviewDetailAPIView.as_view(), name='review-detail'),
]
'''