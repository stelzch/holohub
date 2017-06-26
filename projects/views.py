import zipfile
import shutil
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from el_pagination.decorators import page_template
from .forms import ProjectForm
from .models import HoloProject
from .utils import create_project


def index(request):
	data = {
		'projects': HoloProject.objects.all()
	}
	return render(request, 'projects/freshfeed.html', data)

@page_template('projects/project_list_page.html')
@login_required
def feed(request, template='projects/feed.html', extra_context={}):
    projects = HoloProject.objects.all().order_by('-created_at')
    context = {
        'project_list': projects,
        'user': request.user,
    }
    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)

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

@login_required
@require_POST
def project_up(request, project_id):
        proj = get_object_or_404(HoloProject, pk__exact=project_id)

        """Check if the user already voted."""
        if proj.downvoters.filter(pk__exact=request.user.pk).exists():
                proj.upvoters.add(request.user)
                proj.downvoters.remove(request.user)
                return HttpResponse("Success")
        elif proj.upvoters.filter(pk__exact=request.user.pk).exists():
                return HttpResponse("Error")
        else:
                proj.upvoters.add(request.user)
                return HttpResponse("Success")

@login_required
@require_POST
def project_down(request, project_id):
        proj = get_object_or_404(HoloProject, pk__exact=project_id)

        """Check if the user already voted."""
        if proj.upvoters.filter(pk__exact=request.user.pk).exists():
                proj.downvoters.add(request.user)
                proj.upvoters.remove(request.user)
                return HttpResponse("Success")
        elif proj.downvoters.filter(pk__exact=request.user.pk).exists():
                return HttpResponse("Error")
        else:
                proj.downvoters.add(request.user)
                return HttpResponse("Success")

@login_required
def project(request, project_id):
    proj = get_object_or_404(HoloProject, pk__exact=project_id)
    context = {
        'project': proj,
        'user': request.user,
    }
    return render(request, 'projects/project.html', context)