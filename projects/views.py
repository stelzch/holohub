from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProjectForm
from .models import HoloProject


def index(request):
	data = {
		'projects': HoloProject.objects.all()
	}
	return render(request, 'projects/freshfeed.html', data)

@login_required
def create(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			print("Form valid")
			project = HoloProject()
			project.title = form.cleaned_data['title']
			project.description = form.cleaned_data['description']
			project.file = form.cleaned_data['file']
			project.op = request.user
			with ZipFile(project.file.path) as mzip:
				print("Zip contains ", mzip.namelist())
			return HttpResponseRedirect('/')
	else:
		form = ProjectForm()
	return render(request, 'projects/create.html', {'form': form})