from django import forms
from django.db.models import fields
from django.forms import widgets
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextFormField
from .models import Event, TaskChat, eventComments, eventRating,Task, Feedbacks, clubInfo, Clubverification, Members, Story

INTERSET_CHOICES = [

    ("web-developers", "web-development"),
    ("machine-learning", "machine-learning"),
    ("android-development", "android-development"),
    ("designing", "designing"),
    ("video-editing", "video-editing"),
    ("content-writting", "content-writting"),
    ("marketing", "marketing"),
    ("general", "general"),
    ("competitive programming", "competitive programming"),
]


BRANCH_CHOICES = [
    ("Computer Engg", "Computer Engg"),
    ("CSDS", "CSDS"),
    ("IT", "IT"),
    ("ECS", "ECS"),
    ("EIOT", "EIOT"),
    ("ECE", "ECE"),
    ("Mech", "Mech"),
    ("Civil", "Civil"),
    ("BBA", "BBA"),
    ("BSc", "BSc"),
    ("B.Com", "B.Com"),
    ("B.Voc", "B.Voc"),
    ("M.Tech", "M.Tech"),
    ("MBA", "MBA"),
]
SEM_CHOICES = [

    ("First", "First"),
    ("Second", "Second"),
    ("Third", "Third"),
    ("Fourth", "Fourth"),
    ("Fifth", "Fifth"),
    ("Sixth", "Sixth"),
    ("Seventh", "Seventh"),
    ("Eight", "Eight"),
]
COURSE_CHOICES = [

    ("B.Tech", "B.Tech"),
    ("BBA", "BBA"),
    ("BSC", "BSC"),
    ("B.COM", "B.COM"),
    ("M.Tech", "M.Tech"),
    ("B.Voc", "B.Voc"),
    ("MBA", "MBA"),


]

CLUB_FIELDS = [

    ("ART & CRAFT", "ART & CRAFT"),
    ("DRAMA", "DRAMA"),
    ("DATA SCIENCE", "DATA SCIENCE"),
    ("TECHNICAL", "TECHNICAL"),
    ("CYBERSECURITY", "CYBERSECURITY"),
    ("SPRITUAL", "SPRITUAL"),
    ("SPORTS", "SPORTS"),
    ("MUSIC", "MUSIC"),
    ("SOFTWARE", "SOFTWARE"),
    ("FINANCE", "FINANCE"),
    ("DESIGN", "DESIGN"),
    ("ALL", "ALL"),


]


class TaskForm(forms.ModelForm):
    msg = forms.CharField(label = "Message", widget = forms.Textarea(attrs = {'id': 'summer'}))

    class Meta:

        model = Task 
        fields = ['msg']


class RegisterForm(forms.Form):
    full_name = forms.CharField(max_length=255, required=False, label = "Full Name", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Diary Greenson',
        'rows':2,
        'cols':30,

    }))
    sem = forms.ChoiceField(choices=SEM_CHOICES)
    course = forms.ChoiceField(choices = COURSE_CHOICES)
    branch = forms.ChoiceField(choices=BRANCH_CHOICES)
    phone_no = forms.CharField(max_length=10, widget = forms.TextInput(attrs = {'class': 'special'}), required=False, label = "Mobile Number(Optional)")

class interestForm(forms.Form):
    interest = forms.ChoiceField(choices=INTERSET_CHOICES, widget = forms.Select(attrs = {'class': 'form-control border-dark', "style": "font-size:16px;"}))

class EventForm(forms.Form):

    name = forms.CharField(max_length=500, help_text="")
    content = forms.CharField(widget = SummernoteWidget())
    poster = forms.ImageField(help_text="recommended 300px*300px")
    #date = forms.DateTimeField()

class UpdateEventForm(forms.ModelForm):

    name = forms.CharField(max_length=500)
    content = SummernoteTextFormField()
    poster = forms.ImageField()


    class Meta:

        model = Event
        fields = "__all__"

        widgets = {"content": SummernoteWidget()
        }



class UpdateTaskForm(forms.ModelForm):

    msg = forms.CharField(label = "Message", widget = forms.Textarea(attrs = {'class': 'form-control', 'id': 'summernote'}))

    class Meta:

        model = Task
        fields = ['msg']


class UpdateStoryForm(forms.ModelForm):


    content = forms.CharField(label ="Story", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'id':'summernote',
    }))


    class Meta:

        model = Story
        fields = ["title", "content"]



class CommentForm(forms.ModelForm):

    comment = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Comment here !',
        'rows':1,
        'cols':5,
        'id':'commentid',
    }))

    class Meta:

        model = eventComments
        fields = ["comment"]

RATE_CHOICES = [('poor', 'poor'), ('good', 'good'), ('very good', 'very good')]


class RateForm(forms.Form):

    rate_field = forms.ChoiceField(choices=RATE_CHOICES, widget = forms.Select(attrs = {'class': 'form-control', "name": "Rate this event", "id": "rateid"}))

class ClubTags(forms.Form):

    tag_field = forms.ChoiceField(choices=CLUB_FIELDS, widget = forms.Select(attrs = {"id": "select-tag"}))

class SearchForm(forms.Form):


    search = forms.ChoiceField(help_text= "Search students by profession.", choices = INTERSET_CHOICES, widget = forms.Select(attrs = {'class': 'form-control', 'style': 'width:300px', 'style': 'border-color: black'}))


class ChatForm(forms.ModelForm):

    msg = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'What do you want to talk about?',
        'rows':2,
        'cols':30,
        'id':'chatid',
    }))

    class Meta:

        model = TaskChat
        fields = ["msg"]


class FeedbackForm(forms.ModelForm):

    feedback = forms.CharField(widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Your suggestions here!',
        'rows':2,
        'cols':30,

    }))

    class Meta:

        model = Feedbacks
        fields = ["feedback"]


class ClubverificationForm(forms.Form):

    name = forms.CharField(label = "Club's Name", widget = forms.TextInput(attrs = {'class': 'mt-1 mb-1'}))

    logo = forms.ImageField(label = "Club's logo", required = False, widget = forms.FileInput(attrs = {'class': 'mt-1 mb-2'}))

    tag = forms.ChoiceField(choices=CLUB_FIELDS, label = "club's Field")
    tagline = forms.CharField(required = False, widget = forms.TextInput(attrs = {'class': 'mt-2 mb-2'}))
    vision_and_mission = forms.CharField(label = "club's vission and mission", required = False, widget = forms.Textarea(attrs = {"class": "form-control", "cols":10}))
    
    #private = forms.BooleanField(label = "Make Private", required = False)




class ClubverificationUpdateForm(forms.ModelForm):

    name = forms.CharField(label = "Club's Name", widget = forms.TextInput(attrs = {'class': 'mt-1 mb-1'}))

    logo = forms.ImageField(label = "Club's logo", required = False, widget = forms.FileInput(attrs = {'class': 'mt-1 mb-2'}))

    tag = forms.ChoiceField(choices=CLUB_FIELDS, label = "club's Field")
    tagline = forms.CharField(required = False, widget = forms.TextInput(attrs = {'class': 'mt-2 mb-2'}))
    vision_and_mission = forms.CharField(label = "club's vission and mission", required = False, widget = forms.Textarea(attrs = {"class": "form-control", "cols":10}))
    
    #private = forms.BooleanField(label = "Make Private", required = False)
    
    class Meta:

        model = clubInfo

        fields = ['name', 'logo', 'tag', 'tagline', 'vision_and_mission']
            
    

# , widget = forms.FileInput(attrs = {'class': 'mt-1 mb-2'})   
#release: python manage.py migrate