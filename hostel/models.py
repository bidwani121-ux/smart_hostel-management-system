from django.db import models


# 1. Student Database
class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    guardian_contact = models.CharField(max_length=15)
    admission_date = models.DateField()

    def __str__(self):
        return self.name


# 2. Room Database
class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20)
    total_beds = models.PositiveIntegerField()

    def __str__(self):
        return self.room_number


# 3. Room Allocation Database
class RoomAllocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    bed_number = models.PositiveIntegerField()
    allocation_date = models.DateField()
    vacate_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="Active")

    def __str__(self):
        return f"{self.student.name} - {self.room.room_number}"


# 4. Attendance Database
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    attendance_date = models.DateField()
    marked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Present")
    qr_reference = models.CharField(max_length=100, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "attendance_date"],
                name="unique_student_attendance_per_day"
            )
        ]

    def __str__(self):
        return f"{self.student.name} - {self.attendance_date}"


# 5. Complaint Database
class Complaint(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    title = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# 6. Fee Payment Database
class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=30, blank=True)
    transaction_id = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.amount}"


# 7. Fee Reminder Database
class FeeReminder(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    fee_payment = models.ForeignKey(FeePayment, on_delete=models.PROTECT)
    message = models.TextField()
    reminder_date = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Reminder - {self.student.name}"

