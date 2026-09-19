from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, Application, Employer
from django.db.models import Q

def job_list(request):
    query = request.GET.get('q')
    if query:
        # Search filter logic
        jobs = Job.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        )
    else:
        jobs = Job.objects.all()
    return render(request, 'job_board/job_list.html', {'jobs': jobs, 'query': query})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'job_board/job_detail.html', {'job': job})

def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        resume = request.FILES.get('resume') # Handling file upload

        Application.objects.create(
            job=job,
            candidate_name=name,
            email=email,
            resume=resume
        )
        return render(request, 'job_board/apply_success.html', {'job': job})
    return redirect('job_detail', pk=pk)
