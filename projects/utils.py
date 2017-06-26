import shutil
import zipfile
import json
import logging
from .models import HoloProject, Figure
from django.core.files import File

logger = logging.getLogger(__name__)

def create_project(request, form,):
	"""Create a HoloProject and its figures from the form.
	Ensure that all form data is cleaned before passing it to this function!"""
	project = HoloProject()
	project.file = request.FILES['projectfile']
	project.op = request.user
	try:
		with zipfile.ZipFile(project.file) as mzip:
			# Retrieve metadata from the json file.
			if 'meta.json' not in mzip.namelist():
				logger.error('Project file does not contain meta.json')
				raise AttributeError('Project file does not contain meta.json')
			with mzip.open('meta.json') as file:
				metadata = json.load(file)
				if not isinstance(metadata['title'], str):
					logger.error('Project meta.json does not contain a title')
					raise AttributeError('Project meta.json does not contain a title')
				if not isinstance(metadata['description'], str):
					logger.error('Project meta.json does not contain a description')
					raise AttributeError('Project meta.json does not contain a description')
				figurelist = metadata['figures']

			project.title = metadata['title']
			project.image = File(mzip.open('image.png'))
			with mzip.open('script.py', 'r') as codefile:
				project.code = codefile.read()
				print("Reading code: {}".format(project.code))
			project.description = metadata['description']
			project.save()
			for figure in metadata['figures']:
				with mzip.open(figure) as figurefile:
					fig = Figure()
					fig.op = request.user
					fig.title = "".join(figure.split(".")[:-1])
					fig.file = File(figurefile)
					fig.save()
					project.figures.add(fig)
			project.save()
	except AttributeError:
		if project.pk is not None:
			project.delete()
		raise