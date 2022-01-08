from django.urls import path
from . import views
app_name = 'sinx'

urlpatterns = [

	
	path("", views.all_courses, name = "sinx"),
	path("overview/<int:course_id>/", views.course_overview, name = "course-overview"),
	path("rate/<int:course_id>/", views.course_rating, name = "course-rating"),
	path("search-courses/", views.search_courses, name = "search-courses"),
	path("search-courses/<str:tag>/", views.search_courses_by_tag, name = "search-courses-by-tag"),


]