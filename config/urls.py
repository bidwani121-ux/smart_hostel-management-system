from django.contrib import admin
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from accounts import views as account_views

urlpatterns = [
    path(
        "login/",
        login_not_required(
            LoginView.as_view(
                template_name="login.html",
                redirect_authenticated_user=True,
            )
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("admin/login/", LoginView.as_view(template_name="login.html")),
    path("admin/logout/", LogoutView.as_view()),
    path("admin/", admin.site.urls),
    path("", account_views.homepage, name="homepage"),
    path("", account_views.homepage, name="home"),
    path("dashboard/", account_views.dashboard, name="dashboard"),
    path("students/", include("students.urls")),
    path("rooms/", include("rooms.urls")),
    path("fees/", include("fees.urls")),
]