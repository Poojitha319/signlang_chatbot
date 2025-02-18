from django.urls import path
from .views import AlphabetAPIView, NumberAPIView, WordAPIView, MathExerciseAPIView, ScienceLessonAPIView, LearningProgressAPIView,VideoUploadView,VideoListView,VideoDetailView

urlpatterns = [
    path('api/alphabet/<str:letter>/', AlphabetAPIView.as_view(), name='alphabet'),
    path('api/number/<int:number>/', NumberAPIView.as_view(), name='number'),
    path('api/word/<str:word>/', WordAPIView.as_view(), name='word'),
    path('api/math-exercises/', MathExerciseAPIView.as_view(), name='math_exercises'),
    path('api/science-lessons/', ScienceLessonAPIView.as_view(), name='science_lessons'),
    path('api/progress/<int:student_id>/', LearningProgressAPIView.as_view(), name='progress'),
    path('media/upload-video/', VideoUploadView.as_view(), name='upload-video'),
    path('media/videos/', VideoListView.as_view(), name='video_list'),
    path('media/videos/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
]
