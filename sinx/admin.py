from django.contrib import admin
from sinx.models import Course, Rating, TotalRating
# Register your models here.

admin.site.register(Course)
admin.site.register(Rating)
admin.site.register(TotalRating)