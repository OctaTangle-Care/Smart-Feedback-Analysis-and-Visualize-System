from django.urls import path
from . import api_views

urlpatterns = [
    path('register/', api_views.RegisterAPIView.as_view(), name='api_register'),
    path('login/', api_views.LoginAPIView.as_view(), name='api_login'),
    path('categories/', api_views.CategoryListAPIView.as_view(), name='api_categories'),
    path('feedbacks/', api_views.FeedbackAPIView.as_view(), name='api_feedbacks'),
    path('feedbacks/<int:feedback_id>/delete/', api_views.DeleteFeedbackAPIView.as_view(), name='api_delete_feedback'),
    path('summary/', api_views.SentimentSummaryAPIView.as_view(), name='api_summary'),
    path('admin/analytics/', api_views.AdminAnalyticsAPIView.as_view(), name='api_admin_analytics'),
]
