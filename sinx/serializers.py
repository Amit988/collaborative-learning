from rest_framework import serializers
from sinx.models import Course


class CourseSerializer(serializers.ModelSerializer):

	class Meta:
		model = Course
		fields = ['id', 'name', 'author', 'description', 'image', 'about', 'link', 'overall_rating']
