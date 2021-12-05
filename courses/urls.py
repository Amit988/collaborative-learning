
from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [

    path('', views.view_courses, name='courses-view'),
    path("course-lessons/<int:course_id>/", views.course_lessons, name = 'lesson-view'),
    path("lesson-video/<slug:link>/<int:course_id>/<int:lesson_id>/", views.lesson_video, name = 'lesson-video'),
    path("course-qna/<int:course_id>/", views.course_qna, name = 'course-qna'),
    path("add-course-qna/<int:course_id>/", views.addQuestion, name = 'add-course-qna'),


]