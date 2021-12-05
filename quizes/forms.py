from django import forms
from django.forms import fields, widgets
from questions.models import Question, Answer
from django.forms import ModelForm, inlineformset_factory


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        exclude = ()


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ()


QuizFormSet = inlineformset_factory(
    Question, Answer, form=AnswerForm, extra=1)