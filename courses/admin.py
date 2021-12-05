from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Course, Lessons, About
# Register your models here.

class LessonsAdmin(SummernoteModelAdmin):
    summernote_fields = ('resources',)


class AboutAdmin(SummernoteModelAdmin):

	summernote_fields = ('details',)

admin.site.register(Course)
admin.site.register(Lessons, LessonsAdmin)
admin.site.register(About, AboutAdmin)