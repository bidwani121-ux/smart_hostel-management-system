
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from .models import Student, StudentMovement


@staff_member_required
@require_POST
def scan_student_qr(request):

    student_id = request.POST.get('student_id')

    if not student_id:
        return JsonResponse({
            'success': False,
            'message': 'Student ID is required.'
        }, status=400)

    student = Student.objects.filter(student_id=student_id).first()
    if not student:
        return JsonResponse({
            'success': False,
            'message': f'Student ID "{student_id}" not found in database.'
        }, status=404)

    now = timezone.now()

    # Check whether the student is currently outside
    movement = StudentMovement.objects.filter(
        student=student,
        check_out_time__isnull=False,
        check_in_time__isnull=True
    ).order_by('-check_out_time').first()

    if movement:
        # Student is returning to hostel
        movement.check_in_time = now
        movement.status = 'INSIDE'
        movement.save()

        action = 'CHECK-IN'
        message = f'{student.name} has returned to the hostel.'

    else:
        # Student is leaving the hostel
        movement = StudentMovement.objects.create(
            student=student,
            movement_date=timezone.localdate(),
            check_out_time=now,
            status='OUTSIDE'
        )

        action = 'CHECK-OUT'
        message = f'{student.name} has left the hostel.'

    return JsonResponse({
        'success': True,
        'student': student.name,
        'student_id': student.student_id,
        'action': action,
        'message': message,
        'time': timezone.localtime(now).strftime('%I:%M %p')
    })


@staff_member_required
def scan_page(request):
    return render(request, 'hostel/scan.html')
