from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from taggit.managers import TaggableManager
# Create your models here.

class Question(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = TaggableManager()
    title = models.CharField(max_length=2000)
    detail = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null = True)
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = "Questions"

class Answere(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ans = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f"{self.question.title}"

    class Meta:
        verbose_name_plural = "Answeres"