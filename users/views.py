from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import View
from PIL import Image
from django.conf import settings
from mysite.settings import EMAIL_HOST_USER 
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from accounts.forms import ClubverificationForm, FeedbackForm, ChatForm, SearchForm, UpdateTaskForm, TaskForm, EventForm, RegisterForm, interestForm, UpdateEventForm, CommentForm, RateForm, ClubTags
import uuid
from datetime import datetime, date, timedelta, time
from django.http import HttpResponseRedirect, request, HttpResponse, JsonResponse
from django.utils.http import urlsafe_base64_encode
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from accounts.models import ClubRating, WaitingArea, EventUpdates, Clubverification, Feedbacks, TaskRoom, TaskChat, clubInfo, jSecs, Members, Info, Event, eventRegistration, Task, Interest, TaskStatus, UserRating, eventComments, eventRating
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.utils.encoding import force_bytes


#### USER REGISTRATION <<<< ==============================================================================>>>>
def register(request):
    if request.method == 'POST':

        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        user = request.POST['username']

        try:
            foo = User.objects.get(username=user)
            profile_form = RegisterForm()
            return render(request, 'accounts/signup.html', {"msg": "Username already exists"})

        except User.DoesNotExist:
            if pass1 == pass2:
                profile_form = RegisterForm(request.POST)

                bar = User.objects.create_user(username=user, password=pass1, email=request.POST['email'])
                bar.save()
                auth_token = str(uuid.uuid4())
                profile = Info(user = bar, auth_token = auth_token)
                profile.save()
                send_mail_after_registration(request.POST['email'] , auth_token)
                messages.success(request, "A email has been sent to you, to verify your account.")
                return redirect("users:login")

            else:
                messages.success(request, "Password didn't match.")

    else:
        profile_form = RegisterForm()

    return render(request, 'accounts/signup.html', {"profile_form": profile_form})


def verify(request, auth_token):
    try:
        profile_obj = Info.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified == "YES":
                messages.success(request, 'Your account is already verified.')
                return redirect('login')


            profile_obj.is_verified = "YES"
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('users:login')

    except Exception as e:
        print(e)
        return redirect('users:register')


def send_mail_after_registration(email , token):

    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account https://www.cosb.live/users/verify/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def login_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        profile_obj = Info.objects.filter(user__username = username).first()


        if not profile_obj:
            messages.success(request, "User not found")

        elif profile_obj.is_verified == "NO":
            messages.success(request, 'Profile is not verified check your email.')
            return redirect('users:register')



        user = authenticate(request, username=username, password = password)

        if user is not None:
            login(request, user)


            mem, created = Members.objects.get_or_create(memname = request.user)

            var = Group.objects.get(name="cosb")
            var.user_set.add(request.user)
            var.save()
            club = clubInfo.objects.get(name = "cosb")
            mem.club.add(club)
            mem.save()

            return HttpResponseRedirect(reverse("index"))


        else:

            messages.info(request, "Invalid Credentials.")
            return render(request, "accounts/login.html")

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "logout successfuly")
    return render(request, "accounts/login.html")


class UpdateInfo(UpdateView):
    model = Info
    template_name = "accounts/updateinfo.html"
    fields = ['full_name', 'course', 'branch', 'sem', 'phone']

    success_url = "/"
    success_message = "Info Updated Successfully!"


@login_required
def deleteaccount(request):
    user = User.objects.filter(id = request.user.id)
    for i in user:
        user.delete()
    return redirect("register")

