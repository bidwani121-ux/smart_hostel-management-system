from django.contrib.auth.decorators import login_not_required
from django.shortcuts import render


@login_not_required
def homepage(request):
    return render(request, "home.html")


def dashboard(request):
    return render(request, "dashboard.html")

# Create your views here.
