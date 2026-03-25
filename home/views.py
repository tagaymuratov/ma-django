from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from home.models import EventPage, EventParticipant

@login_required
def register_for_event(request, event_id):
    event = EventPage.objects.get(id=event_id)
    EventParticipant.objects.get_or_create(
        event=event,
        user=request.user
    )
    return redirect(event.url)

def mark_attendance(request, event_id, user_id):
    record = get_object_or_404(
        EventParticipant,
        event_id=event_id,
        user_id=user_id
    )

    record.is_attended = not record.is_attended
    record.save()

    return redirect(request.META.get("HTTP_REFERER", "/"))