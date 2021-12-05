from django.db import models
from quizes.models import Quiz
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Result(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add = True, blank = True)
	score = models.FloatField()

	def __str__(self):

		return f"{self.user} got {self.score}"