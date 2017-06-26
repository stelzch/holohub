import zipfile
import shutil
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ProjectForm
from .models import HoloProject
from .utils import create_project


def index(request):
	data = {
		'projects': HoloProject.objects.all()
	}
	return render(request, 'projects/freshfeed.html', data)

@login_required
def create(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST, request.FILES)
		if form.is_valid():
			print("Form valid")
			try:
				create_project(request, form)
			except AttributeError:
				raise
				return HttpResponse('project invalid')
			return HttpResponseRedirect('/')
		else:
			print(form.errors)
	else:
		form = ProjectForm()
	return render(request, 'projects/create.html', {'form': form})