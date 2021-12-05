from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.utils import timezone
from datetime import datetime
from PIL import Image
from django_resized import ResizedImageField
#import StringIO
# Create your models here.
class Info(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default="")
    course = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    sem = models.CharField(max_length=20)
    phone = models.CharField(max_length=10, blank = True)
    is_verified = models.CharField(max_length=3, default = "NO")
    auth_token = models.CharField(max_length=100, default="nothing")

    def __str__(self):
        return f"Info about {self.user.username}"

    class  Meta:

    	verbose_name_plural = "Extrainfo-about-user"


class clubInfo(models.Model):


    name = models.CharField(max_length=255)
    dateoffound = models.DateTimeField(auto_now_add=True)
    logo = ResizedImageField(size=[300, 300], upload_to = "images/")
    vision_and_mission = models.TextField(null = True, blank = True)
    tag = models.CharField(max_length=1000, default="ALL")
    tagline = models.CharField(max_length = 1000, null = True, blank=True)


    def __str__(self):
        return self.name


    class  Meta:
    	verbose_name_plural = "Club-Info"

class Clubverification(models.Model):
    club = models.OneToOneField(clubInfo, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    clg = models.CharField(max_length=1000, default = "Not Required")
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.club.name} is Verified!"

    class  Meta:
        verbose_name_plural = "Verified Clubs"

   
class jSecs(models.Model):

    name = models.ForeignKey(User, on_delete = models.CASCADE)
    club = models.ForeignKey(clubInfo, on_delete = models.CASCADE, related_name="jsecsclub")
    year = models.DateField(null = True, blank = True)

    def __str__(self):
        return f"{self.name} jsec of {self.club.name}"

    
    class  Meta:
    	verbose_name_plural = "Jsec's"


class Members(models.Model):

    memname = models.ForeignKey(User, on_delete = models.CASCADE, related_name="memberofclubs")

    #manytomanyfield doesnt have models.CASCADE
    club = models.ManyToManyField(clubInfo, blank=True,  related_name = "clubs")

    def __str__(self):

        foo = self.club.all()
        clubs = []
        for i in foo:
            clubs.append(i.name)
        return f"{self.memname} is a member of {clubs}"

    
    class  Meta:
    	verbose_name_plural = "Member's"


class WaitingArea(models.Model):

    user = models.ManyToManyField(User)
    club = models.ForeignKey(clubInfo, on_delete = models.CASCADE)
    accepted = models.BooleanField(default = False)

    def __str__(self):

        foo = self.user.all()
        users = []

        for i in foo:
            users.append(i.username)

        return f"{users} are waiting for {self.club.name}"

    class  Meta:
        verbose_name_plural = "Waiting-Area"


class Event(models.Model):

    club = models.ForeignKey(clubInfo, on_delete=models.CASCADE, related_name="clubevents")
    name = models.CharField(max_length=500, blank=False, null=False, default="DigiWeek")
    content = models.TextField()
    poster = ResizedImageField(size=[300, 300], upload_to="posters/")
    
    event_date = models.DateField(blank=True, null=True)
    event_time = models.TimeField(default=datetime.now(), null=True, blank=True)


    def __str__(self):
        return f"{self.name} Organized by {self.club.name}!"

    class  Meta:
        verbose_name_plural = "Events"


class eventRegistration(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userevents")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="events")
    #club = models.ManyToManyField(clubInfo)

    def __str__(self):
        foo = eventRegistration.objects.filter(event = self.event)
        return f"{len(foo)} users are registered for {self.event.name}"

    class  Meta:
        verbose_name_plural = "Event-Registrations"

class eventComments(models.Model):

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        foo = eventComments.objects.filter(event = self.event)
        return f"{len(foo)} users commented on {self.event.name}"

    class  Meta:
        verbose_name_plural = "Event-Comments"

#Not in use currently!
class eventRating(models.Model):

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default = 10)


    def __str__(self):
        return f"{self.user.username} rate event {self.event.name} ({self.rating})."

#Not is use currently!
class ClubRating(models.Model):

    club = models.ForeignKey(clubInfo, on_delete = models.CASCADE)
    rating = models.IntegerField(default = 10)

    def __str__(self):
        return f"{self.club.name} has {self.rating} Points."


class EventUpdates(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    update = models.TextField(null = False)
    time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.event.name} -- {self.update[:30]}"

    class  Meta:
        verbose_name_plural = "Event-Updates"

class Task(models.Model):

    TAG_CHOICES = [

        ("web-development", "web-development"),
        ("machine-learning", "machine-learning"),
        ("android-development", "android-development"),
        ("designing", "designing"),
        ("video-editing", "video-editing"),
        ("content-writting", "content-writting"),
        ("marketing", "marketing"),
        ("cosb", "cosb"),
    ]

    #title = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # only users clubs
    club = models.ForeignKey(clubInfo, on_delete = models.CASCADE, default="cosb", related_name="clubstask")
    tag = models.CharField(max_length=255, choices=TAG_CHOICES)
    time = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateField(default = timezone.now(), blank = True, null=True)
    deadline_time = models.TimeField(default=timezone.now(),  null=True, blank=True)
    msg = models.TextField()

    def __str__(self):
        return f"{self.user.username} -- {self.club.name} -- {self.msg}"

    class  Meta:
        verbose_name_plural = "Club-Discussions"


class TaskView(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    task = models.ForeignKey(Task, on_delete = models.CASCADE, related_name = "taskviews")
    time_stamp = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return f"{self.user.username}-seen-{self.task.msg}"

#Not in use currently!
class TaskRoom(models.Model):
    task = models.OneToOneField(Task, on_delete = models.CASCADE)
    user = models.ManyToManyField(User)


class TaskChat(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    msg = models.TextField()
    time = models.DateTimeField(auto_now_add = True)
    task = models.ForeignKey(Task, on_delete = models.CASCADE, null = True)

    def __str__(self):
        return f"{self.user.username} -- {self.msg[:30]}"

    class  Meta:
        verbose_name_plural = "Club-Discussions-Updates"

#Not in use currently!
class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.CharField(max_length=500)

#Not in use currently!
class  TaskStatus(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ManyToManyField(Task, related_name="done")
    status = models.BooleanField(blank=True, default=False, null=True)

    class  Meta:
    	verbose_name_plural = "Task-status"
     

#Not in use currently!   
class UserRating(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0 , blank=True)
        
    def __str__(self):
        return f"{self.user.username} has {self.rating} rating."


class Feedbacks(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s feedback!"

    class  Meta:
        verbose_name_plural = "Feedbacks"


class Visitors(models.Model):
    """docstring for Visitors"""

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        
        foo = Visitors.objects.all()
        return f"{len(foo)} visitors"

    class Meta:
        verbose_name_plural = "Visitors"


  

class ContentCreator(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    email = models.EmailField(max_length = 255)
    msg = models.TextField()

    def __str__(self):
        return f"{self.user.username}"


class ReportClub(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    club = models.ForeignKey(clubInfo, on_delete = models.CASCADE)
    msg = models.TextField()
