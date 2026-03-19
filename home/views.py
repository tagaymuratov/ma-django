from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from home.models import EventPage

@login_required
def register_for_event(request, event_id):
    event = EventPage.objects.get(id=event_id)
    event.participants.add(request.user)
    return redirect(event.url)