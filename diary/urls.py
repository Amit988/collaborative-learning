from django.urls import path
from . import views
app_name = 'sinx'

urlpatterns = [

	
	path("", views.all_courses, name = "sinx"),
	path("overview/<int:course_id>/", views.course_overview, name = "course-overview"),
	path("rate/<int:course_id>/", views.course_rating, name = "course-rating"),
	path("search-courses/", views.search_courses, name = "search-courses"),
	path("search-courses/<str:tag>/", views.search_courses_by_tag, name = "search-courses-by-tag"),
	path("add-to-watchlist/<int:course_id>/", views.add_to_watchlist, name = "add-to-watchlist"),
	path("view-watchlist/", views.view_watchlist, name = "view-watchlist"),
	path("share-course/<int:course_id>/", views.share, name = "share"),
	path("delete-shared-course/<int:course_id>/<int:club_id>/", views.delete_shared_course, name = "delete-shared-course"),
	path("delete-from-watchlist/<int:course_id>/", views.manage_watchlist, name = "delete-from-watchlist"),



]