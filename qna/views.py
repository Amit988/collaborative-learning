from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, time, date
from .models import Question, Answere
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import eventRegistration, Members, clubInfo
from .forms import QuestionForm, AnswereForm, UpdateAnswereForm, UpdateQuestionForm, QuestionSearchForm
from django.http import HttpResponseRedirect, request, HttpResponse, JsonResponse
# Create your views here.


####### Questions ==============================================================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def questionListView(request):

    user = request.user
    q = Question.objects.filter(tag__in = user.groups.all())
    now = datetime.now()
    tag_form = QuestionSearchForm()
   
    events_upcoming = eventRegistration.objects.filter(user = request.user, event__event_date__gte = now).order_by("-id")
    
    return render(request, "qna/questionlist.html", {"questions": Question.objects.all().order_by("-id"),  
        "events_upcoming": events_upcoming, "tag_form": tag_form})

def allQuestionView(request):

    q = Question.objects.all()

    return render(request, "qna/allquestions.html", {"questions": q})

def addQuestion(request, club_id):
    
    
    if request.method == 'POST':


        tags, title, detail = request.POST['tag'], request.POST['title'], request.POST['details']
        
        foo = tags.split(",")

        q = Question.objects.create(user = request.user, title = title, detail=detail)

        for i in foo:
            q.tag.add(i)

        q.save()
        print("Hello")
        return redirect(f"/qna/club-qna/{club_id}")

    return redirect(f"/qna/club-qna/{club_id}")

def deleteQuestion(request, pk):
    
    obj = get_object_or_404(Question, id = pk)
    obj.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def updateQuestion(request, pk):

    context ={}
    obj = get_object_or_404(Question, id = pk)
    form = UpdateQuestionForm(request.POST or None, instance = obj)

    if request.method == 'POST':

        tags, title, detail = request.POST['tag'], request.POST['title'], request.POST['detail']
        
        foo = tags.split(",")

        q, created = Question.objects.get_or_create(id = pk)

        q.title = title
        q.detail = detail

        for i in foo:
            q.tag.add(i)

        q.save()

        return redirect("qna:your-question-view")
 

    return render(request, "qna/questionform.html", {"form": form})


def questionTags(request, tag):


    questions = Question.objects.values().filter(tag = tag)
    users = []



    for i in questions:

        u = User.objects.values().get(pk = i['user_id'])

        users.append(u)


    return JsonResponse({"questions": list(questions), "users": list(users)})


class QuestionJsonListView(View):

    def get(self, *args, **kwargs):


        upper = kwargs.get('visible')
        #eventid = kwargs.get('eventid')
        lower = upper - 5
        username = []
        questions = list(Question.objects.all().order_by("-id").values()[lower:upper])

        users = []



        for i in questions:

            u = User.objects.values().get(pk = i['user_id'])

            users.append(u)
  


        questions_size = len(Question.objects.all())
        max_size = True if upper >= questions_size else False

        return JsonResponse({'data': questions, 'max': max_size, 'users': list(users)}, safe=False)


def clubQuestions(request, club_id):

    club = clubInfo.objects.get(id = club_id)
    club_mem = club.clubs.all()

    members = []
    for i in club_mem:
        members.append(i.memname.username)

    ques = Question.objects.all().order_by("-id")
    club_questions = []

    for i in ques:
        user = i.user.username
        if user in members:
            club_questions.append(i)

    return render(request, "qna/club-qna.html", {"questions": club_questions, "club_id": club_id})



##### Answeres =====================================================================================>>>>>>>>>>>>>>>>>>

def addAnswere(request, id):

    question = Question.objects.get(id = id)
    a = Answere.objects.filter(question=question, parent = None)
    replies = Answere.objects.filter(question = question).exclude(parent = None)

    replyDict={}

    for reply in replies:

        if reply.parent.id not in replyDict.keys():
            replyDict[reply.parent.id]=[reply]
        else:
            replyDict[reply.parent.id].append(reply)

    if request.method == 'POST':
        
        user = request.user
        parentSno = request.POST.get('parent')
        parent_ans = request.POST.get('parent_ans')


        if parentSno == "ans":  
            foo = request.POST.get('answer', 'blank')         
            ans  = Answere(ans = foo, user = user, question = question)
            ans.save()
            messages.success(request, "Your ans has been posted successfully")

        elif parent_ans:

            foo = request.POST.get('answer1', 'blank')
            parent = Answere.objects.get(id = parent_ans)
            reply = Answere(ans = foo, user = user, question = question, parent = parent)
            reply.save()

            messages.success(request, "Your reply has been posted successfully")


        replies = Answere.objects.filter(question = question).exclude(parent = None)

        replyDict={}

        for reply in replies:

            if reply.parent.id not in replyDict.keys():
                replyDict[reply.parent.id]=[reply]
            else:
                replyDict[reply.parent.id].append(reply)
                
        #ajax
        return render(request, "qna/answereform.html", {"i": question, "answeres": a, "total_q": len(a), "replyDict": replyDict})

    return render(request, "qna/answereform.html", {"i": question, "answeres": a, "total_q": len(a), "replyDict": replyDict})

def updateAnswere(request, pk):


    context ={}
    obj = get_object_or_404(Answere, id = pk)
    form = UpdateAnswereForm(request.POST or None, instance = obj)

    if form.is_valid():
        form.save()
        return redirect("qna:your-answer-view")
        

    context["form"] = form
    return render(request, "qna/answere-update-form.html", context)

def deleteAnswere(request, pk):
    
    obj = Answere.objects.filter(id = pk)
    obj.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def userQuestion(request):

    questions = Question.objects.filter(user=request.user)
    return render(request, "qna/yourquestion.html", {"questions": questions})

def userAnswer(request):

    ans = Answere.objects.filter(user = request.user)
    return render(request, "qna/yourans.html", {"ans": ans})