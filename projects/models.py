from django.db import models
from django.contrib.auth.models import User

def get_image_filename(instance, filename):
	return 'uploads/figures/{}'.format(filename)

class HoloProject(models.Model):
	""" A short title of the project."""
	title = models.CharField(max_length=255)

	""" A more detailed description."""
	description = models.TextField()

	""" The projects source code."""
	code = models.TextField()

	""" The input image (capture image)."""
	image = models.ImageField(upload_to='uploads/captures/')

	""" The original zip file. """
	file = models.FileField(upload_to='uploads/projects/')

	""" The original poster/creator of this post. """
	op = models.ForeignKey(User, related_name='op', on_delete=models.CASCADE)

	""" The users which down/upvoted this post. """
	upvoters = models.ManyToManyField(User, related_name='upvoter')
	downvoters = models.ManyToManyField(User, related_name='downvoter')

	""" Automatically generated timestamps."""
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Figure(models.Model):
	title = models.CharField(max_length=255)
	project = models.ForeignKey(HoloProject, related_name='figure_project', on_delete=models.CASCADE)
	file = models.ImageField(upload_to=get_image_filename)