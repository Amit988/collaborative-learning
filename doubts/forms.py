from django import forms
from django.forms import fields, widgets
from .models import Answere, Question
from django_summernote.widgets import SummernoteWidget
from django_summernote.fields import SummernoteTextFormField

INTERSET_CHOICES = [

    ("web-developement", "web-developement"),
    ("machine-learning", "machine-learning"),
    ("android-developement", "android-developement"),
    ("designing", "designing"),
    ("video-editing", "video-editing"),
    ("content-writting", "content-writting"),
    ("marketing", "marketing"),

    ("general", "general"),
    ("competitive programming", "competitive programming"),
]

class QuestionForm(forms.Form):

    title = forms.CharField(max_length=2000, label = "Title", widget = forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'title', 'rows': 0}))
    tag = forms.CharField(label = "Tags", widget = forms.Textarea(attrs = {'placeholder': 'css,html,javascript...', 'rows': 0}))
    detail = forms.CharField(label = "Details", widget = forms.Textarea(attrs = {'id': 'summernote'}))
    

class AnswereForm(forms.Form):
    answere = forms.CharField(label = "Your Answer", widget = SummernoteWidget())

class UpdateAnswereForm(forms.ModelForm):
    
    ans = forms.CharField(label ="Your answer", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'id':'summernote',
    }))

    class Meta:

        model = Answere
        fields = ["ans"]

        widgets = {"ans": forms.Textarea(attrs={'cols': 80, 'rows': 20, 'id': 'summernote'}),
        }


    
class UpdateQuestionForm(forms.ModelForm):
    

    class Meta:

        model = Question
        fields = ["title", "tag", "detail"]

        widgets = {"detail": forms.Textarea(attrs={'cols': 80, 'rows': 20, 'id': 'summernote'}),
        }


class QuestionSearchForm(forms.Form):
    tags = forms.ChoiceField(choices=INTERSET_CHOICES, widget = forms.Select(attrs = {'class': 'form-control border-dark text-center', "style": "font-size:16px;", "id": "tag"}))

