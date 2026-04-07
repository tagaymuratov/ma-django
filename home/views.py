from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.utils.text import get_valid_filename
from urllib.parse import quote

from home.models import EventPage, EventParticipant


@login_required
def get_excel_report(request, event_id):
    import openpyxl

    event = get_object_or_404(EventPage, id=event_id)
    participants_records = EventParticipant.objects.filter(event=event).select_related('user')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = event.title
    ws.append([
        "Фамилия", "Имя", "Email", "Город", "Телефон", "ИИН", "Место работы", "Специальность", 'Посетил мероприятие'
    ])

    for record in participants_records:
        user = record.user
        attendance_status = "V" if record.is_attended else "X"
        ws.append([
            user.last_name,
            user.first_name,
            user.email,
            user.city,
            user.phone,
            user.iin,
            user.work_place,
            user.specialty,
            attendance_status
        ])

    safe_title = get_valid_filename(event.title)
    if len(safe_title) > 150:
        safe_title = safe_title[:150]
    filename = f"{safe_title}.xlsx"

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f"attachment; filename*=UTF-8''{quote(filename)}"

    wb.save(response)
    return response

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