from .models import events
from django.views import generic, View
from blog.models import User
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from .forms import EventForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
class EventList(generic.ListView):
    model = events
    queryset = events.objects.filter(approve=True).order_by("-event_date")
    template_name = "events.html"
    paginate_by = 6


@login_required
def add_event(request):
    """Add Event Method"""
    submitted = False
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        print("chk post")
        if form.is_valid():
            event_obj = form.save(commit=False)
            event_obj.creator = request.user
            event_obj.save()
            form.save()
            messages.success(
                request, 'The event has been added successfully, awaiting approval')
            return redirect('events')
        else:
            print("Error")
            form = EventForm
            if 'submitted' in request.POST:
                submitted = True

    return render(request, 'add_event.html', {'form': form, 'submitted': submitted})


# login required resolves issues with non-users.
@login_required
def PostEvents(request, location):
    post = get_object_or_404(events, location=location)
    print(post)
    if post.guests.filter(id=request.user.id).exists():
        post.guests.remove(request.user)
    else:
        post.guests.add(request.user)

    return redirect('events')


@login_required
def edit_event(request, pk):
    events_obj = events.objects.get(id=pk)
    form = EventForm(instance=events_obj)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=events_obj)
        if form.is_valid():
            form.save()
            messages.success
            (request, 'The event has been updated successfully!')

            return redirect('events')

    context = {'form': form}
    return render(request, 'edit_event.html', context)


@login_required
def delete_event(request, pk):
    events_obj = events.objects.get(id=pk)
    if request.method == "POST":
        if events_obj.creator == events_obj.creator:
            events_obj.delete()
            messages.success
            (request, 'The event has been deleted successfully!')
            return redirect('events')
    else:
        messages.error
        (request, 'You currently do not have access to delete this')
    return render(request, 'delete_event.html')
