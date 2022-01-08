from django.shortcuts import render
from course_diary.models import Course, Rating, TotalRating
from django.http import HttpResponseRedirect, request, HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.

def all_courses(request):

	courses = Course.objects.all()
	return render(request, "course_diary/courses.html", {"courses": courses})


def course_overview(request, course_id):

	course = Course.objects.get(id = course_id)
	reviews = Rating.objects.filter(course = course)
	return render(request, "course_diary/course-rating.html", {"course": course, "reviews": reviews})


def course_rating(request, course_id):

	if request.method == 'POST':

		rating, review = request.POST['rating'], request.POST['review']

		course = Course.objects.get(id = course_id)
		foo, created = Rating.objects.get_or_create(course = course, user = request.user)
		total, created = TotalRating.objects.get_or_create(course = course)

		bar = Rating.objects.filter(course = course)
	
		if created:
			print(rating)
			foo.rating = int(rating)
			foo.review = review
			foo.save()

			total.total_rating += int(rating)
			total.save()

			per = (total.total_rating) / (len(bar))
			course.overall_rating = per
			course.save()

			messages.success(request, "Thanks for rating this course!")
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

		messages.success(request, "You can only rate once.")
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def search_courses(request):

	if request.method == 'POST':

		tag = request.POST['course-tag'].lower()

		query = Course.objects.filter(tags__name__in = [tag])
		flag1 = False


		if len(query) == 0:
			flag1 = True



		return render(request, "course_diary/courses.html", {"courses": query, "flag": True, "flag1": flag1})


def search_courses_by_tag(request, tag):


	query = Course.objects.filter(tags__name__in = [tag])
	flag1 = False


	if len(query) == 0:
		flag1 = True

	return render(request, "course_diary/courses.html", {"courses": query, "flag": True, "flag1": flag1})