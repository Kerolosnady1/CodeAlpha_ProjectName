from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Registration

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

def register_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        Registration.objects.create(event=event, full_name=full_name, email=email)
        return render(request, 'events/success.html', {'event': event})
    return redirect('event_detail', pk=pk)
