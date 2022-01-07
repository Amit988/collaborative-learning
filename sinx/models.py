from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
#from PIL import Image
from django_resized import ResizedImageField
from taggit.managers import TaggableManager


class Course(models.Model):

	name = models.CharField(max_length = 1000)
	author = models.CharField(max_length = 1000)
	tags = TaggableManager(related_name="course_tags")
	description = models.CharField(max_length = 5000)
	image = ResizedImageField(size=[300, 300], upload_to = "images/", null = True, blank = True)
	about = models.TextField(null = True, blank = True)
	link = models.URLField(max_length = 2000)
	overall_rating = models.IntegerField(default = 0)


	def __str__(self):

		return f"{self.name}"

	class  Meta:

		verbose_name_plural = "Courses-sinx"
		ordering = ["-overall_rating"]

class CourseDetail(models.Model):


	CHOICES = (

		('Videos', 'Videos'),
		('Textual', 'Textual'),
		('Hybrid', 'Hybrid'),
	)

	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_details")
	price = models.IntegerField(default = 0)
	catagory = models.CharField(max_length = 250, default="Computer Science")
	platform = models.CharField(max_length = 1000, default="YouTube")
	released_date = models.DateField(null = True, blank = True)
	country = models.CharField(max_length = 1000, default="India")
	language = models.CharField(max_length = 250, default="English")
	price = models.IntegerField(default = 0)
	duration = models.IntegerField(default=4)
	certificate = models.BooleanField(default = False)
	material_type = models.CharField(max_length = 25, choices = CHOICES, default="Videos")
	added_by = models.CharField(max_length = 1000, default="Neesham")


	def __str__(self):

		return f"{self.course.name}--Details"

	class  Meta:
		verbose_name_plural = "Courses-details"
		

class Rating(models.Model):

	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	review = models.CharField(max_length = 3000, null = True, blank = True)
	rating = models.IntegerField(default = 0)

	def __str__(self):

		return f"{self.user.username} rate {self.course.name} {self.rating}"

	class  Meta:

		verbose_name_plural = "Course-Ratings"


class TotalRating(models.Model):
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	total_rating = models.IntegerField(default = 0)

	def __str__(self):

		return f"{self.course.name} has {self.total_rating} rating."