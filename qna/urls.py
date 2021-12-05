from django.urls import path
from .views import clubQuestions, QuestionJsonListView, questionTags, questionListView, addQuestion, deleteQuestion, updateQuestion, updateAnswere, addAnswere, deleteAnswere, userQuestion, userAnswer

app_name = 'qna'

urlpatterns = [
    path('', questionListView , name='question-view'),
    path('addquestion/<int:club_id>/', addQuestion , name='add-question-view'),
    path('delete-ques/<slug:pk>/', deleteQuestion, name='delete-question-view'),
    path('update-question/<slug:pk>/', updateQuestion, name='update-question-view'),
    path('add-answere/<int:id>/', addAnswere, name='add-answere-view'),
    path('update-answere/<slug:pk>/', updateAnswere, name='update-answere-view'),
    path('delete-answere/<slug:pk>/', deleteAnswere, name='delete-answere-view'),
    path('your-question/', userQuestion, name='your-question-view'),
    path('your-answer/', userAnswer, name='your-answer-view'),
    path('filter-questions/<str:tag>/', questionTags, name='filter-questions'),
    path('questions-scroll/<int:visible>/', QuestionJsonListView.as_view(), name='questions-scroll'),
    path('club-qna/<int:club_id>/', clubQuestions, name='club-qna'),


]