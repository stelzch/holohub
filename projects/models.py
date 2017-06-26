from django.db import models
from django.contrib.auth.models import User

class Figure(models.Model):
	title = models.CharField(max_length=255)
	op = models.ForeignKey(User, related_name='figure_op')
	file = models.ImageField(upload_to='uploads/figures/')

class HoloProject(models.Model):
	""" A short title of the project."""
	title = models.CharField(max_length=255)

	""" A more detailed description."""
	description = models.TextField()

	""" The projects source code."""
	code = models.TextField()

	""" The input image (capture image)."""
	image = models.ImageField(upload_to='uploads/captures/', blank=True)

	""" The output figures the code produces when running on the figures."""
	figures = models.ManyToManyField(Figure, related_name='figure')

	""" The original zip file. """
	file = models.FileField(upload_to='uploads/projects/')

	""" The original poster/creator of this post. """
	op = models.ForeignKey(User, related_name='op')

	""" The users which down/upvoted this post. """
	upvoters = models.ManyToManyField(User, related_name='upvoter')
	downvoters = models.ManyToManyField(User, related_name='downvoter')

	""" Automatically generated timestamps."""
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
