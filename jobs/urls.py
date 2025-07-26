from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # auth
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("post-login-redirect/", views.post_login_redirect, name="post_login_redirect"),

    # dashboards
    path("employer/dashboard/", views.employer_dashboard, name="employer_dashboard"),
    path("applicant/dashboard/", views.applicant_dashboard, name="applicant_dashboard"),

    # employer
    path("jobs/new/", views.job_create, name="job_create"),
    path("jobs/<int:pk>/applicants/", views.job_applicants, name="job_applicants"),

    # applicant
    path("jobs/", views.job_list, name="job_list"),
    path("jobs/<int:pk>/", views.job_detail, name="job_detail"),
    path("jobs/<int:pk>/apply/", views.apply_job, name="apply_job"),
    path("my-applications/", views.my_applications, name="my_applications"),
]
