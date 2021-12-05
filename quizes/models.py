# Create your models here.
from django.db import models
from accounts.models import clubInfo
import random
from django_resized import ResizedImageField

DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)

class Quiz(models.Model):
    #connect it to club's
    club = models.ForeignKey(clubInfo, on_delete=models.CASCADE)
    img = ResizedImageField(size=[300, 300],upload_to="quiz_poster/")
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text="required score in %")
    difficluty = models.CharField(max_length=6, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]


    class  Meta:
    	verbose_name_plural = "Quizes"
    		