from django.shortcuts import render, redirect
from course_diary.models import Course, Rating, TotalRating, Watchlist, ShareCourse
from django.http import HttpResponseRedirect, request, HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from accounts.models import Members, clubInfo
from .forms import ShareForm
# Create your views here.

def all_courses(request):

	courses = Course.objects.all()
	return render(request, "course_diary/courses.html", {"courses": courses})


def course_overview(request, course_id):

	course = Course.objects.get(id = course_id)
	
	added = False

	clubs = ""

	if request.user.is_authenticated:

		watchlist = Watchlist.objects.filter(user = request.user, courses=course)

		member, created = Members.objects.get_or_create(memname = request.user)

		clubs = member.club.all()

		if watchlist:
			added = True

	form = ShareForm()

	reviews = Rating.objects.filter(course = course)
	return render(request, "course_diary/course-rating.html", {"course": course, "reviews": reviews, "added": added, 'clubs': clubs, "form": form})


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

@login_required
def add_to_watchlist(request, course_id):

	course = Course.objects.get(id = course_id)
	watchlist, created = Watchlist.objects.get_or_create(user = request.user, courses = course)

	return JsonResponse({"status": 1})

@login_required
def view_watchlist(request):

	courses = Watchlist.objects.filter(user = request.user)
	return render(request, "course_diary/courses.html", {"watchlist_courses": courses, "watchlist": True})


def share(request, course_id):

	if request.method == 'POST':

		form = ShareForm(request.POST)

		if form.is_valid():

			course = Course.objects.get(id = course_id)
			club_id = request.POST['club-name']
			club = clubInfo.objects.get(id = club_id)
			msg = request.POST['message']
			data = ShareCourse.objects.create(user = request.user, msg = msg, course = course, club = club)
			data.save()

			return redirect(f"/accounts/your-club/{club_id}/")

@login_required
def delete_shared_course(request, course_id, club_id):

	shared_course = ShareCourse.objects.get(id = course_id)

	if request.user == shared_course.user:

		shared_course.delete()

		messages.success(request, "Deleted Successfully.")
		return redirect(f"/accounts/your-club/{club_id}/")

	else:

		messages.success(request, "You don't have permissions to delete it.")
		return redirect(f"/accounts/your-club/{club_id}/")

@login_required
def manage_watchlist(request, course_id):

	course = Watchlist.objects.filter(courses = course_id, user = request.user)

	for i in course:

		i.delete()

	return redirect("sinx:view-watchlist")