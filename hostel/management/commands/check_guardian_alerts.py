
from django.core.management.base import BaseCommand
from django.utils import timezone

from hostel.models import Student, StudentMovement, GuardianAlertLog


class Command(BaseCommand):
    help = "Check students who have no recorded check-out today"

    def handle(self, *args, **options):
        today = timezone.localdate()

        # Get students who have a guardian contact number
        students = Student.objects.exclude(
            guardian_contact__isnull=True
        ).exclude(
            guardian_contact__exact=''
        )

        # Find students who have a recorded check-out today
        checked_out_ids = StudentMovement.objects.filter(
            movement_date=today,
            check_out_time__isnull=False
        ).values_list('student_id', flat=True).distinct()

        # Find students without a recorded check-out
        missing_students = students.exclude(
            id__in=checked_out_ids
        )

        self.stdout.write(
            self.style.WARNING(
                f"\nChecking guardian alerts for: {today}"
            )
        )

        if not missing_students.exists():
            self.stdout.write(
                self.style.SUCCESS(
                    "All students have a recorded check-out."
                )
            )
            return

        self.stdout.write(
            self.style.WARNING(
                "\nStudents with no recorded check-out:"
            )
        )

        for student in missing_students:
            alert, created = GuardianAlertLog.objects.get_or_create(
                student=student,
                alert_date=today,
                defaults={
                    'status': 'PENDING',
                    'message': 'No check-out was recorded by 9:00 AM.'
                }
            )

            self.stdout.write(
                f"- {student.name} (ID: {student.student_id})"
            )

            if created:
                self.stdout.write("  Guardian alert record created.")
            else:
                self.stdout.write("  Alert record already exists. No duplicate created.")

        self.stdout.write(
            self.style.SUCCESS(
                "\nCheck completed. No messages were sent."
            )
        )

