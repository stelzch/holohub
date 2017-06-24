import zipfile
import json
from PIL import Image
from django.template.defaultfilters import filesizeformat

@deconstructible
class ProjectFileValidator(object):
	error_messages = {
		'max_size': ("The maximum file is %(max_size)s."
					 "Your file is %(size)s."),
		'invalid': ("This file is not a valid HoloView project file"),
	}

	def __init__(self, max_size=None):
		self.max_size = max_size

	def __call__(self, data):
		if self.max_size is not None and data.size > self.max_size:
			params = {
				'max_size': filesizeformat(self.max_size),
				'size': filesizeformat(data.size),
			}
			raise ValidationError(self.error_messages['max_size'], 'max_size', params)
		try:
			mzip = zipfile.ZipFile(data.path)

			""" Retrieve metadata from the json file. """
			if 'meta.json' not in zip.namelist():
				raise Exception()
				print("No metadata")
			with zipfile.open('meta.json') as file:
				meta = json.load(file)
				if not isinstance(meta['title'], 'str'):
					print("No title")
					raise Exception()
				if not isinstance(meta['description'], 'str'):
					print("No description")
					raise Exception()
				figurelist = meta['figures']

			""" Walk over all figures and the captured image and verify them."""
			figurelist.append('image.jpg')
			for image in figurelist:
				with zipfile.open(image) as image:
					im = Image.open(image)
					if not im.verify():
						print("PIL says image not valid")
						raise Exception
					im.close()
				

		except Exception:
			raise ValidationError(self.error_messages['invalid'], 'invalid')