from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Story, ReportClub, ContentCreator, Visitors, WaitingArea, EventUpdates, Clubverification,  Feedbacks, TaskRoom, TaskChat, clubInfo, jSecs, Members, Event, eventRegistration, Task, Interest, Info, TaskStatus, UserRating, eventRating, eventComments

# Register your models here.
class EventAdmin(SummernoteModelAdmin):

    summernote_fields = ('content',)

admin.site.register(Event, EventAdmin)
admin.site.register(clubInfo)
admin.site.register(jSecs)
admin.site.register(Members)
admin.site.register(eventRegistration)
admin.site.register(Task)
#admin.site.register(Interest)
admin.site.register(Info)
#admin.site.register(TaskStatus)
#admin.site.register(UserRating)
#admin.site.register(eventRating)
admin.site.register(eventComments)
admin.site.register(TaskChat)
#admin.site.register(TaskRoom)
admin.site.register(Feedbacks)
admin.site.register(Clubverification)
admin.site.register(EventUpdates)
admin.site.register(WaitingArea)
admin.site.register(Visitors)
admin.site.register(ContentCreator)
admin.site.register(ReportClub)
admin.site.register(Story)