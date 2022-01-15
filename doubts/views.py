
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, time, date
from .models import Question, Answere, ClubQuestion, ClubQuestionAnswere
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import eventRegistration, Members, clubInfo
from .forms import QuestionForm, AnswereForm, UpdateAnswereForm, UpdateQuestionForm, QuestionSearchForm
from django.http import HttpResponseRedirect, request, HttpResponse, JsonResponse
# Create your views here.


####### Questions ==============================================================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def clubQuestions(request, club_id):

    club = clubInfo.objects.get(id = club_id)
    
    club_questions = ClubQuestion.objects.filter(club = club)

    form = QuestionForm()

    member, created = Members.objects.get_or_create(memname = request.user)

    user_clubs = member.club.all()


    if request.method == 'POST':

        form = QuestionForm(request.POST)

        if form.is_valid():

            title = form.cleaned_data['title']
            tags = form.cleaned_data['tag']
            detail = form.cleaned_data['detail']
            club_id = request.POST['club-name']
            club = clubInfo.objects.get(id = club_id)

            question = ClubQuestion.objects.create(user = request.user, club = club, title = title, tag = tags, detail = detail)
            question.save()

            return redirect(f"/qna/club-qna/{club_id}/")

    return render(request, "qna/club-qna.html", {"questions": club_questions, "club_id": club_id, "form": form, "user_clubs": user_clubs})





def deleteQuestion(request, pk):
    
    obj = get_object_or_404(ClubQuestion, id = pk)

    if obj.user == request.user:
        obj.delete()
        return redirect("qna:your-question-view")

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def updateQuestion(request, pk):

    context ={}

    obj = get_object_or_404(ClubQuestion, id = pk)

    form = UpdateQuestionForm(request.POST or None, instance = obj)

    user_clubs, created = Members.objects.get_or_create(memname = request.user)

    if request.method == 'POST':


        if form.is_valid():

            tags, title, detail, club_id = form.cleaned_data['tag'], form.cleaned_data['title'], form.cleaned_data['detail'], request.POST['club-name']

            club = clubInfo.objects.get(id = club_id)

            question = ClubQuestion.objects.create(user = request.user, tag = tags, title = title, detail = detail, club = club)

            messages.success(request, "Question updated.")
            return redirect(f"/qna/add-answere/{pk}/")
 

    return render(request, "qna/questionform.html", {"form": form, "user_clubs": user_clubs.club.all()})





##### Answeres =====================================================================================>>>>>>>>>>>>>>>>>>

def addAnswere(request, id):

    question = ClubQuestion.objects.get(id = id)
    a = ClubQuestionAnswere.objects.filter(question=question, parent = None)
    replies = ClubQuestionAnswere.objects.filter(question = question).exclude(parent = None)

    replyDict={}
    form = UpdateAnswereForm()
    for reply in replies:

        if reply.parent.id not in replyDict.keys():
            replyDict[reply.parent.id]=[reply]
        else:
            replyDict[reply.parent.id].append(reply)

    if request.method == 'POST':
        
        form = UpdateAnswereForm(request.POST or None)

        if form.is_valid():

            user = request.user
            parentSno = request.POST.get('parent')
            parent_ans = request.POST.get('parent_ans')


            if parentSno == "ans":  
                foo = form.cleaned_data['ans']
                        
                ans  = ClubQuestionAnswere(ans = foo, user = user, question = question)
                ans.save()
                messages.success(request, "Your ans has been posted successfully")

            elif parent_ans:

                foo = request.POST.get('answer1', 'blank')
                parent = ClubQuestionAnswere.objects.get(id = parent_ans)
                reply = ClubQuestionAnswere(ans = foo, user = user, question = question, parent = parent)
                reply.save()

                messages.success(request, "Your reply has been posted successfully")


            replies = ClubQuestionAnswere.objects.filter(question = question).exclude(parent = None)

            replyDict={}

            for reply in replies:

                if reply.parent.id not in replyDict.keys():
                    replyDict[reply.parent.id]=[reply]
                else:
                    replyDict[reply.parent.id].append(reply)
                    
            #ajax
            return render(request, "qna/answereform.html", {"i": question, "answeres": a, "total_q": len(a), "replyDict": replyDict, "form": form})

    return render(request, "qna/answereform.html", {"i": question, "answeres": a, "total_q": len(a), "replyDict": replyDict, "form": form})



def updateAnswere(request, pk):


    context ={}
    obj = get_object_or_404(ClubQuestionAnswere, id = pk)
    form = UpdateAnswereForm(request.POST or None, instance = obj) 


    if form.is_valid():
        form.save()
        return redirect(f"/qna/add-answere/{obj.question.id}/")       

    return render(request, "qna/answere-update-form.html", {"form": form})




def deleteAnswere(request, pk):
    
    obj = get_object_or_404(ClubQuestionAnswere, id = pk)

    if obj.user == request.user:
        obj.delete()
        return redirect("qna:your-answer-view")

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def userQuestion(request):

    questions = ClubQuestion.objects.filter(user=request.user)
    return render(request, "qna/yourquestion.html", {"questions": questions})



def userAnswer(request):

    ans = ClubQuestionAnswere.objects.filter(user = request.user)
    return render(request, "qna/yourans.html", {"ans": ans})