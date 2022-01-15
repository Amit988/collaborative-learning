from django.contrib import admin
from diary.models import Course, Rating, TotalRating, Watchlist, ShareCourse



admin.site.register(Course)
admin.site.register(Rating)
admin.site.register(TotalRating)
admin.site.register(Watchlist)
admin.site.register(ShareCourse)
