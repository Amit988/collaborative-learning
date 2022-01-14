from django.contrib import admin
from .models import Question, Answere, ClubQuestion
# Register your models here.

admin.site.register(Question)
admin.site.register(Answere)
admin.site.register(ClubQuestion)