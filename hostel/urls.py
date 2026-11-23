
from django.urls import path
from . import views

urlpatterns = [
    path('scan-qr/', views.scan_student_qr, name='scan_student_qr'),
    path('scan/', views.scan_page, name='scan_page'),
]