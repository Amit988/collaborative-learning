
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, time, date
from .models import Course, Lessons, About
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.models import User
from accounts.models import eventRegistration
from django.http import HttpResponseRedirect, request, HttpResponse, JsonResponse
from qna.models import Question


def view_courses(request):

	all_courses = Course.objects.all()
	return render(request, "courses/courses.html", {"crs": all_courses})


@login_required
def course_lessons(request, course_id):
	course = Course.objects.get(id = course_id)
	lessons = Lessons.objects.filter(course = course).order_by("lesson_no")
	about, created = About.objects.get_or_create(course = course)

	return render(request, "courses/lessons.html", {"lessons": lessons, "course": course, "about": about})


@login_required
def lesson_video(request, link, course_id, lesson_id):

	course = Course.objects.get(id = course_id)
	lessons = Lessons.objects.filter(course = course).order_by("lesson_no")
	lesson = Lessons.objects.get(id = lesson_id)
	return render(request, "courses/lesson-video.html", {"video_link": link, "course": course, "lessons": lessons, "lesson": lesson})


@login_required
def course_qna(request, course_id):

	course = Course.objects.get(id = course_id)
	questions = Question.objects.filter(course = course).order_by("-id")

	return render(request, "courses/course_qna.html", {"questions": questions, "course_id": course_id})


@login_required
def addQuestion(request, course_id):



	if request.method == 'POST':

	    course = Course.objects.get(id = course_id)

	    tags, title, detail = request.POST['tag'], request.POST['title'], request.POST['details']
	    foo = tags.split(",")
	    q = Question.objects.create(user = request.user, title = title, detail=detail, course = course)

	    for i in foo:
	    	q.tag.add(i)

	    q.save()

	    return redirect(f"/courses/course-qna/{course_id}")

		
	return render(request, "courses/course_qna.html", {"course_id": course_id})
    
    
