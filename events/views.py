from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm

@login_required
def event_list(request):
    events = Event.objects.all().order_by('event_date')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def event_create(request):
    # Only logged-in users can create an event.
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

