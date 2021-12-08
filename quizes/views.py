

# Create your views here.
from django.shortcuts import render
from .models import Quiz
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question, Answer
from results.models import Result
import statistics
from .forms import QuizFormSet, QuestionForm, AnswerForm
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

def  QuizListView(request):

    quiz  = Quiz.objects.all()
    recent = Result.objects.filter(user = request.user).order_by("-id")[:3] 

    return render(request, 'quizes/main.html', {"object_list": quiz, "recent_quizzes": recent})

@login_required
def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quiz.html', {'obj': quiz})

@login_required
def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })

@login_required
def save_quiz_view(request, pk):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})
            
        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})

@login_required
def RecentQuizzes(request):

    recent = Result.objects.filter(user = request.user)

    data = []
    for i in recent:

        foo = Result.objects.filter(quiz = i.quiz)

        scores = [i.score for i in foo]

        data.append((len(foo), round(statistics.mean(scores))))

    return render(request, "quizes/recent-quiz.html", {"recent": zip(recent, data)})


def quizform(request):


    form = QuizFormSet()
    form1 = QuestionForm()
    form2 = AnswerForm()


    return render(request, "quizes/quizform.html", {"form": form, "form1": form1, "form2": form2})


class TestCreate(CreateView):


    def get(self, request, *args, **kwargs):
        context = {
          'form': QuestionForm(), # form used to create model_A instance(s)
          'formset': QuizFormSet(), # formset for create model_B instace(s) linked to that model_A instace
        }

        return render(request, 'quizes/quizform.html', context)


    def post(self, request, *args, **kwargs):
        # if our ajax is calling so we have to take action
        # because this is not the form submition
        if request.is_ajax():
            cp = request.POST.copy() # because we couldn't change fields values directly in request.POST
            value = int(cp['wtd']) # figure out if the process is addition or deletion
            prefix = "answers" # whatever your related_name is
            cp[f'{prefix}-TOTAL_FORMS'] = int(
                cp[f'{prefix}-TOTAL_FORMS']) + value
            formset = QuizFormSet(cp) # catch any data which were in the previous formsets and deliver to-
              # the new formsetes again -> if the process is addition!
            return render(request, 'quizes/formset.html', {'formset': formset})

        form = QuestionForm(request.POST)
        formset = QuizFormSet(request.POST or None)
        theres_no_error = True # a good tip, you'll see ;)
        # important note: check any desired validation of formset here and it's helpful
        # to prevent save model_A instance if formset contains invalid data which-
        # means connected model_B instance(s) wont be created

        """
        if formset.is_valid():

           
            for subform in formset:
              if subform.cleaned_data['custom_field'] is not valid_in_your_opinion: # the formset is valid but-
                # you want to check something if you'relike me crazy
                theres_no_error = False
                subform.full_clean()
                subform.errors['custom_field'] = subform.error_class(["yor message to show error"])"""

        print(form.is_valid(), formset.is_valid())
        
        if form.is_valid() and theres_no_error and formset.is_valid(): # if formsets are valid too! :)
            form.save()

            for subform in formset:

                subform.save()

