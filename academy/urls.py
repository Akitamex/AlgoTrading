from django.urls import path
from . import views
from .views import CourseAPIView, ChapterAPIView, LessonAPIView, ReviewAPIView, ProgressAPIView

urlpatterns = [
    path("courses/", CourseAPIView.as_view(), name='courses'),
    path("courses/<int:course_id>", CourseAPIView.as_view(), name='courses-detail'),
    
    path("courses/<int:course_id>/reviews", ReviewAPIView.as_view(), name='courses-reviews'),
    path("courses/<int:course_id>/reviews/<int:review_id>", ReviewAPIView.as_view(), name='courses-reviews-detail'),
    
    path("courses/<int:course_id>/chapters", ChapterAPIView.as_view(), name='course-chapters'),
    path("courses/<int:course_id>/chapters/<int:chapter_id>", ChapterAPIView.as_view(), name='course-chapters-detail'),
    
    path("courses/<int:course_id>/chapters/<int:chapter_id>/lessons", LessonAPIView.as_view(), name='course-chapters-lesson'),
    path("courses/<int:course_id>/chapters/<int:chapter_id>/lessons/<int:lesson_id>", LessonAPIView.as_view(), name='course-chapters-lesson'),

    path("progress/<uuid:user_uuid>", ProgressAPIView.as_view(), name="user-progress"),
    path("progress/", ProgressAPIView.as_view(), name="user-progress"),
]
