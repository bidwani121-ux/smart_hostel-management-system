
from django.contrib import admin
from .models import (
    Student,
    Room,
    RoomAllocation,
    Attendance,
    Complaint,
    FeePayment,
    FeeReminder
)


# Room Admin with Bed Availability
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'room_number',
        'room_type',
        'total_beds',
        'occupied_beds',
        'available_beds'
    )

    def occupied_beds(self, obj):
        return obj.roomallocation_set.filter(status="Active").count()

    occupied_beds.short_description = "Occupied Beds"

    def available_beds(self, obj):
        return obj.total_beds - self.occupied_beds(obj)

    available_beds.short_description = "Available Beds"


# Register Other Models
admin.site.register(Student)
admin.site.register(RoomAllocation)
admin.site.register(Attendance)
admin.site.register(Complaint)
admin.site.register(FeePayment)
admin.site.register(FeeReminder)
