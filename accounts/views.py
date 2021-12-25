
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
from .forms import UpdateStoryForm, ClubverificationForm, FeedbackForm, ChatForm, SearchForm, UpdateTaskForm, TaskForm, EventForm, RegisterForm, interestForm, UpdateEventForm, CommentForm, RateForm, ClubTags
import uuid
from qna.models import Question
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
from .models import Story, ReportClub, ContentCreator, TaskView, Visitors, ClubRating, WaitingArea, EventUpdates, Clubverification, Feedbacks, TaskRoom, TaskChat, clubInfo, jSecs, Members, Info, Event, eventRegistration, Task, Interest, TaskStatus, UserRating, eventComments, eventRating
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.utils.encoding import force_bytes


#### Home <<<< ==============================================================================>>>>

def index(request):

    if not  request.user.is_authenticated:
        return render(request, "accounts/landing.html", {"message": None})

    mem, created = Members.objects.get_or_create(memname = request.user)
    club = clubInfo.objects.get(name = "cosb")
    mem.club.add(club)
    mem.save()

    form = RateForm()
    poster = Event.objects.all()

    #foo = Visitors.objects.create(user = request.user)
    #foo.save()
    user_rated_event = eventRating.objects.filter(user = request.user)
    event = []

    userrating = UserRating.objects.filter(user = request.user)

    mem, created = Members.objects.get_or_create(memname = request.user)
    for i in user_rated_event:

        event.append(i.event.name)


    now = date.today()
    #one = date(day = (now.day) + 1, month = now.month, year = now.year)
    t = datetime.now()

    tt = time(t.hour, t.minute, t.second)

    events_upcoming = eventRegistration.objects.filter(user = request.user, event__event_date__gte = now).order_by("-id")[:2]
    events_rating = eventRegistration.objects.filter(user = request.user, event__event_date__lt = datetime.now())#.exclude(event__name__in = event)
    

        
    return render(request, "accounts/home.html", {"clubs": mem.club.all(), "pos": poster, "events_upcoming": events_upcoming, "events_rating": events_rating, "form": form})


##### Events<<<< =======================================================================================>>>>>>
class event(ListView):

    template_name = "accounts/events.html"
    model = Event

    def get_queryset(self):
        now = date.today()
        t = datetime.now()

        tt = time(t.hour, t.minute, t.second)
        upcoming = Event.objects.filter(event_date__gte = now).order_by("-id")

        return upcoming

@login_required
def eventdetails(request, id):

    data = Event.objects.get(pk = id)
    total_reg = eventRegistration.objects.filter(event = data)
    comments = eventComments.objects.filter(event = data)[:5]
    
    previous_ratings = eventRating.objects.filter(event__name = data.name)
    #very_good = eventRating.objects.filter(event = data, rating = 'very good')
    registered = eventRegistration.objects.filter(event = data, user = request.user)
    percentage = 0

    updates = EventUpdates.objects.filter(event = data)

    """
    if (previous_ratings and very_good):
        percentage = (len(previous_ratings) / len(very_good)) * 100
    """

    cf = CommentForm()
    
    return render(request, "accounts/events-detail.html", {"data": data, "total_reg": len(total_reg), "form": cf, "comments": comments, 
        "registered": registered, "updates": updates})



@login_required
def eventRegister(request, event_id):
    
    event = Event.objects.get(pk=event_id)
    u = request.user
    userevents = eventRegistration.objects.filter(user = u, event = event)
    
    if (not userevents):

        register = eventRegistration(user = u, event= event)
        register.save()

        
 
        return JsonResponse({"status": 1})


@login_required
def reg_events(request):

    now = date.today()
    events_upcoming = eventRegistration.objects.filter(user = request.user).order_by("-id")

    return render(request, "accounts/reg-events.html", {"upcoming_events": events_upcoming})


@login_required
def eventsrating(request, id):
  
    if request.method == 'POST':

        form = RateForm(request.POST)

        if form.is_valid():

            ratings = form.cleaned_data['rate_field']
            event = Event.objects.get(id = id)

            bar = eventRating.objects.filter(event = event, user = request.user)

            if (len(bar) == 0):

                foo = eventRating.objects.create(event = event, user = request.user, rating = ratings)

                foo.save()
                messages.info(request, "Thanks for your feedback!")

                return redirect("index")
                

    else:

        return redirect("index")


#### JSEC'S <<<<<<<<<<<<<<<<<=====================================================================>>>>>>>>>>

@user_passes_test(lambda u: Group.objects.get(name='jsecs') in u.groups.all())
def dashboard(request):

    now = date.today()

    jsec = jSecs.objects.get(name = request.user)
    club = get_object_or_404(clubInfo, pk = jsec.club.id)
    members_list = Members.objects.filter(club = jsec.club.id)

    requests, created = WaitingArea.objects.get_or_create(club = club)

    clubs_rating, create = ClubRating.objects.get_or_create(club = club)

    interests = {}
    for i in members_list:

        grp = i.memname.groups.all()

        for j in grp.exclude(name = 'cosb'):


            if j.name not in ['cosb', 'jsecs']:

                if j in interests.keys():

                    interests[j] += 1

                else:

                    interests[j] = 1

        


    upcoming_events = Event.objects.filter(club = jsec.club.id, event_date__gte = now)

    total_participants = [len(eventRegistration.objects.filter(event = i)) for i in upcoming_events]
        
    return render(request, 'accounts/dashboard.html', {"members_list": members_list, "upcoming_events": zip(upcoming_events, total_participants), 
        "club_id": jsec.club.id, "club": club, "interests": interests, "requests": requests, "clubs_rating": clubs_rating})



@login_required
def allMem(request):

    template_name = "accounts/members.html"

@login_required
def  addEvent(request):


    if request.method == 'POST':

        form = EventForm(request.POST, request.FILES or None)

        j = jSecs.objects.get(name=request.user)
        if form.is_valid():
            #print(form.cleaned_data['poster'].image)
            #img = Image.open(form.cleaned_data['poster'])
            #print(img.width, img.height)
            event_data = Event(club = j.club, name = form.cleaned_data['name'], content=form.cleaned_data['content'], poster=form.cleaned_data['poster'], event_date = request.POST['event_date'], event_time=request.POST['event_time'])
            event_data.save()
            messages.success(request, "Event added.")
            return redirect("update-event")

    else:

        form = EventForm()
    
    return render(request, 'accounts/addevents.html', {"form": form})

@login_required
def update(request):

    j = jSecs.objects.get(name = request.user)

    events = Event.objects.filter(club = j.club.id).order_by("-id")

    return render(request, "accounts/updateevents.html", {"events": events})


@login_required
def EventUpdate(request, pk):

    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Event, id = pk)
 
    # pass the object as instance in form
    form = UpdateEventForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return redirect("event")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "accounts/updateeventform.html", context)

    """
    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff
    """
@login_required
def EventDelete(request, pk):

    obj = get_object_or_404(Event, id = pk)
    obj.delete()

    return render(request, "accounts/error.html", {"msg": "Event deleted successfuly."})

@login_required
def eventUpdates(request, event_id):


    msg = request.POST.get('msg')
    event = Event.objects.get(id = event_id)
    updates = EventUpdates(user = request.user, event = event, update = msg)

    updates.save()
    
    return redirect(f"/accounts/event-details/{event_id}/")


@login_required
def updates(request, eventid):


    return render(request, "accounts/events-updates.html", {"event_id": eventid})





### ADDITIONAL FEATURES <<<<<<<<<=================================================================>>>>>>>>>>>
@login_required
def search(request):

    if request.method == "POST":

        search_value = request.POST['search']

        get_searched = User.objects.filter(username__startswith = search_value[0:3])

        return render(request, "accounts/searchedmember.html", {"results": get_searched})

    else:

        return HttpResponseRedirect(reverse("members"))


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





@login_required
def searchclubmem(request, club_id):

    if request.method == "POST":

        club = clubInfo.objects.get(id = club_id)

        search_value = request.POST["search"]
        u = User.objects.filter(username__startswith = search_value[0:3])

        context = {}
        for i in u:
            context[i] = Members.objects.filter(memname = i)

        return render(request, "accounts/clubmembers.html", {"context": context})

@login_required
def cluster(request):

    if request.method == "POST":

        form = interestForm(request.POST)
        interest = request.POST['interest']

        try:
            g = Group.objects.get(name=interest)

        except:

            messages.info(request, "This cluster is not available currently.")
            return redirect("tasks")
        if form.is_valid():
            

            if g in request.user.groups.all():
                
                return render(request, "accounts/int.html", {"msg": "You are already in the Group"})

            else:

                f = Interest(user = request.user)
                f.save()
                request.user.groups.add(g)

                return redirect("tasks")

    else:

        form = interestForm()

    return render(request, "accounts/int.html", {"form": form})

@login_required
def searchCluster(request):


    form = SearchForm()
    searched = request.POST['search']
    cluster = Group.objects.get(name = searched)

    users = cluster.user_set.all()
    return render(request, "accounts/cluster.html", {"cluster": users, "form": form, "group_name": cluster.name})

@login_required
def clusterTag(request, tag):

    cluster = Group.objects.get(name = tag)

    users = cluster.user_set.all()
    return render(request, "accounts/cluster.html", {"cluster": users, "group_name": cluster.name})



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
def taskstatus(request, task_id):


    task = Task.objects.get(id = task_id)
    rate, created = UserRating.objects.get_or_create(user=request.user)

    if created:
        rate.rating = 10
        rate.save()


    taskstatus, create = TaskStatus.objects.get_or_create(user = request.user)
    done_before = TaskStatus.objects.filter(user=request.user, task=task)

    if len(done_before) == 0:
        taskstatus.task.add(task)

        foo, create = TaskRoom.objects.get_or_create(task = task)
        foo.user.add(request.user)

            
        rate.rating += 10
        rate.save()

        messages.success(request, "You have done one more task, Do more tasks to increase your ratings.")
        return redirect(f"/accounts/task-chat/{task_id}/")


    else:
        messages.success(request, "You have already done that task.")
        return redirect("tasks")
    


@login_required
def recentTasks(request):

    j = jSecs.objects.get(name = request.user)
    task_list = Task.objects.filter(club = j.club).order_by("-id")

    return render(request, "accounts/recent-tasks.html", {"task_list":task_list})



@login_required
def TaskUpdate(request, pk):

    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Task, id = pk)
 
    # pass the object as instance in form
    form = UpdateTaskForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        messages.success(request, "Task updated.")
        return redirect("recent-tasks")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "accounts/updatetaskform.html", context)


@login_required
def TaskDelete(request, pk):

    obj = get_object_or_404(Task, id = pk)
    obj.delete()

    messages.success(request, "Task deleted.")
    return redirect("recent-tasks")


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
def commentSave(request, id):

    data = Event.objects.get(pk = id)
    
    if request.method == 'POST':

        cf = CommentForm(request.POST)

        if cf.is_valid():
            comment = request.POST.get('comment')

            foo = eventComments.objects.create(user = request.user, event = data, comment = comment)
            foo.save()

            comment = eventComments.objects.values().filter(event = data, comment = comment)

            comments_data = list(comment)

            now = datetime.now()
            user = request.user.username
            return JsonResponse({"status": "save", "comments_data": comments_data, "now": now, "user": user})


        else:
            return JsonResponse({"status": 0})





@login_required
def rating(request):

    ratings, created = UserRating.objects.get_or_create(user = request.user)

    return render(request, "accounts/rating.html", {"ratings": ratings})

@login_required
def dataVisuals(request, id):

    students = Info.objects.all()
    event = Event.objects.get(id = id)
    total_participants = len(eventRegistration.objects.filter(event = event))
    total_users = len(User.objects.all())

    percentage_par = round((total_participants / total_users ) * 100)
    user = {}
    data_sem = {}

    for i in students:

        data = eventRegistration.objects.filter(user = i.user, event = event)

        if (len(data) != 0) and str(i.branch) not in user.keys():

            user[str(i.branch)] = 1

        elif (len(data) != 0) and (str(i.branch)) in user.keys():

            user[str(i.branch)] += 1

    for i in students:

        data = eventRegistration.objects.filter(user = i.user)

        if (len(data) != 0) and str(i.sem) not in data_sem.keys():

            data_sem[str(i.sem)] = 1
            print(i.sem)

        elif (len(data) != 0) and (str(i.sem)) in data_sem.keys():

            data_sem[str(i.sem)] += 1


    return render(request, "accounts/data.html", {"data_branch": user, "data_sem": data_sem, "total_par": total_participants, "per_par": percentage_par, "event_id": id})



@login_required
def allParticipants(request, id):

    par = eventRegistration.objects.filter(event = id)
    #print(request.mail)
    return render(request, "accounts/allpar.html", {"par": par})


class CommentJsonListView(View):

    def get(self, *args, **kwargs):


        upper = kwargs.get('number_comments')
        eventid = kwargs.get('eventid')
        lower = upper - 5
        username = []
        posts = list(eventComments.objects.filter(event = eventid).values()[lower:upper])


  
        for i in posts:

            u = User.objects.get(id = i['user_id'])
            username.append(u.username)

        posts_size = len(eventComments.objects.filter(event = eventid))
        max_size = True if upper >= posts_size else False
        return JsonResponse({'data': posts, 'max': max_size, 'username': username}, safe=False)

@login_required
def chatSave(request, id):

    room, created_room = TaskRoom.objects.get_or_create(task = id)
    task = Task.objects.get(id = int(id))
    chatroom = TaskChat.objects.filter(task = task)
    print(id)
    if request.method == 'POST':

        cf = ChatForm(request.POST)

        chat = request.POST['chat']
        foo = TaskChat(user = request.user, msg = chat, task = task)
        foo.save()
        now = datetime.now()
        user = request.user.username
        return JsonResponse({"status": "save", "now": now, "user": user})


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


    if request.method == 'POST':

        name = request.POST['name']
        logo = request.FILES.get('logo', 'blank')

        tag = request.POST['tag']

        #email = request.POST['email']
        tagline = request.POST['tagline']
        vision_and_mission = request.POST['vision_and_mission']


        club = clubInfo.objects.create(name = name, logo = logo, tag = tag, tagline = tagline, vision_and_mission = vision_and_mission)
        club.save()
        now = datetime.now()

        jsec = jSecs.objects.create(name = request.user, club = club)
        mem, created = Members.objects.get_or_create(memname = request.user)
        mem.club.add(club)
        mem.save()
        jsec.save()

        group = Group.objects.get(name = "jsecs")
        group.user_set.add(request.user)

        foo = Clubverification(club = club, is_verified = True)
        foo.save()
        messages.success(request, f"Welcome to {club.name}!")
        return redirect(f"/accounts/your-club/{club.id}/")


    else:
        return render(request, "accounts/club-registration.html")


@login_required
def club(request, club_id):

    club = clubInfo.objects.get(id = club_id)


    club_mem = club.clubs.all()
    foo = Members.objects.filter(club = club)
    mem, created = WaitingArea.objects.get_or_create(club = club)
    club_discussion = Task.objects.filter(club = club).order_by("-id")
    allclub = Members.objects.get(memname = request.user)
    members = []
    for i in club_mem:

        members.append(i.memname.username)

    ques = Question.objects.all().order_by("-id")
    club_questions = []

    for i in ques:
        user = i.user.username
        if user in members:
            club_questions.append(i)


    flag = False
    bar = club.jsecsclub.all()

    for i in bar:
        if str(i.name.username) == str(request.user.username):
            flag = True
            break

    return render(request, "accounts/clubs.html", {"club": club, "jsecs": club.jsecsclub.all(), "members": members, "questions": club_questions[:3], "club_discussion": club_discussion[:3], "flag": flag, "waiting_list": len(mem.user.all()), "allclub": allclub.club.all()})


@login_required
def club_discussion(request, club_id):

    club = clubInfo.objects.get(id = club_id)
    mem = Members.objects.get(memname = request.user)
    messages = Task.objects.filter(club = club_id).order_by("-id")
    print(mem.club.all())
    return render(request, "accounts/club-discussion.html", {"message": messages, "club_id": club_id, "club": club, "clubs": mem.club.all()})


@login_required
def taskform(request):

    if request.method == 'POST':

        tag = request.POST['tag']

        club_name = request.POST['club-name']
        club_id = clubInfo.objects.get(id = int(club_name))
        msg = request.POST['msg']
        task = Task(user = request.user, club = club_id, tag = tag, msg=msg)
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
        clubs = Clubverification.objects.filter(is_verified = True)
        return render(request, "accounts/allclub.html", {"clubs": clubs, "tag": "ALL"})

    clubs = Clubverification.objects.filter(club__tag = tag, is_verified = True)
    return render(request, "accounts/allclub.html", {"clubs": clubs, "tag": tag}) 



@login_required
def join_club(request, club_id):

    club = clubInfo.objects.get(id = club_id)
    wait, created = WaitingArea.objects.get_or_create(club = club)
    wait.user.add(request.user)
    return JsonResponse({"status": 1})



@login_required
def view_waitingarea(request, club_id):

    club = clubInfo.objects.get(id = club_id)
    members, created = WaitingArea.objects.get_or_create(club = club)
    mem = Members.objects.filter(club = club) 
    return render(request, "accounts/addmembers.html", {"members": members.user.all(), "club_id": club_id, "mem": mem, "club": club})


@login_required
def addmem(request, mem_id, club_id):

    member = User.objects.get(pk = mem_id)

    addmember, created = Members.objects.get_or_create(memname = member)
    club_name = clubInfo.objects.get(id = club_id)
    addmember.club.add(club_name)
    addmember.save()
    waiting, created = WaitingArea.objects.get_or_create(club = club_name)

    waiting.user.remove(member)

    return JsonResponse({"status": 1})

@login_required
def make_jsec(request, club_id, mem_id):

    club_name = clubInfo.objects.get(id = club_id)

    mem = User.objects.get(pk = mem_id)
    jsec = jSecs.objects.filter(club = club_name, name = mem)

    if jsec:

        messages.success(request, "Already a Jsec.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    new_jsec = jSecs.objects.create(club = club_name, name = mem)
    new_jsec.save()

    messages.success(request, "New Jsec added.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def removemem(request, mem_id, club_id):

    club = clubInfo.objects.get(id = club_id)
    u = User.objects.get(id = mem_id)
    mem = Members.objects.get(memname =  u, club = club)
    mem.club.remove(club)
    mem.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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


@login_required
def view_story(request, story_id):

    story = Story.objects.get(id = story_id)
    story.views = story.views + 1
    story.save()
    allclub = Members.objects.get(memname = request.user)

    return render(request, "accounts/story.html", {"story": story, "clubs": allclub.club.all()})


def delete_story(request, story_id):
    
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