
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
from .forms import ClubverificationUpdateForm, UpdateStoryForm, ClubverificationForm, FeedbackForm, ChatForm, SearchForm, UpdateTaskForm, TaskForm, EventForm, RegisterForm, interestForm, UpdateEventForm, CommentForm, RateForm, ClubTags
import uuid
from qna.models import Question, ClubQuestion
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
from .models import StoryAudio, Story, ReportClub, ContentCreator, TaskView, Visitors, ClubRating, WaitingArea, EventUpdates, Clubverification, Feedbacks, TaskRoom, TaskChat, clubInfo, jSecs, Members, Info, Event, eventRegistration, Task, Interest, TaskStatus, UserRating, eventComments, eventRating
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.utils.encoding import force_bytes
from course_diary.models import ShareCourse
from qna.forms import QuestionForm

#### Home <<<< ==============================================================================>>>>
def index(request):

    if not  request.user.is_authenticated:
        return render(request, "accounts/landing.html", {"message": None})

    mem, created = Members.objects.get_or_create(memname = request.user)
    club = clubInfo.objects.get(name = "cosb")
    mem.club.add(club)
    mem.save()
    info, created = Info.objects.get_or_create(user = request.user)
    if created:
        info.save()


    stories = Story.objects.all()[:3]

    #foo = Visitors.objects.create(user = request.user)
    #foo.save()

    mem, created = Members.objects.get_or_create(memname = request.user)
        
    return render(request, "accounts/home.html", {"clubs": mem.club.all(), "stories": stories})



@login_required
def allMem(request):

    template_name = "accounts/members.html"




@login_required
def clubMembers(request, id):

    members = Members.objects.values().filter(club = id)    
    club = clubInfo.objects.values().filter(id = id)


    return JsonResponse({"data": list(members), "club": list(club)})



#change
@login_required
def memberinfo(request, member_id):

    info = User.objects.get(id = member_id)
    extended_info = Info.objects.get(user = info)

    return render(request, "accounts/info.html", {"info": info, "extended_info": extended_info})

@login_required
def info(request, username):

    user = User.objects.get(username = username)
    extended_info = Info.objects.filter(user__username = username)
    flag = ""
    interests = user.groups.all()
    ratings, create = UserRating.objects.get_or_create(user = user)
    mem, created = Members.objects.get_or_create(memname = user)

    clubs = mem.club.all()

    if (len(extended_info) == 0):

        flag = "Info not available"


    return render(request, "accounts/info.html", {"info": user, "extended_info": extended_info, "flag": flag, "clubs": clubs, "interests": interests, "ratings": ratings})



### TASKS <<<<<<<<=======================================================================>>>>>>>>>>>>>>>>>>>>>
@login_required
def tasks(request):
    form = interestForm()

    foo, created = TaskStatus.objects.get_or_create(user = request.user)
    
    bar = foo.task.all()
    
    for i in bar:
        print(i)

    s_form = SearchForm()
    return render(request, "accounts/task.html", {"tasks": request.user.groups.all(), "form": form, "search": s_form, "recent_tasks": foo.task.all()})



@login_required
def taskmsg(request, tag_name):

    now = datetime.now()

    mem = Members.objects.get(memname= request.user)
    var = Task.objects.values().filter(tag = tag_name, deadline_date__gte = now, club__in = mem.club.all()).order_by("-id")

    not_done = []

    
    for i in var:

        t = Task.objects.get(id = int(i['id']))
        ts, created = TaskStatus.objects.get_or_create(user = request.user)
        if t not in ts.task.all():

            not_done.append(i)

    print(not_done)
    return JsonResponse({"task_msg": list(not_done)})

@login_required
def taskDetails(request, task_id):

    task = Task.objects.get(id = task_id)

    return render(request, "accounts/task-details.html", {"task_details": task})
      


@login_required
def recentTasks(request):

    j = jSecs.objects.get(name = request.user)
    task_list = Task.objects.filter(club = j.club).order_by("-id")

    return render(request, "accounts/recent-tasks.html", {"task_list":task_list})



@login_required
def TaskUpdate(request, pk, club_id):

    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Task, id = pk)
 
    # pass the object as instance in form
    form = UpdateTaskForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        messages.success(request, "Announcement updated.")
        return HttpResponseRedirect(f"/accounts/task-chat/{pk}/{club_id}/")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "accounts/updatetaskform.html", context)


@login_required
def TaskDelete(request, pk, club_id):

    obj = get_object_or_404(Task, id = pk)

    if obj.user == request.user:
        obj.delete()

        messages.success(request, "Announcement deleted.")
        return redirect(f"/accounts/your-club/{club_id}")

    else:

        messages.success(request, "You don't have permission to delete it.")
        return redirect(f"/accounts/your-club/{club_id}")



def emailtesting(request):

    if request.method == 'POST':

        form = PasswordResetForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            associated_user = User.objects.filter(Q(email=email))

            if associated_user.exists():
                for user in associated_user:
                    subject = "Password Reset Request"
                    email_template_name = "accounts/password_reset_email.txt"

                    c = {

                        "email":user.email,
                        "domain": "www.cosb.live",
                        "site_name": "cosb",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "https",

                    }

                    email = render_to_string(email_template_name, c)
        
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

                    except BadHeaderError:
                        return HttpResponse("Invalid Header Found")

                    return redirect("password_reset_done")



    else:
        form = PasswordResetForm()

    return render(request, "accounts/password_reset.html", {"form": form})



@login_required
def feedbackForm(request):

    if request.method == 'POST':
        
        fd = FeedbackForm(request.POST)


        if fd.is_valid():

            msg = request.POST['feedback']

            feedback = Feedbacks.objects.create(user = request.user, feedback = msg)
            feedback.save()

            messages.success(request, "Thanks for your feedback.")
            return redirect("index")



    return render(request, "accounts/feedback.html", {"form": FeedbackForm()})

###### Club's #######################################################################################################################

@login_required
def clubRegistration(request):

    form = ClubverificationForm(request.POST)
    if request.method == 'POST':

        form = ClubverificationForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data['name']

            logo = request.FILES.get('logo', 'blank')

            tag = form.cleaned_data['tag']

            tagline = form.cleaned_data['tagline']

            vision_and_mission = form.cleaned_data['vision_and_mission']
            private = form.cleaned_data['private']

            club = clubInfo.objects.create(name = name, logo = logo, tag = tag, tagline = tagline, vision_and_mission = vision_and_mission, private = private)
            club.save()

            jsec = jSecs.objects.create(name = request.user, club = club)
            mem, created = Members.objects.get_or_create(memname = request.user)
            mem.club.add(club)
            mem.save()
            jsec.save()

            group = Group.objects.get(name = "jsecs")
            group.user_set.add(request.user)

            messages.success(request, f"Welcome to {club.name}!")
            return redirect(f"/accounts/your-club/{club.id}/")

        else:
            form = ClubverificationForm(request.POST)

        return render(request, "accounts/club-registration.html", {"form": form})



    else:
        return render(request, "accounts/club-registration.html", {"form": form})

@login_required
def EditClub(request, pk):


    context ={}

    obj = get_object_or_404(clubInfo, id = pk)

    form = ClubverificationUpdateForm(request.POST or None, instance = obj) 


    if form.is_valid():

        name = form.cleaned_data['name']

        logo = request.FILES.get('logo', 'blank')

        tag = form.cleaned_data['tag']

        tagline = form.cleaned_data['tagline']

        vision_and_mission = form.cleaned_data['vision_and_mission']

        private = form.cleaned_data['private']

        club = clubInfo.objects.create(name = name, logo = logo, tag = tag, tagline = tagline, vision_and_mission = vision_and_mission, private = private)
        club.save()

        return redirect(f"/accounts/your-club/{pk}/")       

    return render(request, "accounts/club-registration.html", {"form": form})


@login_required
def club(request, club_id):

    club = clubInfo.objects.get(id = club_id)

    flag_mem = Members.objects.filter(memname = request.user, club = club)

    announcement_form = TaskForm()
    question_form = QuestionForm()

    club_members = Members.objects.filter(club = club)
    if flag_mem:

        club_mem = club.clubs.all()

        foo = Members.objects.filter(club = club)

        mem, created = WaitingArea.objects.get_or_create(club = club)

        club_discussion = Task.objects.filter(club = club).order_by("-id")

        allclub = Members.objects.get(memname = request.user)
        

        club_questions = ClubQuestion.objects.filter(club = club)


        flag = False
        bar = club.jsecsclub.all()

        jsec = jSecs.objects.filter(name = request.user, club = club)

        if jsec:
            flag = True

        shared_courses = ShareCourse.objects.filter(club = club)

        return render(request, "accounts/clubs.html", {"club": club, "jsecs": club.jsecsclub.all(), "questions": club_questions[:3], "club_discussion": club_discussion[:3], "flag": flag, "waiting_list": len(mem.user.all()), "allclub": allclub.club.all(), "shared_courses": shared_courses, "announcement_form": announcement_form, "question_form": question_form, "total_members": len(club_members)})

    else:

        return redirect(f"/accounts/view-club/{club_id}/")


@login_required
def club_discussion(request, club_id):

    club = clubInfo.objects.get(id = club_id)
    form = TaskForm()
    mem = Members.objects.get(memname = request.user)
    messages = Task.objects.filter(club = club_id).order_by("-id")
    print(mem.club.all())
    return render(request, "accounts/club-discussion.html", {"message": messages, "club_id": club_id, "club": club, "clubs": mem.club.all(), "form": form})


@login_required
def taskform(request):

    if request.method == 'POST':

        form = TaskForm(request.POST)

        if form.is_valid():

            club_name = request.POST['club-name']
            club_id = clubInfo.objects.get(id = int(club_name))
            msg = request.POST['msg']
            task = Task(user = request.user, club = club_id, msg=msg)
            task.save()
            club = clubInfo.objects.get(id = int(club_name))
            foo = TaskRoom.objects.create(task = task)
            foo.save()

            #create a task messages instance.
            messages.success(request, "New topic added!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


            
    clubs, created = Members.objects.get_or_create(memname = request.user)

    return render(request, "accounts/taskform.html", {"form": TaskForm(), "clubs": clubs.club.all()})

@login_required
def taskChat(request, task_id, club_id):

    bar = Task.objects.get(id = task_id)
    foo = TaskChat.objects.filter(task = bar).order_by("-id")
    discussions = Task.objects.filter(club = club_id).order_by("-id")
    seen = TaskView.objects.create(user = request.user, task = bar)
    seen.save()
    total_views = TaskView.objects.filter(task = bar)
    form = ChatForm()
    return render(request, "accounts/task-chat.html", {"chat": foo, "form": form, "id": task_id, "disc": discussions, "club_id": club_id, "task": bar, "total_views": len(total_views)})


def view_club(request, club_id):

    flag1 = False

    flag2 = False

    club = clubInfo.objects.get(id = club_id)

    if request.user.is_authenticated:

        user_club, created = Members.objects.get_or_create(memname = request.user)

        user_clubs = user_club.club.all()

        foo, create = WaitingArea.objects.get_or_create(club = club)

        if request.user in foo.user.all():
            flag1 = True

        if club in user_clubs:
            flag2 = True

    return render(request, "accounts/join-club.html", {"club": club, "flag1": flag1, "flag2": flag2})




def clubTag(request, tag):
     

    #user_club, created = Members.objects.get_or_create(memname = request.user)
    #user_clubs = user_club.club.all()

    if (tag == 'ALL'):
        clubs = clubInfo.objects.filter(private = False)
        return render(request, "accounts/allclub.html", {"clubs": clubs, "tag": "ALL"})

    clubs = clubInfo.objects.filter(tag = tag, private = False)
    return render(request, "accounts/allclub.html", {"clubs": clubs, "tag": tag}) 



@login_required
def join_club(request, club_id):

    club = clubInfo.objects.get(id = club_id)
    wait, created = WaitingArea.objects.get_or_create(club = club)
    wait.user.add(request.user)
    return JsonResponse({"status": 1})



@login_required
#@user_passes_test(lambda u: Group.objects.get(name='jsecs') in u.groups.all())
def view_waitingarea(request, club_id):

    club = clubInfo.objects.get(id = club_id)
    jsec = jSecs.objects.filter(name = request.user, club = club)

    if jsec:
        members, created = WaitingArea.objects.get_or_create(club = club)
        mem = Members.objects.filter(club = club) 
        return render(request, "accounts/addmembers.html", {"members": members.user.all(), "club_id": club_id, "mem": mem, "club": club})

    else:
        return redirect(f"/accounts/your-club/{club_id}/")


@login_required
def addmem(request, mem_id, club_id):


    club_name = clubInfo.objects.get(id = club_id)

    jsec = jSecs.objects.filter(name = request.user, club = club_name)

    if jsec:
        member = User.objects.get(pk = mem_id)

        addmember, created = Members.objects.get_or_create(memname = member)
        addmember.club.add(club_name)
        addmember.save()
        waiting, created = WaitingArea.objects.get_or_create(club = club_name)

        waiting.user.remove(member)

        return JsonResponse({"status": 1})

    else:

        return JsonResponse({"status": 0})

@login_required
def make_jsec(request, club_id, mem_id):

    club_name = clubInfo.objects.get(id = club_id)
    jsec = jSecs.objects.filter(name = request.user, club = club_name)

    if jsec:

        mem = User.objects.get(pk = mem_id)
        already_jsec = jSecs.objects.filter(club = club_name, name = mem)

        if already_jsec:

            messages.success(request, "Already a Jsec.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        new_jsec = jSecs.objects.create(club = club_name, name = mem)
        new_jsec.save()

        messages.success(request, "New Jsec added.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:

        return redirect(f"/accounts/view-club/{club_id}/")



@login_required
def removemem(request, mem_id, club_id):

    club = clubInfo.objects.get(id = club_id)

    jsec = jSecs.objects.filter(name = request.user, club = club)

    if jsec:
        u = User.objects.get(id = mem_id)
        mem = Members.objects.get(memname =  u, club = club)
        mem.club.remove(club)
        mem.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:

        return redirect(f"/accounts/view-club/{club_id}/")



@login_required
def club_Members(request, id):

    members = Members.objects.filter(club = id)    
    club = clubInfo.objects.values().filter(id = id)


    return render(request, "accounts/members.html",{"object_list": members})

@login_required
def leaveclub(request, club_id):

    club = clubInfo.objects.get(id = club_id)
    mem = Members.objects.get(memname = request.user, club = club)
    mem.club.remove(club)
    mem.save()

    return redirect(f"/accounts/view-club/{club_id}/")


def content_creators(request):

    if request.method == 'POST':

        msg = request.POST['msg']
        email = request.POST['email']
        creator = ContentCreator.objects.create(user = request.user, msg = msg, email = email)
        creator.save()
        messages.success(request, "We will contact you in a few moments.")
        return redirect("index")


@login_required
def report_club(request, club_id):

    if request.method == 'POST':

        msg = request.POST['msg']
        club = clubInfo.objects.get(id = club_id)
        report = ReportClub(user = request.user, club = club, msg = msg)
        report.save()
        messages.success(request, "We are resolving your problems.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def donation(request):
    return render(request, "accounts/donation.html")


def stories(request):

    allStories = Story.objects.all().order_by("-id")
    allclub = Members.objects.get(memname = request.user)

    return render(request, "accounts/stories.html", {"stories": allStories, "clubs": allclub.club.all()})

@login_required
def add_story(request):

    if request.method == 'POST':

        tag = request.POST['tag']
        title = request.POST['title']
        content = request.POST['content']
        club_id = request.POST['club-name']
        club = clubInfo.objects.get(id = club_id)
        story = Story.objects.create(user = request.user, tag = tag, title = title, content = content, club = club, views = 0)
        story.save()

        return redirect(f"/accounts/view-story/{story.id}/")


    return redirect("stories")


def view_story(request, story_id):

    story = Story.objects.get(id = story_id)
    story.views = story.views + 1
    story.save()
    foo = False
    audio = StoryAudio.objects.filter(story = story)
    if request.user.is_authenticated:
        allclub = Members.objects.get(memname = request.user)
        foo = allclub.club.all()

    return render(request, "accounts/story.html", {"story": story, "clubs": foo, "audio": audio})


def delete_story(request, story_id):
    
    story = Story.objects.get(id = story_id)

    if request.user == story.user:
        obj = get_object_or_404(Story, id = pk)
        obj.delete()

    return redirect("stories")


def update_story(request, story_id):

    context ={}
    obj = get_object_or_404(Story, id = story_id)
    form = UpdateStoryForm(request.POST or None, instance = obj) 


    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/accounts/stories/')       

    return render(request, "accounts/story-update-form.html", {"form": form})