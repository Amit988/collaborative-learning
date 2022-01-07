from django.contrib import admin
from sinx.models import Course, Rating, TotalRating, CourseDetail
# Register your models here.

class CourseInline(admin.TabularInline):
    model = CourseDetail

class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseInline]

admin.site.register(Course, CourseAdmin)
admin.site.register(Rating)
admin.site.register(TotalRating)
admin.site.register(CourseDetail)
