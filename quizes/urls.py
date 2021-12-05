from django.urls import path
from .views import QuizListView, quiz_view, quiz_data_view, save_quiz_view, RecentQuizzes, quizform, TestCreate

app_name = 'quizes'

urlpatterns = [
    path('', QuizListView, name='main-view'),
    path('<pk>/', quiz_view, name='quiz-view'),
    path('<pk>/save/', save_quiz_view, name='save-view'),
    path('<pk>/data/', quiz_data_view, name='quiz-data-view'),
    path('recent-quizzes', RecentQuizzes, name='recent-quizzes'),
    path('quiz-form', TestCreate.as_view(), name='quizform'),
]