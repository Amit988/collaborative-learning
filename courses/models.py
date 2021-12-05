
from django.db import models
from quizes.models import Quiz
from django.contrib.auth.models import User
import datetime
from quizes.models import Quiz
from django_resized import ResizedImageField
from taggit.managers import TaggableManager

class Course(models.Model):

	poster = ResizedImageField(size=[300, 300], upload_to = "images/")
	title = models.CharField(max_length = 3000)
	tag = TaggableManager()
	auther = models.ForeignKey(User, on_delete = models.CASCADE)
	duration = models.IntegerField(help_text = "In hours")
	discription = models.TextField()

	def __str__(self):
		return f"{self.title}"


class Lessons(models.Model):

	title = models.CharField(max_length = 3000)
	lesson_no = models.IntegerField()
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	video_url = models.SlugField()
	discription = models.TextField()
	quiz = models.ForeignKey(Quiz, on_delete = models.CASCADE, blank = True, null = True)
	duration = models.IntegerField(help_text = "In minutes")
	resources = models.TextField(blank = True, null = True)

	def __str__(self):
		return f"{self.course.title} -- {self.title} -- {self.lesson_no}"



class About(models.Model):
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	details = models.TextField()


	def __str__(self):
		return f"{self.course.title}-about"